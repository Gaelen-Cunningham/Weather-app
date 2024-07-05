import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_get_weather_success():
    mock_response = {
        "main": {
            "temp_min": 15,
            "temp_max": 25,
            "humidity": 80
        }
    }
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = client.get("/weather/testcity")
        assert response.status_code == 200
        data = response.json()
        assert data["City"] == "testcity"
        assert data["Minimum Temperature"] == 15
        assert data["Maximum Temperature"] == 25
        assert data["Average Temperature"] == 20.0
        assert data["Humidity"] == 80

def test_get_weather_city_not_found():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404

        response = client.get("/weather/testcity")
        assert response.status_code == 404
        assert response.json() == {"detail": "City not found"}

def test_get_weather_internal_server_error():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500

        response = client.get("/weather/testcity")
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal server error"}
import pytest
import requests

# Assuming your FastAPI is running locally on port 8000
BASE_URL = 'http://127.0.0.1:8000/'

@pytest.fixture
def api_url():
    return BASE_URL

def test_get_weather_valid_city(api_url):
    city = 'London'
    url = f"{api_url}/weather/{city}"
    response = requests.get(url)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()
    assert data["City"] == city, f"Expected city '{city}', but got '{data['City']}'"
    assert "Minimum Temperature" in data, "Expected 'Minimum Temperature' in response"
    assert "Maximum Temperature" in data, "Expected 'Maximum Temperature' in response"
    assert "Average Temperature" in data, "Expected 'Average Temperature' in response"

def test_get_weather_invalid_city(api_url):
    city = 'InvalidCityName'
    url = f"{api_url}/weather/{city}"
    response = requests.get(url)

    assert response.status_code == 404, f"Expected status code 404 for invalid city, but got {response.status_code}"

    data = response.json()
    assert "detail" in data, "Expected 'detail' in response"
    assert "City not found" in data["detail"], f"Expected 'City not found' message in response, but got {data['detail']}"

# Add more test cases as needed for different scenarios (error cases, edge cases, etc.)

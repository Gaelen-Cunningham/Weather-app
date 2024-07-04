import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/weather/{city}")
async def get_weather(city: str):
    weather_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=953a93326f0b7ebbf0d6bbaaa9386794&units=metric")

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        minimum_temp = weather_data["main"]["temp_min"]
        maximum_temp = weather_data["main"]["temp_max"]
        average_temp = (weather_data["main"]["temp_min"] + weather_data["main"]["temp_max"]) / 2
        humidity = weather_data["main"]["humidity"]
        return {
            "City": city,
            "Minimum Temperature": minimum_temp,
            "Maximum Temperature": maximum_temp,
            "Average Temperature": round(average_temp, 2),
            "Humidity": humidity
        }    
    elif weather_response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found")
    else:
        raise HTTPException(status_code=500, detail="Internal server error")

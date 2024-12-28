import requests
import csv
from datetime import datetime

# Your API keys
WEATHER_API_KEY = "3443df9e6a3d2df4ae5a38bca00b7619"

# API endpoints
weather_base_url = "https://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data dynamically based on user input location
def fetch_weather_for_location(lat, lon, api_key):
    url = f"{weather_base_url}?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Latitude": lat,
            "Longitude": lon,
            "Temperature": data['main']['temp'],
            "Rainfall": data.get('rain', {}).get('1h', 0.0),
            "Humidity": data['main']['humidity'],
        }
    else:
        print(f"Error fetching weather data: {response.json()}")
        return None

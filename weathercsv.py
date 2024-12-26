import requests
import csv
from datetime import datetime

# Your API key
API_KEY = "3443df9e6a3d2df4ae5a38bca00b7619"

# Cities to fetch data for
cities = ["London", "New York", "Mumbai"]

# Output CSV file name
csv_file = "weather_data.csv"

# OpenWeatherMap API endpoint for weather data
base_url = "https://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data
def fetch_weather(city, api_key):
    url = f"{base_url}?q={city}&appid={api_key}&units=metric"  # Metric units for temperature
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current date and time
            "Location": city,
            "Temperature": data['main']['temp'],  # Temperature in Celsius
            "Rainfall": data.get('rain', {}).get('1h', 0.0),  # Rainfall in the last hour, default 0.0
            "Humidity": data['main']['humidity']  # Humidity percentage
        }
    else:
        print(f"Error fetching data for {city}: {response.json()}")
        return None

# Create and write to the CSV file
with open(csv_file, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Date", "Location", "Temperature", "Rainfall", "Humidity"])
    writer.writeheader()  # Write column headers

    # Fetch data for each city and write to the CSV
    for city in cities:
        weather = fetch_weather(city, API_KEY)
        if weather:
            writer.writerow(weather)

print(f"Weather data has been saved to {csv_file}")

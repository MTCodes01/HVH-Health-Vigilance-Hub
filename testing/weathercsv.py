import requests
from datetime import datetime

# Your API keys
WEATHER_API_KEY = "3443df9e6a3d2df4ae5a38bca00b7619"
GEONAMES_USERNAME = "urban_xtreme"  # Replace with your GeoNames username

# API endpoints
weather_base_url = "https://api.openweathermap.org/data/2.5/weather"
geonames_base_url = "http://api.geonames.org/findNearbyPlaceNameJSON"

# Function to fetch weather data dynamically based on user input location
def fetch_weather_for_location(lat, lon, weather_api_key, geonames_username):
    # Fetch weather data
    weather_url = f"{weather_base_url}?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
    weather_response = requests.get(weather_url)
    
    if weather_response.status_code != 200:
        print(f"Error fetching weather data: {weather_response.json()}")
        return None
    
    weather_data = weather_response.json()
    
    # Extract weather data safely
    temperature = weather_data['main'].get('temp', None)
    humidity = weather_data['main'].get('humidity', None)
    rainfall = weather_data.get('rain', {}).get('1h', 0.0)  # Default to 0 if no rain data
    if temperature is None or humidity is None:
        print("Error: Incomplete weather data")
        return None

    # Fetch population density data from GeoNames
    geonames_url = f"{geonames_base_url}?lat={lat}&lng={lon}&username={geonames_username}"
    geonames_response = requests.get(geonames_url)
    
    if geonames_response.status_code != 200:
        print(f"Error fetching GeoNames data: {geonames_response.json()}")
        return None
    
    geonames_data = geonames_response.json()
    
    # Extract population density safely
    population_density = 0  # Default population density if unavailable
    if "geonames" in geonames_data and geonames_data["geonames"]:
        population_density = geonames_data["geonames"][0].get("population", 0)

    # Return the combined data
    return {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Latitude": lat,
        "Longitude": lon,
        "Temperature": temperature,
        "Rainfall": rainfall,
        "Humidity": humidity,
        "Population Density": population_density
    }

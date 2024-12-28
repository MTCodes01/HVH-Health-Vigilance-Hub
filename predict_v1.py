import folium
import pandas as pd
from folium.plugins import HeatMap
from prophet import Prophet

# Load the CSV data, assuming it contains columns: 'date', 'location', 'disease', 'latitude', 'longitude', 'cases'
data = pd.read_csv("time_series_disease_data.csv")

# Filter data for a specific location and disease
location = 1  # Example location ID
disease = "Flu"  # Example disease
filtered_data = data[(data["location"] == location) & (data["disease"] == disease)]

# Prepare data for Prophet
prophet_data = filtered_data[["date", "cases"]].copy()  # Make a copy to avoid SettingWithCopyWarning
prophet_data.rename(columns={"date": "ds", "cases": "y"}, inplace=True)

# Train the Prophet model
model = Prophet()
model.fit(prophet_data)

# Forecast future cases (e.g., predict for 30 days)
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Create a DataFrame with the forecasted values
forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

# Now, extract the forecasted cases along with latitude and longitude from the original data
locations = filtered_data[['latitude', 'longitude']].copy()
locations['forecasted_cases'] = forecast['yhat'][:len(locations)]  # Add forecasted cases for each location

# Create a folium map centered around a specific location
map_center = [40.137700857991874, -85.67509607538854]  # Center of the US, or you can use the mean of the latitudes/longitudes
m = folium.Map(
    location=map_center,  # Center map
    zoom_start=4,  # Initial zoom level
    control_scale=True,
    zoom_control=False,  # Disable zoom controls
    scrollWheelZoom=False,  # Disable scroll wheel zoom
    dragging=True,  # Enable map dragging
    min_zoom=4,
    max_zoom=4 
)

# Prepare heatmap data (latitude, longitude, forecasted cases)
heat_data = locations[['latitude', 'longitude', 'forecasted_cases']].values.tolist()

# Add HeatMap to the map
HeatMap(heat_data).add_to(m)

# Save the map to an HTML file
m.save("heatmap.html")

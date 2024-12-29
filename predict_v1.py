import joblib
import folium
from folium.plugins import HeatMap
import numpy as np
from weathercsv import fetch_weather_for_location
from folium.plugins import Search

# Symptom-to-disease mapping
SYMPTOM_DISEASE_MAP = {
    "fever": ["Dengue", "Malaria", "Flu", "Covid"],
    "cough": ["Covid", "Flu"],
    "rash": ["Dengue", "Measles"],
    "chills": ["Malaria"],
}

# Load the trained model
model = joblib.load("disease_predictor_model.pkl")

# Function to predict disease and spread data
def predict_disease_and_spread(temp, humidity, density, lat, lon, rainfall, symptoms):
    # Identify possible diseases from symptoms
    possible_diseases = set()
    for symptom in symptoms:
        possible_diseases.update(SYMPTOM_DISEASE_MAP.get(symptom.lower(), []))

    # Prepare input data
    input_data = np.array([[temp, humidity, density, lat, lon, rainfall]])
    
    # Get predictions
    prediction_probabilities = model.predict_proba(input_data)[0]
    disease_mapping = {index: category for index, category in enumerate(['Dengue', 'Malaria', 'Flu', 'Covid'])}
    
    # Map prediction probabilities to diseases
    disease_spread = {}
    for index, probability in enumerate(prediction_probabilities):
        disease_name = disease_mapping[index]
        if disease_name in possible_diseases:
            disease_spread[disease_name] = probability

    # Select the most probable disease
    predicted_disease = max(disease_spread, key=disease_spread.get) if disease_spread else "Unknown"
    return predicted_disease, disease_spread

# Function to generate heatmap based on prediction probabilities


# Function to generate heatmap based on prediction probabilities# Function to generate heatmap with calendar and search bar
def generate_heatmap(location, predicted_disease, spread_data, estimated_days):
    m = folium.Map(location=location, zoom_start=10)
    
    # Create a FeatureGroup to hold markers
    feature_group = folium.FeatureGroup(name="Searchable Locations")
    
    # Add a marker for the input location
    folium.Marker(
        location=location,
        popup=f"Predicted Disease: {predicted_disease}",
        tooltip="Click for more info"
    ).add_to(feature_group)
    
    # Add FeatureGroup to the map
    feature_group.add_to(m)
    
    # Add search functionality
    search = Search(layer=feature_group, placeholder="Search for a location", search_label="name", collapsed=False)
    m.add_child(search)
    
    # Generate heatmap points based on spread probabilities
    for day in range(1, estimated_days + 1):
        weight_factor = day / estimated_days
        points = [
            [location[0] + np.random.uniform(-0.01, 0.01),
             location[1] + np.random.uniform(-0.01, 0.01),
             spread_data[predicted_disease] * weight_factor]
        ]
        HeatMap(points, radius=15, blur=10).add_to(m)

    # Add calendar functionality to the map
    calendar_code = """
        <style>
            #calendar {
                position: fixed;
                top: 10px;
                left: 10px;
                z-index: 1000;
                background: white;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            #calendar input {
                width: 200px;
                padding: 5px;
                margin: 5px 0;
                font-size: 14px;
            }
        </style>
        <div id="calendar">
            <label for="date">Select Date:</label>
            <input type="date" id="date" name="date">
        </div>
        <script>
            document.getElementById('date').addEventListener('change', function() {
                alert('Selected date: ' + this.value); // Add dynamic functionality here
            });
        </script>
    """
    m.get_root().html.add_child(folium.Element(calendar_code))
    
    heatmap_file = f"heatmap_{predicted_disease}.html"
    m.save(heatmap_file)
    print(f"Heatmap saved as {heatmap_file}")



# Main Function
def main():
    # User Inputs
    symptoms = input("Enter symptoms (comma-separated, e.g., fever,cough): ").split(",")
    lat = float(input("Enter latitude: "))
    lon = float(input("Enter longitude: "))
    estimated_days = int(input("Enter estimated days for spread: "))

    # Fetch weather data (including population density)
    weather_data = fetch_weather_for_location(lat, lon, "3443df9e6a3d2df4ae5a38bca00b7619", "urban_xtreme")

    if not weather_data:
        print("Failed to fetch weather data.")
        return

    # Extract population density from weather_data
    density = weather_data['Population Density']

    # Predict disease and spread data
    predicted_disease, spread_data = predict_disease_and_spread(
        weather_data['Temperature'], weather_data['Humidity'], density, lat, lon, weather_data['Rainfall'], symptoms
    )

    if predicted_disease == "Unknown":
        print("Could not determine the disease based on the input symptoms.")
        return

    print(f"Predicted Disease: {predicted_disease}")
    print(f"Spread Data: {spread_data}")
    
    # Generate the heatmap
    generate_heatmap([lat, lon], predicted_disease, spread_data, estimated_days)

if __name__ == "__main__":
    main()

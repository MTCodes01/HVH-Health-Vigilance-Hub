import joblib
import folium
from folium.plugins import HeatMap
import numpy as np
from weathercsv import fetch_weather_for_location

# Symptom-to-disease mapping
SYMPTOM_DISEASE_MAP = {
    "fever": ["Dengue", "Malaria", "Flu", "Covid"],
    "cough": ["Covid", "Flu"],
    "rash": ["Dengue", "Measles"],
    "chills": ["Malaria"],
}

# Load the trained model
model = joblib.load("disease_predictor_model.pkl")

# Function to predict disease
def predict_disease(temp, humidity, density, lat, lon, rainfall, symptoms):
    possible_diseases = set()
    for symptom in symptoms:
        possible_diseases.update(SYMPTOM_DISEASE_MAP.get(symptom.lower(), []))

    input_data = np.array([[temp, humidity, density, lat, lon, rainfall]])
    prediction = model.predict(input_data)
    disease_mapping = {index: category for index, category in enumerate(['Dengue', 'Malaria', 'Flu', 'Covid'])}
    predicted_disease = disease_mapping[prediction[0]]

    if predicted_disease in possible_diseases:
        return predicted_disease
    return "Unknown"

# Function to generate heatmap
def generate_heatmap(location, predicted_disease, estimated_days):
    m = folium.Map(location=location, zoom_start=10)
    for day in range(1, estimated_days + 1):
        radius = day * 10  # Increase radius per day
        HeatMap([[location[0], location[1], radius]]).add_to(m)
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

    # Fetch weather data
    weather_data = fetch_weather_for_location(lat, lon, "3443df9e6a3d2df4ae5a38bca00b7619")
    if not weather_data:
        print("Failed to fetch weather data.")
        return

    density = 5000  # Placeholder for population density; replace with actual data or logic
    predicted_disease = predict_disease(
        weather_data['Temperature'], weather_data['Humidity'], density, lat, lon, weather_data['Rainfall'], symptoms
    )
    print(f"Predicted Disease: {predicted_disease}")
    generate_heatmap([lat, lon], predicted_disease, estimated_days)

if __name__ == "__main__":
    main()

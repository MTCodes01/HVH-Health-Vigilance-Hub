import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters for synthetic data
NUM_SAMPLES = 1000
AGES = np.random.randint(18, 80, NUM_SAMPLES)  # Age range: 18-80
FEVER = np.random.uniform(97.0, 104.0, NUM_SAMPLES)  # Body temperature
COUGH = np.random.choice([0, 1], NUM_SAMPLES, p=[0.4, 0.6])  # 0: No Cough, 1: Cough
FATIGUE = np.random.choice([0, 1], NUM_SAMPLES, p=[0.5, 0.5])  # 0: No Fatigue, 1: Fatigue
LOCATIONS = np.random.randint(1, 5, NUM_SAMPLES)  # Location ID (1-4, representing regions)
WEATHER_TEMP = np.random.uniform(30.0, 100.0, NUM_SAMPLES)  # Weather temperature (Fahrenheit)

# Generate disease labels based on rules (adjust as needed)
def generate_disease(fever, cough, fatigue, weather_temp):
    if fever > 101 and cough and fatigue:
        return random.choices(["Flu", "COVID-19"], weights=[0.4, 0.6])[0]
    elif fever > 100 and cough:
        return "Flu"
    elif fever < 99 and weather_temp < 40:
        return "Common Cold"
    else:
        return "No Disease"

DISEASE = [generate_disease(FEVER[i], COUGH[i], FATIGUE[i], WEATHER_TEMP[i]) for i in range(NUM_SAMPLES)]

# Create a DataFrame
data = {
    "age": AGES,
    "fever": FEVER,
    "cough": COUGH,
    "fatigue": FATIGUE,
    "location": LOCATIONS,
    "weather_temp": WEATHER_TEMP,
    "disease": DISEASE
}

df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv("synthetic_disease_data.csv", index=False)
print("Synthetic data saved to 'synthetic_disease_data.csv'.")

# Display the first few rows
print(df.head())

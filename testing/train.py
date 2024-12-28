import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Parameters for synthetic data
locations = [1, 2]  # Location IDs
diseases = ["Flu", "Dengue"]  # Disease types
start_date = datetime(2023, 12, 1)  # Start date for the time series
days = 30  # Number of days to generate data for

# Generate synthetic data
data = []
for loc in locations:
    for disease in diseases:
        date = start_date
        cases = random.randint(5, 20)  # Initial number of cases
        for _ in range(days):
            data.append({
                "location": loc,
                "disease": disease,
                "date": date.strftime('%Y-%m-%d'),  # Format the date
                "cases": cases,
                "temperature": random.uniform(10, 35),  # Random temperature between 10 and 35°C
                "humidity": random.uniform(40, 90),  # Random humidity between 40 and 90%
                "population_density": random.randint(300, 1000),  # Random population density
                "latitude": random.uniform(25, 50),  # Random latitude between 25 and 50
                "longitude": random.uniform(-125, -65)  # Random longitude between -125 and -65
            })
            date += timedelta(days=1)  # Increment the date by 1 day
            cases += random.randint(-3, 5)  # Randomly change the number of cases

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file = "time_series_disease_data.csv"
df.to_csv(csv_file, index=False)
print("\nGenerated Synthetic Data:")
print(df.head())

# Step 1: Prepare Features (X) and Target (y)
# Use 'temperature', 'humidity', 'population_density', 'latitude', 'longitude' as features
X = df[['temperature', 'humidity', 'population_density', 'latitude', 'longitude']]  # Features
y = df['disease']  # Target variable

# Encode 'disease' into numeric labels for model training (e.g., Flu=0, Dengue=1)
y = y.astype("category").cat.codes  # Convert diseases to numeric labels

# Step 2: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 4: Evaluate the Model
y_pred = model.predict(X_test)
print("\nModel Evaluation:")
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Step 5: Save the model
joblib.dump(model, "disease_predictor_model.pkl")
print("\nModel saved as 'disease_predictor_model.pkl'")

# Step 6: Predict for New User Input (based on new features)
def predict_disease(temperature, humidity, population_density, latitude, longitude):
    input_data = np.array([[temperature, humidity, population_density, latitude, longitude]])
    prediction = model.predict(input_data)
    disease_mapping = {index: category for index, category in enumerate(df["disease"].astype("category").cat.categories)}
    return disease_mapping[prediction[0]]

# **Updated User Input Section**
print("\nPlease enter the following information to predict the disease:")

# Taking new user input for prediction
new_entry = {
    "temperature": float(input("Enter temperature (°C): ")),
    "humidity": float(input("Enter humidity (%): ")),
    "population_density": int(input("Enter population density: ")),
    "latitude": float(input("Enter latitude: ")),
    "longitude": float(input("Enter longitude: "))
}

# Predict the disease for the new input
predicted_disease = predict_disease(**new_entry)
print("\nPredicted Disease for New User Input:", predicted_disease)

# **Appending the New Entry to the DataFrame**
new_entry['disease'] = predicted_disease  # Add the predicted disease to the new entry

# Convert the new entry to a DataFrame
new_entry_df = pd.DataFrame([new_entry])

# Concatenate the new entry with the original DataFrame and save to the CSV
df = pd.concat([df, new_entry_df], ignore_index=True)
df.to_csv(csv_file, index=False)
print("\nNew data added to the CSV file:", new_entry)

# Optional: Verify the data added to the CSV
print("\nUpdated Data Sample:\n", df.tail())

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the disease dataset
weather_df = pd.read_csv("time_series_disease_data.csv")

# Add new features if missing
weather_df['Rainfall'] = weather_df.get('Rainfall', 0)

# Prepare Features (X) and Target (y)
X = weather_df[['Temperature', 'Humidity', 'Population Density', 'Latitude', 'Longitude', 'Rainfall']]
y = weather_df['Disease']

# Encode 'Disease' into numeric labels
y = y.astype("category").cat.codes

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the Model
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the Model
joblib.dump(model, "disease_predictor_model.pkl")
print("\nModel saved as 'disease_predictor_model.pkl'")

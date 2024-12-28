import pandas as pd

# Load datasets
symptom_data = pd.read_csv("diseasesymptom.csv")
environmental_data = pd.read_csv("weather_data_with_density.csv")
case_data = pd.read_csv("dataset1.csv")

# Clean symptom-to-disease data
symptom_data.drop_duplicates(inplace=True)  # Remove duplicates
symptom_data.dropna(inplace=True)  # Remove rows with missing values

# Clean environmental data
environmental_data.drop_duplicates(inplace=True)
environmental_data.fillna({'Rainfall': 0}, inplace=True)  # Fill missing rainfall with 0

# Clean case data
case_data.drop_duplicates(inplace=True)
case_data.fillna({'Cases': 0}, inplace=True)

# Save cleaned files
symptom_data.to_csv("cleaned_symptom_data.csv", index=False)
environmental_data.to_csv("cleaned_environmental_data.csv", index=False)
case_data.to_csv("cleaned_case_data.csv", index=False)
print("Data cleaning complete. Cleaned files saved.")

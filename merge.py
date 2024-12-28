import pandas as pd

# Load datasets
symptom_data = pd.read_csv("cleaned_symptom_data.csv")
case_data = pd.read_csv("cleaned_case_data.csv")
environmental_data = pd.read_csv("cleaned_environmental_data.csv")

# Clean column names
symptom_data.columns = symptom_data.columns.str.strip()
case_data.columns = case_data.columns.str.strip()
environmental_data.columns = environmental_data.columns.str.strip()

# Rename 'Etiology' to 'Disease' if applicable
if "Etiology" in case_data.columns:
    case_data.rename(columns={"Etiology": "Disease"}, inplace=True)

# Check for common Diseases
common_diseases = set(symptom_data["Disease"]).intersection(case_data["Disease"])
print("Common Diseases:", common_diseases)

if not common_diseases:
    print("No common Diseases found. Consider using alternative keys or manual mapping.")

# Attempt merge on Disease
merged_data = pd.merge(symptom_data, case_data, on="Disease", how="inner")

# If no matches, try alternative keys
if merged_data.empty:
    print("No matches found on 'Disease'. Trying alternative merge on 'Primary Mode'...")
    if "Primary Mode" in symptom_data.columns and "Primary Mode" in case_data.columns:
        merged_data = pd.merge(symptom_data, case_data, on="Primary Mode", how="inner")

# If still empty, raise an error
if merged_data.empty:
    raise ValueError("No matching rows found between symptom_data and case_data. Check your merge keys.")

# Map State to Location (Example mapping)
location_mapping = {
    "Hong Kong": "hong kong",
    "Reunion": "reunion",
    "Mumbai": "mumbai",
    "Delhi": "delhi",
    "Anguilla": "anguilla"
}
merged_data = pd.merge(symptom_data, case_data, on=["State", "Year"], how="inner")

# Debugging info
print("Locations in merged_data after mapping:", merged_data["Location"].unique())
print("Locations in environmental_data:", environmental_data["Location"].unique())

# Merge with environmental_data
final_data = pd.merge(
    merged_data,
    environmental_data,
    on="Location",
    how="inner"
)

# Check final dataset
if final_data.empty:
    print("Warning: The final dataset is empty after merging.")
else:
    final_data.to_csv("training_data.csv", index=False)
    print("Data merged successfully into training_data.csv")

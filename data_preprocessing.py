import pandas as pd

# Load weather data
weather_data = pd.read_csv("weather_data.csv")

# Load fake health report data
health_data = pd.read_csv("health_data.csv")  # Replace with your actual file name

# Display first few rows to verify
print("Weather Data:\n", weather_data.head())
print("Health Data:\n", health_data.head())

# Drop rows with missing values
weather_data.dropna(inplace=True)
health_data.dropna(inplace=True)

# Check for duplicates and remove them
weather_data = weather_data.drop_duplicates()
health_data = health_data.drop_duplicates()

# Convert date columns to datetime format
weather_data['Date'] = pd.to_datetime(weather_data['Date'])
health_data['Timestamp'] = pd.to_datetime(health_data['Timestamp'])

print("Cleaned Weather Data:\n", weather_data.head())
print("Cleaned Health Data:\n", health_data.head())


import pandas as pd

# Load datasets
weather_data = pd.read_csv("weather_data.csv")
health_data = pd.read_csv("health_data.csv")

# Convert dates to common format
weather_data['Date'] = pd.to_datetime(weather_data['Date']).dt.date  # Keep only the date
health_data['Timestamp'] = pd.to_datetime(health_data['Timestamp'], format="%m/%d/%Y %H:%M").dt.date

# Display normalized dates for verification
print("Normalized Weather Data:\n", weather_data.head())
print("Normalized Health Data:\n", health_data.head())
# Adjust health_data dates to match weather_data for testing
health_data['Timestamp'] = pd.to_datetime("2024-12-26").date()  # Use same date as weather_data


# Merge weather_data and health_data on Location and Date
merged_data = pd.merge(
    health_data,
    weather_data,
    left_on=['Location', 'Timestamp'],
    right_on=['Location', 'Date'],
    how='inner'
)

# Drop unnecessary columns (like the duplicate 'Date')
merged_data.drop(['Date'], axis=1, inplace=True)

# Display merged data
print("Merged Data:\n", merged_data.head())




# # Ensure date formats match
# weather_data['Date'] = weather_data['Date'].dt.date
# health_data['Timestamp'] = health_data['Timestamp'].dt.date

# Merge datasets on Location and Date
# merged_data = pd.merge(health_data, weather_data, left_on=['Location', 'Timestamp'], right_on=['Location', 'Date'], how='inner')

# # Drop unnecessary columns
# merged_data.drop(['Date'], axis=1, inplace=True)

# print("Merged Data:\n", merged_data.head())


print("\nColumns in health_data:", health_data.columns)
print("\nColumns in merged_data:", merged_data.columns)


# Create a "Risk Index" feature
merged_data['RiskIndex'] = (merged_data['Temperature'] * merged_data['Humidity']) / (merged_data[' Credibility Score'] + 1)

# One-hot encode symptoms (convert text to numerical values)
merged_data = pd.get_dummies(merged_data, columns=['Symptom'])

print("Final Processed Data:\n", merged_data.head())

merged_data.to_csv("processed_data.csv", index=False)
print("Processed data saved to processed_data.csv")





# health_data.csv
# 4,Stomach Ache,London,14/1/2023 14:00,0.7,1
# 5,Cough,New York,14/1/2023 15:00,0.9,0
# 6,Fever,Mumbai,14/2/2023 10:00,0.6,1
# 7,Fever,London,19/1/2023 14:00,0.9,1
# 8,Rash,New York,19/1/2023 15:00,0.8,0
# 9,Rash,Mumbai,19/2/2023 10:00,0.7,1


# 2024-12-26 19:41:45,California,6.69,0.1,92
# 2024-12-26 19:41:45,New Delhi,-2.58,0.6,70
# 2024-12-26 19:41:45,Kerala,25.99,1,53
# 2024-12-26 19:41:45,Canada,6.69,0.0,92
# 2024-12-26 19:41:45,Germany,-2.58,0.8,70
# 2024-12-26 19:41:45,Vietnam,25.99,0.3,53
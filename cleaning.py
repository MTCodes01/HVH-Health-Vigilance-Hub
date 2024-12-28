import pandas as pd
# Load the data
file_path = 'time_series_covid19_confirmed_global.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)
# Drop rows with any missing values
cleaned_data = data.dropna()
# Save the cleaned data to a new CSV file
cleaned_data.to_csv('cleaned_data.csv', index=False)
print("Data cleaning complete. Cleaned data saved to 'cleaned_data.csv'.")
import pandas as pd

# Read both CSV files
cleaned_data = pd.read_csv('cleaned_data.csv')
weather_data = pd.read_csv('weather_data_with_density.csv')
print(weather_data)
print(cleaned_data)

# Rename Province/State to Location in cleaned_data for matching
cleaned_data = cleaned_data.rename(columns={'Province/State': 'Location'})
print(f"Total rows in cleaned file: {len(cleaned_data)}")
print(cleaned_data)
# Merge the dataframes based on Location
merged_df = pd.merge(
    weather_data,         # left dataframe
    cleaned_data,         # right dataframe
    on='Location',        # column to merge on
)

# Save the merged dataframe
merged_df.to_csv('merged.csv', index=False)

print("Merge completed. Check merged.csv for results.")
print(f"Total rows in merged file: {len(merged_df)}")
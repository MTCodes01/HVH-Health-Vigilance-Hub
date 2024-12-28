import pandas as pd
import random
from datetime import datetime, timedelta

# Parameters for synthetic data
locations = [1, 2, 3, 4, 5, 6]  # Location IDs
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
df.to_csv("time_series_disease_data.csv", index=False)

# Display the first few rows of the DataFrame
print(df.head())

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Step 1: Load Processed Data
data = pd.read_csv("processed_data.csv")

# Step 2: Separate Features (X) and Target Variable (y)
X = data.drop(['Outbreak'], axis=1)  # Drop the target column
y = data['Outbreak']  # Target column

# Step 3: Encode Categorical Columns (Location in this case)
label_encoder = LabelEncoder()  # Initialize LabelEncoder
X['Location'] = label_encoder.fit_transform(X['Location'])  # Encode Location column

# Step 4: Convert any date columns to numerical formats (if applicable)
if 'Date' in X.columns:
    X['Date'] = pd.to_datetime(X['Date'], errors='coerce')  # Handle any invalid date strings
    X['Date'] = X['Date'].astype(int) / 10**9  # Convert to timestamp in seconds

# Step 5: Ensure all columns are numeric
X = X.apply(pd.to_numeric, errors='coerce')  # Convert non-numeric columns to NaN and then to numbers

# Step 6: Fill missing values
X = X.fillna(X.mean())  # Fill NaN values with mean for numerical columns

# Step 7: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 8: Train the Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Model training complete.")

# Checking Accuracy
from sklearn.metrics import accuracy_score

# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)


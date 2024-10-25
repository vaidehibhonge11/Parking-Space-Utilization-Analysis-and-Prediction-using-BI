import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import psycopg2
import joblib

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="vehicle_detection_db",  
    user="postgres",           
    password="postgres",       
    host="localhost"                
)

# Fetch data from PostgreSQL
query = "SELECT date, hour, vehicle_count FROM detection_vehiclehourlystats"
df = pd.read_sql(query, conn)

# Feature engineering: Extract weekday from the date
df['weekday'] = pd.to_datetime(df['date']).dt.weekday

# Prepare features and labels
X = df[['hour', 'weekday']]  # Features: hour of the day and the weekday
y = df['vehicle_count']      # Label: vehicle count for the hour

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model (using Decision Tree Regressor)
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, 'peak_hour_predictor.pkl')

print("Model trained and saved as peak_hour_predictor.pkl")

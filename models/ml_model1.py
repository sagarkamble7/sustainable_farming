import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the farmer advisor dataset
farmer_df = pd.read_csv(r"farmer_advisor_dataset.csv")

# Define features and target for crop yield prediction
X_farm = farmer_df[['Soil_pH', 'Soil_Moisture', 'Temperature_C', 'Rainfall_mm', 'Fertilizer_Usage_kg']]
y_farm = farmer_df['Crop_Yield_ton']

# Split the data into training and testing sets
X_train_farm, X_test_farm, y_train_farm, y_test_farm = train_test_split(X_farm, y_farm, test_size=0.2, random_state=42)

# Train the Random Forest model for crop yield prediction
farm_model = RandomForestRegressor(random_state=42)
farm_model.fit(X_train_farm, y_train_farm)

# Predict crop yield using the trained model
def predict_crop_yield(soil_pH, moisture, temp, rainfall, fertilizer):
    prediction = farm_model.predict([[soil_pH, moisture, temp, rainfall, fertilizer]])[0]
    return prediction

# Evaluate the model on test data
y_pred_farm = farm_model.predict(X_test_farm)
mse_farm = mean_squared_error(y_test_farm, y_pred_farm)
print(f"Farmer Dataset Model MSE: {mse_farm}")


# Load the market researcher dataset
market_df = pd.read_csv(r"market_researcher_dataset.csv")

# Define features and target for market price prediction
X_market = market_df[['Demand_Index', 'Supply_Index', 'Competitor_Price_per_ton', 'Economic_Indicator', 'Weather_Impact_Score']]
y_market = market_df['Market_Price_per_ton']

# Split the data into training and testing sets
X_train_market, X_test_market, y_train_market, y_test_market = train_test_split(X_market, y_market, test_size=0.2, random_state=42)

# Train the Random Forest model for market price prediction
market_model = RandomForestRegressor(random_state=42)
market_model.fit(X_train_market, y_train_market)

# Predict market price using the trained model
def predict_market_price(demand, supply, competitor_price, economic_indicator, weather_impact):
    prediction = market_model.predict([[demand, supply, competitor_price, economic_indicator, weather_impact]])[0]
    return prediction

# Evaluate the model on test data
y_pred_market = market_model.predict(X_test_market)
mse_market = mean_squared_error(y_test_market, y_pred_market)
print(f"Market Dataset Model MSE: {mse_market}")

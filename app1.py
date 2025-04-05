import streamlit as st
from crewai_manager import SustainableFarmingAI
from database.save_results import save_recommendation, get_saved_recommendations
from models.ml_model1 import predict_crop_yield, predict_market_price

# Initialize AI system
ai_system = SustainableFarmingAI(r"D:\v3\farmer_advisor_dataset.csv", r"D:\v3\market_researcher_dataset.csv")

# Sidebar for navigation
st.sidebar.title("🌿 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Prediction", "Agentic Recommendation"])

# --- Home Section ---
if section == "Home":
    st.title("🌱 AI-Powered Sustainable Farming")
    st.header("🚜 Welcome to the Future of Agriculture!")
    st.write("👉 This section will contain an overview of the project, features, and goals. (To be updated)")
    st.info("Use the sidebar to switch between Prediction and Agentic Recommendation.")

# --- Prediction Section ---
elif section == "Prediction":
    st.title("🔍 Smart Predictions for Farmers")

    st.subheader("🌾 Crop Yield Prediction")
    soil_pH = st.number_input("Soil pH", min_value=3.0, max_value=10.0, value=6.5)
    moisture = st.number_input("Soil Moisture (%)", min_value=0.0, max_value=100.0, value=30.0)
    temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=100.0)
    fertilizer = st.number_input("Fertilizer Usage (kg)", min_value=0.0, max_value=100.0, value=50.0)

    if st.button("📈 Predict Crop Yield"):
        yield_prediction = predict_crop_yield(soil_pH, moisture, temperature, rainfall, fertilizer)
        st.success(f"📊 Predicted Crop Yield: {yield_prediction:.2f} tons per hectare")

    st.markdown("---")

    st.subheader("📊 Market Price Prediction")
    demand_index = st.number_input("Demand Index", min_value=0.0, max_value=1.0, value=0.5)
    supply_index = st.number_input("Supply Index", min_value=0.0, max_value=1.0, value=0.5)
    competitor_price = st.number_input("Competitor Price per Ton ($)", min_value=0.0, max_value=5000.0, value=1000.0)
    economic_indicator = st.number_input("Economic Indicator", min_value=0.0, max_value=1.0, value=0.5)
    weather_impact = st.number_input("Weather Impact Score", min_value=0.0, max_value=1.0, value=0.5)

    if st.button("💰 Predict Market Price"):
        market_price_prediction = predict_market_price(demand_index, supply_index, competitor_price, economic_indicator, weather_impact)
        st.success(f"💲 Predicted Market Price: ${market_price_prediction:.2f} per ton")

# --- Agentic Recommendation Section ---
elif section == "Agentic Recommendation":
    st.title("🤖 Agentic Farming Recommendations")

    prompt = st.text_area("Enter your query for AI insights:")

    if st.button("Get AI Recommendation"):
        if prompt:
            results = ai_system.get_recommendation(prompt)
            save_recommendation(prompt, results["Farm Recommendation"], results["Market Recommendation"])

            st.subheader("🌿 Farm Advisor's Recommendation")
            st.write(results["Farm Recommendation"])

            st.subheader("📈 Market Researcher's Recommendation")
            st.write(results["Market Recommendation"])
        else:
            st.warning("Please enter a query.")

    st.subheader("📚 View Past Recommendations")
    saved_data = get_saved_recommendations()

    if saved_data:
        for row in saved_data:
            st.write(f"🔹 **Prompt:** {row[1]}")
            st.write(f"🌱 **Farm Advice:** {row[2]}")
            st.write(f"📊 **Market Advice:** {row[3]}")
            st.markdown("---")
    else:
        st.write("No saved recommendations yet.")

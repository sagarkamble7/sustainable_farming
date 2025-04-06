import streamlit as st
import pandas as pd
from crewai_manager import SustainableFarmingAI
from database.save_results import (
    save_recommendation, 
    get_saved_recommendations, 
    get_recommendation_summary,
    get_recommendation_by_id,
    extract_key_metrics
)
from models.ml_model1 import predict_crop_yield, predict_market_price

# Initialize AI system
ai_system = SustainableFarmingAI(r"C:\Users\USER\OneDrive\Desktop\Farmer_advisor_agentic_ai\farmer_advisor_dataset.csv", r"C:\Users\USER\OneDrive\Desktop\Farmer_advisor_agentic_ai\market_researcher_dataset.csv")

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
    
    tab1, tab2 = st.tabs(["Get Recommendation", "View Past Recommendations"])
    
    with tab1:
        prompt = st.text_area("Enter your query for AI insights:")
        
        if st.button("Get AI Recommendation"):
            if prompt:
                with st.spinner("Generating AI recommendations..."):
                    results = ai_system.get_recommendation(prompt)
                    
                    # Save the recommendation
                    save_recommendation(prompt, results["Farm Recommendation"], results["Market Recommendation"])
                    
                    # Display full recommendations to the user
                    st.subheader("🌿 Farm Advisor's Recommendation")
                    st.write(results["Farm Recommendation"])
                    
                    st.subheader("📈 Market Researcher's Recommendation")
                    st.write(results["Market Recommendation"])
                    
                    st.success("Recommendation saved! View it in the Past Recommendations tab.")
            else:
                st.warning("Please enter a query.")
    
    with tab2:
        st.subheader("📊 Recommendation Summary Table")
        
        # Get recommendation summaries
        summary_data = get_recommendation_summary()
        
        if summary_data:
            # Create a DataFrame for better display
            df = pd.DataFrame(
                summary_data,
                columns=["ID", "Query", "Farm Metrics", "Market Metrics"]
            )
            
            # Show the table with summaries
            st.dataframe(df, use_container_width=True)
            
            # Option to view detailed recommendation
            col1, col2 = st.columns([1, 2])
            
            with col1:
                recommendation_id = st.number_input(
                    "Recommendation ID", 
                    min_value=1, 
                    max_value=max([row[0] for row in summary_data]) if summary_data else 1,
                    step=1
                )
                
                view_button = st.button("View Full Details")
            
            if view_button:
                full_rec = get_recommendation_by_id(recommendation_id)
                if full_rec:
                    st.subheader(f"Full Recommendation #{full_rec[0]}")
                    
                    st.write("**Original Query:**")
                    st.info(full_rec[1])
                    
                    st.write("**Farm Advisor's Recommendation:**")
                    st.success(full_rec[2])
                    
                    st.write("**Market Researcher's Recommendation:**")
                    st.success(full_rec[3])
                else:
                    st.error("Recommendation not found.")
        else:
            st.info("No recommendations saved yet. Generate some recommendations first!")
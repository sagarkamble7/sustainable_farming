import streamlit as st
import pandas as pd
from PIL import Image
from crewai_manager import SustainableFarmingAI
from database.save_results import (
    save_recommendation, 
    get_saved_recommendations, 
    get_recommendation_summary,
    get_recommendation_by_id,
    extract_key_metrics
)
from models.ml_model1 import predict_crop_yield, predict_market_price

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subheader {
        font-size: 1.5rem !important;
        font-weight: 600;
        color: #3a7e6f;
        margin-top: 1rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .feature-title {
        color: #2E8B57;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .feature-desc {
        color: #444;
        font-size: 0.9rem;
    }
    .cta-section {
        background-color: #f0f7f3;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin-top: 2rem;
        border-left: 5px solid #2E8B57;
    }
    .mission-statement {
        background-color: #f5f9f7;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        border-bottom: 3px solid #2E8B57;
    }
    .mission-title {
        color: #2E8B57;
    }
    .mission-text {
        font-size: 18px;
        line-height: 1.6;
        color: #444;
    }
    .testimonial {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        height: 100%;
        border-left: 3px solid #2E8B57;
    }
    .testimonial-text {
        font-style: italic;
        color: #444;
    }
    .testimonial-author {
        text-align: right;
        font-weight: bold;
        color: #2E8B57;
    }
</style>
""", unsafe_allow_html=True)

# Initialize AI system
ai_system = SustainableFarmingAI(r"farmer_advisor_dataset.csv", r"market_researcher_dataset.csv")

# Sidebar for navigation
st.sidebar.title("🌿 Navigation")
section = st.sidebar.radio("Go to", ["Home", "Prediction", "Agentic Recommendation"])

# --- Home Section ---
if section == "Home":
    # Main header
    st.markdown("<h1 class='main-header'>🌱 AI-Powered Sustainable Farming</h1>", unsafe_allow_html=True)
    
    # Banner image
    try:
        banner = Image.open("images/banner.jpg")
        st.image(banner, use_column_width=True, caption="Empowering farmers through AI and data science")
    except Exception as e:
        st.error(f"Could not load banner image. Please check the path: images/banner.jpg")
    
    # Welcome message and mission statement
    st.markdown("""
    <div class="mission-statement">
        <h3 class="mission-title">Our Mission</h3>
        <p class="mission-text">
            Empowering farmers with cutting-edge <b>Artificial Intelligence</b> to make data-driven decisions for 
            sustainable, profitable, and environmentally friendly agriculture.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features section
    st.markdown("<h2 class='subheader'>🚀 Key Features</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        try:
            st.image("images/crop_yield.jpg", width=150)
            st.markdown("<p class='feature-title'>📈 Crop Yield Prediction</p>", unsafe_allow_html=True)
            st.markdown("<p class='feature-desc'>Use AI to predict crop yields based on soil conditions, weather patterns, and fertilizer usage for optimal planning.</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load image. Please check the path: images/crop_yield.jpg")
    
    with col2:
        try:
            st.image("images/market_price.jpg", width=150)
            st.markdown("<p class='feature-title'>💹 Market Price Estimation</p>", unsafe_allow_html=True)
            st.markdown("<p class='feature-desc'>Get accurate market price forecasts to help you make informed selling decisions and maximize profits.</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load image. Please check the path: images/market_price.jpg")
    
    with col3:
        try:
            st.image("images/recommendation.jpg", width=150)
            st.markdown("<p class='feature-title'>🤖 AI Recommendations</p>", unsafe_allow_html=True)
            st.markdown("<p class='feature-desc'>Receive personalized farming and market strategies from your AI advisor to optimize your agricultural operations.</p>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not load image. Please check the path: images/recommendation.jpg")
    
    # Call to action section
    st.markdown("""
    <div class='cta-section'>
        <h2 style='color: #2E8B57; margin-bottom: 15px;'>🌾 Ready to Revolutionize Your Farm?</h2>
        <p style='font-size: 18px; margin-bottom: 20px; color: #444;'>Use the sidebar to explore our prediction tools and get personalized AI recommendations.</p>
        <p style='color: #2E8B57; font-weight: bold; font-size: 20px;'>Let's make agriculture smarter together!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("<h2 class='subheader' style='margin-top: 2rem;'>💬 Success Stories</h2>", unsafe_allow_html=True)
    
    testimonial_col1, testimonial_col2 = st.columns(2)
    
    with testimonial_col1:
        st.markdown("""
        <div class="testimonial">
            <p class="testimonial-text">"Sustainable Farming AI helped me increase my crop yield by 30% while reducing fertilizer usage. The predictions were spot on!"</p>
            <p class="testimonial-author">- John Smith, Wheat Farmer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with testimonial_col2:
        st.markdown("""
        <div class="testimonial">
            <p class="testimonial-text">"The market price predictions helped me time my sales perfectly. I've seen a 25% increase in profits since using this platform."</p>
            <p class="testimonial-author">- Maria Garcia, Organic Farm Owner</p>
        </div>
        """, unsafe_allow_html=True)

# --- Prediction Section --- (Keeping this exactly the same)
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

# --- Agentic Recommendation Section --- (Keeping this exactly the same)
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

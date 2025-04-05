import streamlit as st
from crewai_manager import SustainableFarmingAI
from database.save_results import save_recommendation, get_saved_recommendations

# Initialize AI System
ai_system = SustainableFarmingAI("farmer_advisor_dataset.csv", "market_researcher_dataset.csv")

st.title("🌱 AI-Powered Sustainable Farming")

# User Prompt
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

# Display Saved Recommendations
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

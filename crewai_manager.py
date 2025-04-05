from agents.farmer_advisor import FarmerAdvisor
from agents.market_researcher import MarketResearcher

class SustainableFarmingAI:
    def __init__(self, farm_data_path, market_data_path):
        self.farmer_agent = FarmerAdvisor(farm_data_path)
        self.market_agent = MarketResearcher(market_data_path)

    def get_recommendation(self, prompt):
        farm_recommendation = self.farmer_agent.analyze_data(prompt)
        market_recommendation = self.market_agent.analyze_data(prompt)

        return {
            "User Prompt": prompt,
            "Farm Recommendation": farm_recommendation,
            "Market Recommendation": market_recommendation
        }

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from models.ollama_inference import generate_response

class MarketResearcher:
    def __init__(self, dataset_path):
        self.dataset = pd.read_csv(dataset_path)

    def analyze_data(self, prompt):
        sample_data = self.dataset.head(3).to_dict(orient="records")  # Use sample data
        query = f"""
        Given this market data:
        {sample_data}

        User query: {prompt}

        Generate an AI-powered recommendation based on market trends.
        """
        return generate_response(query)

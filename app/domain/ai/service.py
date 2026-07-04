import os
import openai
from typing import List, Dict

# In a commercial app, keys are securely injected per tenant
openai.api_key = os.getenv("OPENAI_API_KEY")

class AIService:
    @staticmethod
    async def generate_repair_notes(raw_technician_input: str) -> str:
        """
        Transforms messy, shorthand technician notes into a professional
        customer-facing summary.
        """
        try:
            prompt = f"Rewrite these technician notes into a polite, professional summary for a customer invoice. Do not invent facts: {raw_technician_input}"
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a professional repair shop assistant."},
                          {"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to original text if AI service fails
            return raw_technician_input

    @staticmethod
    def predict_inventory_shortage(sales_history: List[Dict]) -> List[str]:
        """
        Stub for time-series forecasting (e.g., using Prophet or simple moving averages)
        to predict which SKUs will run out in the next 14 days based on seasonal trends.
        """
        # Logic to analyze velocity and return high-risk SKUs
        return ["SKU-IP13P-DSP", "SKU-S22-BATT"]

"""
Compliance guardrail layer
"""

from openai import OpenAI
from src.config import Config

# Initialize OpenAI client with the new API format
client = OpenAI(api_key=Config.OPENAI_API_KEY)

def classify_message(message):
    prompt = f"""
    Classify the following message for compliance in investor communications.
    Check for: performance claims without disclaimers, misleading language, investment advice without qualification, over-promising returns, words like "guaranteed", "assured returns", "risk-free", "double your money".

    Message: {message}

    Respond with only one word: Approved, Requires Review, or Rejected.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    classification = response.choices[0].message.content.strip()
    return classification
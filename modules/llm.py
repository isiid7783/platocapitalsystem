import requests
from config import OLLAMA_URL, MODEL_NAME

def generate_analysis(metrics):
    summary = f"""
Average Return: {metrics['avg_return']:.2f}
Success Rate: {metrics['success_rate']:.2f}
Confidence Correlation: {metrics['confidence_corr']:.2f}
Time Correlation: {metrics['time_corr']:.2f}
"""

    prompt = f"""
Provide strategic capital allocation insight.
Identify structural bias, overconfidence risk,
and time inefficiency.

{summary}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=60
        )

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "LLM connection failed."

    except:
        return "LLM connection error."
        

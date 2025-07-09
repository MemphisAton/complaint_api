import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("APILAYER_KEY")

API_URL = "https://api.apilayer.com/sentiment/analysis"


async def get_sentiment(text: str) -> str:
    """Отправляет текст в APILayer для анализа тональности и возвращает: positive, negative или neutral."""

    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("sentiment", "unknown")
    except Exception:
        return "unknown"

import requests
import os
from dotenv import load_dotenv

load_dotenv()
PROFANITY_API_KEY = os.getenv("PROFANITY_API_KEY")  # можно переименовать переменную в .env тоже

def clean_profanity(text: str) -> str:
    """Возвращает текст с заменённой нецензурной лексикой (если есть)."""

    url = "https://api.api-ninjas.com/v1/profanityfilter"
    headers = {"X-Api-Key": PROFANITY_API_KEY}
    params = {"text": text}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("censored", text)
    except Exception:
        return text

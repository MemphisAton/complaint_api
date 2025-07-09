import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def classify_text(text: str) -> str:
    """Определяет категорию жалобы (техническая, оплата или другое) с помощью OpenAI, возвращает результат или 'другое' при ошибке."""

    prompt = (
        f"Определи категорию этой жалобы: \"{text}\"\n"
        f"Варианты: техническая, оплата, другое.\n"
        f"Ответь одним словом, без точек и пояснений."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10,
        )

        category = response.choices[0].message.content.strip().lower()

        if category in ["техническая", "оплата"]:
            return category
        return "другое"

    except Exception:
        return "другое"

from google import genai
from config import GEMINI_MODEL

def ask_gemini(messages: list[dict]) -> str:
    client = genai.Client()  # ключ берётся из ENV: GEMINI_API_KEY

    # склеиваем историю в текст
    parts = []
    for m in messages:
        role = m["role"].upper()
        parts.append(f"[{role}]\n{m['content']}")

    prompt = "\n\n".join(parts)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini вернул пустой ответ")

    return response.text.strip()

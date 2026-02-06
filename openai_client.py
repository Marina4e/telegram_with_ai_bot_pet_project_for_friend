from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_FALLBACK_MODEL, FAKE_MODE
from gemini_client import ask_gemini


def _fake_answer(messages: list[dict]) -> str:
    last_user = ""
    for m in reversed(messages):
        if m["role"] == "user":
            last_user = m["content"]
            break
    return (
        "🤖 Режим тестування\n\n"
        "AI зараз вимкнений.\n"
        "Усі кнопки та команди працюють.\n\n"
        "Текст повідомлення:\n"
        f"“{last_user}”"
    )


def ask_openai(messages: list[dict]) -> str:
    print(">>> ask_openai CALLED, FAKE_MODE =", FAKE_MODE)

    if FAKE_MODE:
        return _fake_answer(messages)

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY не заданий у .env")

    client = OpenAI(api_key=OPENAI_API_KEY)

    # 🔥 ВАЖНО: превращаем messages в текст
    parts = []
    for m in messages:
        role = m["role"].upper()
        parts.append(f"[{role}]\n{m['content']}")

    prompt = "\n\n".join(parts)

    try:
        response = client.responses.create(
            model=OPENAI_MODEL,
            input=prompt
        )
        return response.output_text.strip()

    except Exception as e:

        if OPENAI_FALLBACK_MODEL.lower() == "gemini":
            try:
                return ask_gemini(messages)
            except Exception as ge:
                raise RuntimeError(
                    f"OpenAI впав, Gemini теж не відповів.\n"
                    f"OpenAI error: {e}\n"
                    f"Gemini error: {ge}"
                )

        try:
            response = client.responses.create(
                model=OPENAI_FALLBACK_MODEL,
                input=prompt
            )
            return response.output_text.strip()

        except Exception as e2:
            raise RuntimeError(
                f"Не вдалося викликати OpenAI.\n"
                f"Основна модель: {OPENAI_MODEL}\n"
                f"Fallback: {OPENAI_FALLBACK_MODEL}\n\n"
                f"Помилка 1: {e}\n"
                f"Помилка 2: {e2}"
            )

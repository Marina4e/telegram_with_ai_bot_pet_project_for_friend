import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Главная модель
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

# Фолбэк модель (если главная недоступна)
OPENAI_FALLBACK_MODEL = os.getenv(
    "OPENAI_FALLBACK_MODEL",
    "gemini"
).strip().lower()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3-flash-preview"
).strip()


# Включить фейковый режим (без API) — удобно для тестов
FAKE_MODE = os.getenv("FAKE_MODE", "0").strip().lower() == "1"

SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "Ти корисний асистент. Відповідай коротко, чітко і по суті."
).strip()

# Сколько сообщений хранить в истории
HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", "20"))

# Ограничение на длину сообщения
MAX_USER_CHARS = int(os.getenv("MAX_USER_CHARS", "3000"))


print("FAKE_MODE =", FAKE_MODE)
print("GEMINI_API_KEY =", bool(os.getenv("GEMINI_API_KEY")))
print("=== CONFIG DEBUG ===")
print("FAKE_MODE raw:", os.getenv("FAKE_MODE"))
print("FAKE_MODE parsed:", FAKE_MODE)
print("OPENAI_API_KEY exists:", bool(OPENAI_API_KEY))
print("====================")

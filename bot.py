import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from config import TELEGRAM_BOT_TOKEN, HISTORY_LIMIT, MAX_USER_CHARS
from openai_client import ask_openai
from security import is_allowed
from db import (
    init_db,
    add_message,
    get_history,
    clear_history,
    export_history_text,
    init_settings_table,
    get_user_settings,
    set_user_mode,
    set_user_system_prompt,
    reset_user_system_prompt,
)
print("BOT FILE:", __file__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- Кнопки меню ---
BTN_START  = "🏁Start"
BTN_HELP   = "ℹ️Help"
BTN_WHOAMI = "🆔 ID"
BTN_RESET  = "🔄Reset"
BTN_EXPORT = "📄Export"
BTN_SYSTEM        = "🧾Set prompt"
BTN_SYSTEM_SHOW   = "👁Prompt"
BTN_SYSTEM_RESET  = "♻️Reset prompt"



def main_menu_keyboard(mode: str = "short"):
    mode_btn = "🧠 Подробно" if mode == "long" else "🧠 Коротко"

    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🏁Start"), KeyboardButton("ℹ️Help"), KeyboardButton("🆔 ID")],
            [KeyboardButton("🔄Reset"), KeyboardButton("📄Export"), KeyboardButton(mode_btn)],
            # [KeyboardButton(mode_btn)],
            [KeyboardButton("👁Prompt"), KeyboardButton("♻️Reset prompt"), KeyboardButton("🧾Set prompt")],
            # [KeyboardButton("🧾Set prompt")],
        ],
        resize_keyboard=True
    )

def _deny_text() -> str:
    return (
        "⛔ Вибач, цей бот приватний.\n"
        "Ти не маєш доступу."
    )

def _get_menu_for_user(user_id: int):
    settings = get_user_settings(user_id)
    return main_menu_keyboard(settings["mode"])


# ---------------- COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    await update.message.reply_text(
        "Привіт! 👋\n"
        "Я Telegram-бот з GPT + памʼять (SQLite).\n\n"
        "Можеш писати повідомлення або користуватись кнопками нижче 🙂",
        reply_markup=_get_menu_for_user(user_id)
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    await update.message.reply_text(
        "ℹ️ Команди:\n"
        "/start — старт\n"
        "/reset — очистити памʼять\n"
        "/export — експорт історії в txt\n"
        "/whoami — показати твій Telegram ID\n"
        "/system — змінити system prompt\n"
        "/system_show — показати system prompt\n"
        "/system_reset — скинути system prompt\n"
        "/help — допомога\n\n"
        "Також можна користуватись кнопками 🙂",
        reply_markup=_get_menu_for_user(user_id)
    )


async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    await update.message.reply_text(
        f"🆔 Твій Telegram ID: {user_id}\n\n"
        "Як зробити бота приватним:\n"
        "1) відкрий .env\n"
        "2) впиши ALLOWED_USER_ID=ТВІЙ_ID",
        reply_markup=_get_menu_for_user(user_id)
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    clear_history(user_id)

    await update.message.reply_text(
        "✅ Памʼять очищено. Починаємо з нуля 🙂",
        reply_markup=_get_menu_for_user(user_id)
    )


async def export_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    text = export_history_text(user_id, limit=300)

    if not text.strip():
        await update.message.reply_text(
            "📭 Історія порожня — нема що експортувати.",
            reply_markup=_get_menu_for_user(user_id)
        )
        return

    filename = f"history_{user_id}.txt"
    filepath = filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    await update.message.reply_document(
        document=open(filepath, "rb"),
        filename=filename,
        caption="📄 Ось твоя історія чату (txt)",
        reply_markup=_get_menu_for_user(user_id)
    )

    # удаляем файл после отправки
    try:
        os.remove(filepath)
    except Exception:
        pass

async def system_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    text = update.message.text or ""
    parts = text.split(" ", 1)

    if len(parts) < 2 or not parts[1].strip():
        await update.message.reply_text(
            "✍️ Напиши так:\n"
            "/system Твій новий system prompt",
            reply_markup=_get_menu_for_user(user_id)
        )
        return

    new_prompt = parts[1].strip()
    set_user_system_prompt(user_id, new_prompt)

    await update.message.reply_text(
        "✅ System prompt оновлено!",
        reply_markup=_get_menu_for_user(user_id)
    )


async def system_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    settings = get_user_settings(user_id)

    await update.message.reply_text(
        "🧾 Поточний system prompt:\n\n"
        f"{settings['system_prompt']}",
        reply_markup=_get_menu_for_user(user_id)
    )


async def system_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    reset_user_system_prompt(user_id)

    await update.message.reply_text(
        "♻️ System prompt скинуто до стандартного (з .env).",
        reply_markup=_get_menu_for_user(user_id)
    )


# ---------------- CHAT HANDLER ----------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text(_deny_text())
        return

    user_text = (update.message.text or "").strip()
    if not user_text:
        return

    # --- кнопки как команды ---
    if user_text == BTN_RESET:
        await reset(update, context)
        return

    if user_text == BTN_EXPORT:
        await export_history(update, context)
        return

    if user_text == BTN_HELP:
        await help_command(update, context)
        return

    if user_text == BTN_WHOAMI:
        await whoami(update, context)
        return

    if user_text == BTN_START:
        await start(update, context)
        return

    if user_text == BTN_SYSTEM_SHOW:
        await system_show(update, context)
        return

    if user_text == BTN_SYSTEM_RESET:
        await system_reset(update, context)
        return

    if user_text == BTN_SYSTEM:
        await update.message.reply_text(
            "✍️ Напиши так:\n"
            "/system Твій новий system prompt\n\n"
            "Приклад:\n"
            "/system Ти викладач. Пояснюй простими словами.",
            reply_markup=_get_menu_for_user(user_id)
        )
        return

    # --- настройки пользователя ---
    settings = get_user_settings(user_id)
    mode = settings["mode"]
    user_system_prompt = settings["system_prompt"]

    # --- переключение режима ---
    if user_text in ["🧠 Коротко", "🧠 Подробно"]:
        if mode == "short":
            set_user_mode(user_id, "long")
            await update.message.reply_text(
                "✅ Увімкнено режим: ПОДРОБНО 🙂",
                reply_markup=main_menu_keyboard("long")
            )
        else:
            set_user_mode(user_id, "short")
            await update.message.reply_text(
                "✅ Увімкнено режим: КОРОТКО 🙂",
                reply_markup=main_menu_keyboard("short")
            )
        return

    # --- обычный чат ---
    if len(user_text) > MAX_USER_CHARS:
        await update.message.reply_text(
            f"⚠️ Повідомлення занадто довге ({len(user_text)} символів).\n"
            f"Спробуй скоротити до {MAX_USER_CHARS} символів.",
            reply_markup=_get_menu_for_user(user_id)
        )
        return

    add_message(user_id, "user", user_text)

    history = get_history(user_id, limit=HISTORY_LIMIT)

    # подсказка для режима
    if mode == "short":
        mode_hint = "\n\nВідповідай максимально коротко."
    else:
        mode_hint = "\n\nВідповідай максимально детально, з прикладами."

    messages = [{"role": "system", "content": user_system_prompt + mode_hint}] + history

    await update.message.chat.send_action(action=ChatAction.TYPING)

    try:
        answer = ask_openai(messages)
    except Exception as e:
        await update.message.reply_text(
            f"❌ Помилка при запиті:\n{e}",
            reply_markup=_get_menu_for_user(user_id)
        )
        return

    add_message(user_id, "assistant", answer)

    await update.message.reply_text(
        answer,
        reply_markup=_get_menu_for_user(user_id)
    )


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN не заданий. Додай його в .env")

    init_db()
    init_settings_table()

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(CommandHandler("export", export_history))

    app.add_handler(CommandHandler("system", system_command))
    app.add_handler(CommandHandler("system_show", system_show))
    app.add_handler(CommandHandler("system_reset", system_reset))

    # чат
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("🤖 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()

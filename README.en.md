# Telegram GPT Bot (SQLite Memory)

This is a simple Telegram bot that works as a chat with an OpenAI model through the API. The bot supports:

* conversation memory (SQLite)
* button menu
* history export to `.txt`
* response mode: short / detailed
* changing the system prompt directly in Telegram

## 1) Install Python

Python 3.10 or newer is required.

Download it from the official website:
https://www.python.org/downloads/

During installation, check the box:
✅ Add Python to PATH

## 2) Create a Telegram Bot (BotFather)

In Telegram, find the bot `@BotFather`.

Write the command:

Enter the bot name (any name).

Enter the bot username (it must end with `bot`). For example: `/newbot`

Enter the bot name (any name).

Enter the bot username (it must end with `_bot`). For example: `my_gpt_helper_bot`

BotFather will provide a token in this form:

`1234567890:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

👉 This is the `TELEGRAM_BOT_TOKEN`.

## 3) Download the Project and Open the Folder

Extract the project into a folder, for example:

`telegram-gpt-bot/`

Open the terminal specifically in this folder.

## 4) Create the `.env` File

The project contains the file:

`.env.example`

Create a copy and name it:

`.env`

Or create the `.env` file manually.

## 5) Fill In the `.env` File

Open `.env` and paste:

```env
TELEGRAM_BOT_TOKEN=YOUR_TOKEN_FROM_BOTFATHER_HERE
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE

OPENAI_MODEL=gpt-5-nano
OPENAI_FALLBACK_MODEL=gpt-4o-mini

FAKE_MODE=0

# If you want the bot to work only for 1 person:
# (enter your Telegram ID)
ALLOWED_USER_ID=
```

<img width="300" height="255" alt="Знімок екрана 2026-02-05 220420" src="https://github.com/user-attachments/assets/7dc9cbc7-569b-4ee2-b810-4b0ade233e3b" />

 
## 6) How to Find Out Your Telegram ID for Private Mode

Start the bot.

Write the command:

```text
/whoami
```

The bot will show your Telegram ID.

Insert it into `.env`:

```env
ALLOWED_USER_ID=123456789
```

If `ALLOWED_USER_ID` is empty, the bot will be available to everyone.

## 7) Install the Libraries

In the terminal, inside the project folder, enter:

```bash
pip install -r requirements.txt
```

## 8) Start the Bot

```bash
python bot.py
```

If everything is fine, the bot will start working.

## 9) How to Use the Bot

Simply write messages in Telegram.

A button menu is also available:

🔄 Clear Memory

📄 Export History

🧠 Mode: short/detailed

ℹ️ Help

🆔 My ID

## Commands

`/start` — start

`/help` — help

`/reset` — clear memory (SQLite)

`/export` — export history to `.txt`

`/whoami` — show Telegram ID

`/system ...` — change the system prompt

`/system_show` — show the system prompt

`/system_reset` — reset the system prompt to the default one

## Note About How the Bot Works

This bot works in polling mode.

This means:

* the bot works only when `python bot.py` is running
* if you close the laptop/computer, the bot will stop responding
* for the bot to work 24/7, it must be hosted on a server

## Where the Memory Is Stored

The memory, including chat history and settings, is stored in the file:

`chat.db`

## Typical Problems

### ❌ No module named 'openai'

Run:

```bash
pip install -r requirements.txt
```

### ❌ The Bot Does Not Respond

Check:

* whether `TELEGRAM_BOT_TOKEN` is correct
* whether `python bot.py` is running
* whether there are any errors in the terminal

### ❌ `model_not_found` Error

This means that the API key does not have access to the model.

Try setting the following in `.env`:

```env
OPENAI_MODEL=gpt-5-nano
OPENAI_FALLBACK_MODEL=gpt-4o-mini
```

Author:
https://github.com/Marina4e/telegram_gpt_bot_26

The project was built as a simple educational Telegram GPT bot with memory.

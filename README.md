
# Telegram GPT Bot (SQLite memory)

Це простий Telegram-бот, який працює як чат з моделлю OpenAI через API.
Бот підтримує:
- памʼять діалогу (SQLite)
- кнопочне меню
- експорт історії в .txt
- режим відповідей: коротко / детально
- зміну system prompt прямо в Telegram

---

## 1) Встанови Python
Потрібен Python **3.10 або новіший**.

Завантаж з офіційного сайту:
https://www.python.org/downloads/

Під час встановлення постав галочку:
✅ **Add Python to PATH**

---

## 2) Створи Telegram-бота (BotFather)

1. В Telegram знайди бота **@BotFather**
2. Напиши команду:
3. Введи назву бота (будь-яку)
4. Введи username бота (має закінчуватись на `bot`)
Наприклад:
/newbot
4. Введи назву бота (будь-яку)
5. Введи username бота (має закінчуватись на `_bot`)
Наприклад:
my_gpt_helper_bot 
6. BotFather видасть токен виду:1234567890:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

👉 Це і є `TELEGRAM_BOT_TOKEN`

---

## 3) Завантаж проект і відкрий папку

Розпакуй проект у папку, наприклад: telegram-gpt-bot/

Відкрий термінал саме у цій папці.

---

## 4) Створи файл .env

У проекті є файл:
- `.env.example`

Створи копію і назви її:
- `.env`

Або створи `.env` вручну.

---

## 5) Заповни .env

Відкрий `.env` і встав:

```env
TELEGRAM_BOT_TOKEN=ТУТ_ТВІЙ_ТОКЕН_З_BOTFATHER
OPENAI_API_KEY=ТУТ_ТВІЙ_OPENAI_API_KEY

OPENAI_MODEL=gpt-5-nano
OPENAI_FALLBACK_MODEL=gpt-4o-mini

FAKE_MODE=0

# Якщо хочеш, щоб бот працював тільки для 1 людини:
# (впиши свій Telegram ID)
ALLOWED_USER_ID= 
```
6) Як дізнатись свій Telegram ID (для приватного режиму)

Запусти бота

Напиши команду:

/whoami


Бот покаже твій Telegram ID

Встав його в .env:

ALLOWED_USER_ID=123456789


Якщо ALLOWED_USER_ID порожній — бот буде доступний для всіх.
7) Встанови бібліотеки

У терміналі (в папці проекту) введи:

pip install -r requirements.txt

8) Запусти бота
python bot.py


Якщо все добре — бот почне працювати.

9) Як користуватись ботом

Просто пиши повідомлення у Telegram.

Також доступне меню-кнопки:

🔄 Очистити памʼять

📄 Експорт історії

🧠 Режим: коротко/подробно

ℹ️ Допомога

🆔 Мій ID

Команди

/start — старт

/help — допомога

/reset — очистити памʼять (SQLite)

/export — експорт історії в .txt

/whoami — показати Telegram ID

/system ... — змінити system prompt

/system_show — показати system prompt

/system_reset — скинути system prompt до стандартного

Примітка про роботу бота

Цей бот працює у режимі polling.

<img width="300" height="255" alt="Знімок екрана 2026-02-05 220420" src="https://github.com/user-attachments/assets/7dc9cbc7-569b-4ee2-b810-4b0ade233e3b" />

Це означає:

бот працює тільки тоді, коли запущений python bot.py

якщо закрити ноутбук/компʼютер — бот перестане відповідати

щоб бот працював 24/7 — потрібно хостити його на сервері

Де зберігається памʼять

Памʼять (історія чату + налаштування) зберігається у файлі:

chat.db

Типові проблеми
❌ No module named 'openai'

Запусти:

pip install -r requirements.txt

❌ Bot не відповідає

Перевір:

правильність TELEGRAM_BOT_TOKEN

чи запущений python bot.py

чи немає помилок у терміналі

❌ Помилка model_not_found

Це означає, що у ключа немає доступу до моделі.
Спробуй у .env поставити:

OPENAI_MODEL=gpt-5-nano
OPENAI_FALLBACK_MODEL=gpt-4o-mini

Автор: https://github.com/Marina4e/telegram_gpt_bot_26

Проект зібраний як простий навчальний Telegram GPT bot з памʼяттю.

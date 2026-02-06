import sqlite3
from datetime import datetime

DB_NAME = "chat_memory.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def add_message(user_id: int, role: str, content: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO messages (user_id, role, content, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, role, content, datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()


def get_history(user_id: int, limit: int = 20):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT role, content
        FROM messages
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))

    rows = cur.fetchall()
    conn.close()

    rows.reverse()
    return [{"role": role, "content": content} for role, content in rows]


def clear_history(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def export_history_text(user_id: int, limit: int = 200) -> str:
    history = get_history(user_id, limit=limit)

    lines = []
    for msg in history:
        role = msg["role"]
        text = msg["content"]

        if role == "user":
            prefix = "👤 USER"
        elif role == "assistant":
            prefix = "🤖 GPT"
        else:
            prefix = role.upper()

        lines.append(f"{prefix}: {text}")

    return "\n\n".join(lines)


import sqlite3
from config import SYSTEM_PROMPT


def init_settings_table():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            system_prompt TEXT,
            mode TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_user_settings(user_id: int) -> dict:
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT system_prompt, mode FROM user_settings WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()

    conn.close()

    if not row:
        return {
            "system_prompt": SYSTEM_PROMPT,
            "mode": "short"
        }

    system_prompt, mode = row

    return {
        "system_prompt": system_prompt or SYSTEM_PROMPT,
        "mode": mode or "short"
    }


def set_user_system_prompt(user_id: int, prompt: str):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_settings (user_id, system_prompt, mode)
        VALUES (?, ?, 'short')
        ON CONFLICT(user_id) DO UPDATE SET system_prompt=excluded.system_prompt
    """, (user_id, prompt))

    conn.commit()
    conn.close()


def set_user_mode(user_id: int, mode: str):
    if mode not in ("short", "long"):
        mode = "short"

    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_settings (user_id, system_prompt, mode)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET mode=excluded.mode
    """, (user_id, SYSTEM_PROMPT, mode))

    conn.commit()
    conn.close()


def reset_user_system_prompt(user_id: int):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_settings (user_id, system_prompt, mode)
        VALUES (?, ?, 'short')
        ON CONFLICT(user_id) DO UPDATE SET system_prompt=excluded.system_prompt
    """, (user_id, SYSTEM_PROMPT))

    conn.commit()
    conn.close()

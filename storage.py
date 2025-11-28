import sqlite3
import os

DB_PATH = "/app/data/data.db"


def init_db():
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            image_path TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_drafts(drafts):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Clear old drafts (optional)
    c.execute("DELETE FROM drafts")

    for d in drafts:
        c.execute("INSERT INTO drafts (text, image_path) VALUES (?, ?)", (d["text"], d["image_path"]))

    conn.commit()
    conn.close()


def list_drafts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, text, image_path FROM drafts")
    rows = c.fetchall()
    conn.close()

    return [{"id": r[0], "text": r[1], "image_path": r[2]} for r in rows]


def delete_draft(draft_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))
    conn.commit()
    conn.close()

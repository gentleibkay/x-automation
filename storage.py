import sqlite3
import os

DB_PATH = "/app/data/data.db"   # shared disk location


def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            image_path TEXT,
            created_at TEXT,
            approved INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()


def save_drafts(drafts):
    conn = get_db()
    for d in drafts:
        conn.execute("""
            INSERT INTO drafts (text, image_path, created_at, approved)
            VALUES (?, ?, ?, 0)
        """, (d["text"], d["image_path"], d["created_at"]))
    conn.commit()
    conn.close()


def list_drafts():
    conn = get_db()
    rows = conn.execute("SELECT * FROM drafts WHERE approved = 0").fetchall()
    conn.close()
    return rows


def approve_draft(draft_id):
    conn = get_db()
    conn.execute("UPDATE drafts SET approved = 1 WHERE id = ?", (draft_id,))
    conn.commit()
    conn.close()


def publish_draft(draft_id):
    # Placeholder – to be filled when we add X posting
    pass

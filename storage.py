import sqlite3
from typing import List, Dict

DB = "data.db"

def _conn():
    c = sqlite3.connect(DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    db = _conn()
    db.execute("""
    CREATE TABLE IF NOT EXISTS drafts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        image_path TEXT,
        state TEXT,
        created_at TEXT
    )
    """)
    db.commit()

def save_drafts(drafts: List[Dict]):
    db = _conn()
    for d in drafts:
        db.execute(
            "INSERT INTO drafts (text, image_path, state, created_at) VALUES (?, ?, ?, ?)",
            (d["text"], d["image_path"], "pending", d["created_at"])
        )
    db.commit()

def list_drafts():
    db = _conn()
    rows = db.execute(
        "SELECT * FROM drafts ORDER BY id DESC"
    ).fetchall()
    return [dict(r) for r in rows]

def approve_draft(draft_id: int):
    db = _conn()
    db.execute(
        "UPDATE drafts SET state='approved' WHERE id=?",
        (draft_id,)
    )
    db.commit()
    return True

def publish_draft(draft_id: int):
    # TODO: integrate actual X API posting here
    db = _conn()
    db.execute(
        "UPDATE drafts SET state='published' WHERE id=?",
        (draft_id,)
    )
    db.commit()
    return True


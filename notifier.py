import os
import requests

BOT = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def notify_new_drafts(drafts):
    if not BOT or not CHAT:
        return
    
    for d in drafts:
        text = f"New Draft:\n{d['text']}"
        requests.post(
            f"https://api.telegram.org/bot{BOT}/sendMessage",
            json={"chat_id": CHAT, "text": text}
        )


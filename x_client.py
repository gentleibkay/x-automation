import os
import requests
import json

API_BASE = "https://api.x.com/2"
BEARER = os.getenv("X_BEARER_TOKEN")

def create_post(text):
    url = f"{API_BASE}/tweets"
    headers = {
        "Authorization": f"Bearer {BEARER}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}
    r = requests.post(url, headers=headers, json=payload)

    if r.status_code >= 400:
        print("ERROR posting tweet:", r.text)

    r.raise_for_status()
    return r.json()


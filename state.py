import json
import os

STATE_FILE = "storage/state.json"

DEFAULT_STATE = {
    "last_anime_id": 1,
    "posts_today": 0,
    "mode": "BACKLOG"
}

def load_state():
    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    os.makedirs("storage", exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

import time
from fetcher.anilist import fetch_anime
from formatter.post_formatter import format_anime_post
from publisher.telegram import publish
from state import load_state, save_state
from config import INTERVAL_BACKLOG

def run_backlog():
    state = load_state()
    anime = fetch_anime(state["last_anime_id"])

    if not anime:
        state["last_anime_id"] += 1
        save_state(state)
        return

    text, image = format_anime_post(anime)
    publish(text, image)

    state["last_anime_id"] += 1
    save_state(state)

    time.sleep(INTERVAL_BACKLOG)

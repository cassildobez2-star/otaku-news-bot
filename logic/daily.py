import time
from state import load_state, save_state
from config import MAX_DAILY_POSTS, INTERVAL_DAILY

def run_daily():
    state = load_state()

    if state["posts_today"] >= MAX_DAILY_POSTS:
        time.sleep(INTERVAL_DAILY)
        return

    # Aqui você futuramente busca novidades reais
    state["posts_today"] += 1
    save_state(state)

    time.sleep(INTERVAL_DAILY)

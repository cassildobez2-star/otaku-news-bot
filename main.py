import time
from state import load_state, save_state
from logic.backlog import run_backlog
from logic.daily import run_daily

def main():
    while True:
        state = load_state()

        if state["mode"] == "BACKLOG":
            run_backlog()
            if state["last_anime_id"] > 5000:
                state["mode"] = "DAILY"
                state["posts_today"] = 0
                save_state(state)

        else:
            run_daily()

        time.sleep(5)

if __name__ == "__main__":
    main()

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ex: -100xxxxxxxxxx

MODE = "BACKLOG"  # BACKLOG ou DAILY

INTERVAL_BACKLOG = 20          # segundos
INTERVAL_DAILY = 45 * 60       # 45 minutos
MAX_DAILY_POSTS = 12

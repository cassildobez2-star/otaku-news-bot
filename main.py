import time
from bot import start_bot

print("🤖 Bot iniciado")

while True:
    start_bot()
    time.sleep(3600)  # 1 post por hora

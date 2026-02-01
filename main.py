from telegram import Bot
import os

bot = Bot(os.getenv("BOT_TOKEN"))
channel = os.getenv("CHANNEL_ID")

bot.send_message(
    chat_id=channel,
    text="🚨 TESTE: se você está vendo isso, o bot CONSEGUE postar no canal."
)

print("Teste enviado")

import os
import requests
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot online e respondendo!")

async def postar_teste(app):
    await app.bot.send_message(
        chat_id=CHANNEL_ID,
        text="🚀 TESTE: Se você está vendo isso, o bot CONSEGUE postar no canal."
    )

def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.post_init = postar_teste  # <-- posta assim que inicia

    print("🤖 Bot iniciado")
    app.run_polling()

import os
import json
import requests
import random
from googletrans import Translator
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update, InputMediaPhoto

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

translator = Translator()
POSTED_FILE = "posted_ids.json"

# ================= UTIL =================

def load_posted():
    if not os.path.exists(POSTED_FILE):
        return set()
    with open(POSTED_FILE, "r") as f:
        return set(json.load(f))

def save_posted(data):
    with open(POSTED_FILE, "w") as f:
        json.dump(list(data), f)

def traduzir(texto):
    try:
        return translator.translate(texto, dest="pt").text
    except:
        return texto

# ================= JIKAN =================

def buscar_anime():
    url = "https://api.jikan.moe/v4/top/anime"
    r = requests.get(url, timeout=20).json()
    return random.choice(r["data"])

def formatar_post(anime):
    titulo = anime["title"]
    sinopse = anime.get("synopsis", "Sem sinopse disponível.")
    score = anime.get("score", "N/A")
    eps = anime.get("episodes", "N/A")
    status = anime.get("status", "N/A")
    img = anime["images"]["jpg"]["large_image_url"]

    texto = (
        f"🎬 **{traduzir(titulo)}**\n\n"
        f"📊 Nota: {score}\n"
        f"🎞️ Episódios: {eps}\n"
        f"📌 Status: {traduzir(status)}\n\n"
        f"📝 {traduzir(sinopse[:700])}..."
    )

    return texto, img, anime["mal_id"]

# ================= BOT =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot online! Notícias automáticas rodando.")

async def postar_noticia(context: ContextTypes.DEFAULT_TYPE):
    posted = load_posted()

    anime = buscar_anime()
    texto, imagem, anime_id = formatar_post(anime)

    if str(anime_id) in posted:
        return

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=imagem,
        caption=texto,
        parse_mode="Markdown"
    )

    posted.add(str(anime_id))
    save_posted(posted)

# ================= MAIN =================

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # posta a cada 6 horas (4 por dia)
    app.job_queue.run_repeating(
        postar_noticia,
        interval=21600,
        first=10
    )

    print("🤖 Bot de notícias otaku iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()

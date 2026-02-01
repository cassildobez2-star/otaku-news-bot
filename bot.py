import os
import requests
import json
from googletrans import Translator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

translator = Translator()
POSTED_FILE = "posted_ids.json"

# ---------- UTIL ----------

def load_posted():
    try:
        with open(POSTED_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_posted(data):
    with open(POSTED_FILE, "w") as f:
        json.dump(list(data), f)

def traduzir(txt):
    try:
        return translator.translate(txt, dest="pt").text
    except:
        return txt

# ---------- JIKAN ----------

def buscar_anime():
    url = "https://api.jikan.moe/v4/top/anime"
    r = requests.get(url, timeout=15)
    return r.json()["data"][0]

def montar_post(anime):
    titulo = traduzir(anime["title"])
    sinopse = traduzir(anime.get("synopsis", "Sem sinopse."))
    nota = anime.get("score", "N/A")
    eps = anime.get("episodes", "N/A")
    imagem = anime["images"]["jpg"]["large_image_url"]
    anime_id = str(anime["mal_id"])

    texto = (
        f"🎬 **{titulo}**\n\n"
        f"⭐ Nota: {nota}\n"
        f"🎞️ Episódios: {eps}\n\n"
        f"📝 {sinopse[:800]}"
    )

    return texto, imagem, anime_id

# ---------- COMANDOS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot online!\nUse /postar para enviar uma notícia.")

async def postar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    posted = load_posted()

    anime = buscar_anime()
    texto, imagem, anime_id = montar_post(anime)

    if anime_id in posted:
        await update.message.reply_text("⚠️ Anime já postado, tente novamente.")
        return

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=imagem,
        caption=texto,
        parse_mode="Markdown"
    )

    posted.add(anime_id)
    save_posted(posted)

    await update.message.reply_text("✅ Notícia postada com sucesso!")

# ---------- MAIN ----------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("postar", postar))

    print("🤖 Bot iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()

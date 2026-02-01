import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# LOG
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

JIKAN_TOP_ANIME = "https://api.jikan.moe/v4/top/anime"

# ===== COMANDOS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot Otaku Online!\n\n"
        "📌 Comandos disponíveis:\n"
        "/noticias → animes em alta no MyAnimeList"
    )

async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(JIKAN_TOP_ANIME, timeout=10)
        data = response.json()["data"][:3]  # pega só 3

        for anime in data:
            titulo = anime["title"]
            score = anime["score"]
            sinopse = anime["synopsis"]
            imagem = anime["images"]["jpg"]["large_image_url"]
            url = anime["url"]

            texto = (
                f"🎬 *{titulo}*\n"
                f"⭐ Nota: {score}\n\n"
                f"{sinopse[:300]}...\n\n"
                f"🔗 {url}"
            )

            await update.message.reply_photo(
                photo=imagem,
                caption=texto,
                parse_mode="Markdown"
            )

    except Exception as e:
        await update.message.reply_text("❌ Erro ao buscar notícias.")
        logging.error(e)

# ===== START BOT =====

def start_bot():
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        raise RuntimeError("BOT_TOKEN não encontrado")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("noticias", noticias))

    print("✅ Bot rodando com Jikan API")
    app.run_polling()

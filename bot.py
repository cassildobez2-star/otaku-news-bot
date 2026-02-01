import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ex: @OtakuNews ou -100xxxxxxxxx

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot online e respondendo!\n\n"
        "Comandos disponíveis:\n"
        "/postar - postar notícia no canal"
    )

# ---------- BUSCAR NOTÍCIA ----------
def buscar_noticia():
    url = "https://api.jikan.moe/v4/top/anime?limit=1"
    r = requests.get(url, timeout=15).json()

    anime = r["data"][0]
    titulo = anime["title"]
    imagem = anime["images"]["jpg"]["large_image_url"]
    score = anime["score"]
    eps = anime["episodes"]

    texto = (
        f"🔥 *Anime em Destaque*\n\n"
        f"🎬 *{titulo}*\n"
        f"⭐ Nota: {score}\n"
        f"📺 Episódios: {eps}\n\n"
        f"Fonte: MyAnimeList"
    )

    return texto, imagem

# ---------- POSTAR ----------
async def postar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto, imagem = buscar_noticia()

    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=imagem,
        caption=texto,
        parse_mode="Markdown"
    )

    await update.message.reply_text("🚀 Notícia postada no canal com sucesso!")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("postar", postar))

    app.run_polling()

if __name__ == "__main__":
    main()

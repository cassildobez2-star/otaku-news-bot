import os
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

def postar_noticia():
    # Exemplo usando Jikan (MyAnimeList)
    url = "https://api.jikan.moe/v4/top/anime"
    r = requests.get(url, timeout=15).json()

    anime = r["data"][0]

    titulo = anime["title"]
    score = anime["score"]
    episodios = anime["episodes"]
    imagem = anime["images"]["jpg"]["large_image_url"]

    texto = (
        f"🎌 *{titulo}*\n\n"
        f"⭐ Nota: {score}\n"
        f"📺 Episódios: {episodios}\n\n"
        f"_Fonte: MyAnimeList_"
    )

    bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=imagem,
        caption=texto,
        parse_mode="Markdown"
    )

def start_bot():
    postar_noticia()

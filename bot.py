import os, json, time, random, logging, requests
from telegram import Bot
from deep_translator import GoogleTranslator

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(BOT_TOKEN)

POSTED_FILE = "posted_ids.json"

translator = GoogleTranslator(source="auto", target="pt")

JIKAN_ANIME = "https://api.jikan.moe/v4/top/anime"
JIKAN_MANGA = "https://api.jikan.moe/v4/top/manga"

STATUS_MAP = {
    "Finished Airing": "Finalizado",
    "Currently Airing": "Em exibição",
    "Not yet aired": "Ainda não lançado",
    "Publishing": "Em publicação",
    "Finished": "Finalizado",
    "On Hiatus": "Em hiato"
}

# ===== JSON HELPERS =====

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)

# ===== FETCH =====

def fetch(url):
    return requests.get(url).json()["data"]

# ===== TRANSLATE SAFE =====

def tr(text):
    if not text:
        return "Sem descrição disponível."
    try:
        return translator.translate(text[:500])
    except:
        return text

# ===== POST BUILDER =====

def build_post(item, kind):
    post_type = random.choice(["info", "ranking", "release"])
    key = f"{kind}_{item['mal_id']}_{post_type}"

    posted = load_json(POSTED_FILE)
    if key in posted:
        return None

    title = item["title"]
    synopsis = tr(item.get("synopsis"))
    score = item.get("score", "?")
    rank = item.get("rank", "?")
    favorites = item.get("favorites", "?")
    status = STATUS_MAP.get(item.get("status"), item.get("status", "?"))

    if post_type == "info":
        caption = (
            f"🎬 *{title}*\n\n"
            f"📖 *Sinopse:*\n{synopsis}\n\n"
            f"⭐ *Nota:* {score}"
        )

    elif post_type == "ranking":
        caption = (
            f"🔥 *{title}*\n\n"
            f"🏆 *Ranking:* #{rank}\n"
            f"⭐ *Nota:* {score}\n"
            f"❤️ *Favoritos:* {favorites}"
        )

    else:
        caption = (
            f"📅 *{title}*\n\n"
            f"📌 *Status:* {status}\n"
            f"🎞️ *Episódios/Capítulos:* {item.get('episodes') or item.get('chapters','?')}\n"
            f"⭐ *Nota:* {score}"
        )

    image = item["images"]["jpg"]["large_image_url"]

    posted[key] = True
    save_json(POSTED_FILE, posted)

    return caption, image

# ===== SEND =====

def send(caption, image):
    bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=image,
        caption=caption,
        parse_mode="Markdown"
    )

# ===== MAIN LOOP =====

def run_batch(limit=5):
    anime = fetch(JIKAN_ANIME)[:limit]
    manga = fetch(JIKAN_MANGA)[:limit]

    pool = anime + manga
    random.shuffle(pool)

    for item in pool:
        kind = "manga" if "chapters" in item else "anime"
        post = build_post(item, kind)
        if post:
            send(*post)
            time.sleep(25)

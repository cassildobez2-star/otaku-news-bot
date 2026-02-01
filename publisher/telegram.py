import time
from telegram.error import RetryAfter
from bot import bot
from config import CHANNEL_ID

def publish(text, image):
    try:
        bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image,
            caption=text,
            parse_mode="Markdown"
        )
    except RetryAfter as e:
        time.sleep(e.retry_after)
        publish(text, image)

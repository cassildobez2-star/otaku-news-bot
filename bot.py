import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# LOG
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ===== COMANDOS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot online!\n\n"
        "Use /noticias para ver novidades do mundo otaku."
    )

async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "📰 *Notícias Otaku*\n\n"
        "🔥 Novo trailer de Jujutsu Kaisen\n"
        "📺 Attack on Titan segue entre os mais vistos\n"
        "📚 One Piece ultrapassa 500 milhões de cópias\n"
    )
    await update.message.reply_text(texto, parse_mode="Markdown")

# ===== FUNÇÃO QUE O MAIN IMPORTA =====

def start_bot():
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        raise RuntimeError("BOT_TOKEN não encontrado nas variáveis de ambiente")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("noticias", noticias))

    print("✅ Bot iniciado com sucesso")
    app.run_polling()

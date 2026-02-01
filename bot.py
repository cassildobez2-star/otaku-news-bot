import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

# Pega o token da variável de ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Função que será chamada quando o usuário digitar /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot online e funcionando!")

# Função para configurar e iniciar o bot
def start_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Adiciona o handler para o comando /start
    app.add_handler(CommandHandler("start", start))

    # Inicia o polling para o bot ficar ouvindo as mensagens
    print("🚀 Polling iniciado")
    app.run_polling()

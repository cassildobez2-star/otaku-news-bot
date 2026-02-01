import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Habilita o log para o bot
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot online e funcionando!")

# Comando /noticias
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    noticias = """Últimas notícias sobre animes:
    1. Novo episódio de Attack on Titan está disponível.
    2. Lançamento de Demon Slayer: Kimetsu no Yaiba.
    3. Estreia de Jujutsu Kaisen 2ª temporada.
    4. Boruto recebe novo arco no mangá.
    """
    await update.message.reply_text(noticias)

# Função para configurar o bot
def main():
    # Cria a aplicação com o token do bot
    application = Application.builder().token('8515193241:AAFI1yj3tpW039zdhpDgwBBCkyhgRkcUS5k').build()

    # Adiciona os handlers de comando
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("noticias", noticias))

    # Inicia o bot
    application.run_polling()

if __name__ == "__main__":
    main()

async def postar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧪 Comando /postar recebido")

    try:
        texto, imagem = buscar_noticia()

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="🧪 Tentando postar no canal..."
        )

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=imagem,
            caption=texto,
            parse_mode="Markdown"
        )

        await update.message.reply_text("✅ Postagem enviada com sucesso")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro: {e}")

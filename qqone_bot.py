from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Connessione stabilita con la VPS!")

if __name__ == '__main__':
    # Sostituisci 'IL_TUO_TOKEN' con quello ricevuto da BotFather
    app = ApplicationBuilder().token("IL_TUO_TOKEN").build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

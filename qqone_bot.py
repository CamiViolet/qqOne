"""
qqOne BOT
"""

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from mistralai import Mistral

TELEGRAM_TOKEN = "7952315942:AAEf44ZfD6uRSM3oFieBw3UDPaGPIPESZS8"
MISTRAL_API_KEY = "Yj3PJ3WXAAscn5RyD4GlF3ajcDJqGOLP"

# Inizializza il client Mistral
mistral_client = Mistral(api_key=MISTRAL_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Connected")
    await update.message.reply_text("VPS Bot Connected")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Richiesta a Mistral AI
    chat_response = mistral_client.chat.complete(
        model="mistral-small-latest", # Puoi usare anche mistral-large-latest
        messages=[{"role": "user", "content": user_text}]
    )
    
    # Estrai la risposta dell'AI
    ai_reply = chat_response.choices[0].message.content
    await update.message.reply_text(ai_reply)


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot collegato a Mistral e in ascolto...")
    app.run_polling()

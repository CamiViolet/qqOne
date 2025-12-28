"""
qqOne BOT
"""

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from mistralai import Mistral
import google.generativeai as genai
from openai import OpenAI

TELEGRAM_TOKEN = "7952315942:AAEf44ZfD6uRSM3oFieBw3UDPaGPIPESZS8"
MISTRAL_API_KEY = "Yj3PJ3WXAAscn5RyD4GlF3ajcDJqGOLP"
GEMINI_API_KEY = "AIzaSyCr1i5zq3mcRFobHDgpyUCR9ONbiMjtVDs"
OPENAI_API_KEY = "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"

# Inizializza il client Mistral
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

# Inizializza il client Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.0-flash-lite')

# Inizializza il client OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Connected")
    await update.message.reply_text("VPS Bot Connected")


# Carica il contesto dal file
def load_context():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    context_file = os.path.join(script_dir, "DTech.1bf.txt")
    with open(context_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Limit to first 100KB (100,000 bytes)
        if len(content.encode('utf-8')) > 100000:
            # Truncate to approximately 100KB
            content = content.encode('utf-8')[:100000].decode('utf-8', errors='ignore')
        return content


# Carica il contesto all'avvio
CONTEXT_TEXT = load_context()


async def handle_message_mistral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Richiesta a Mistral AI con contesto dal file
    chat_response = mistral_client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": f"Contesto: {CONTEXT_TEXT}\n\nDomanda: {user_text}"}]
    )
    
    # Estrai la risposta dell'AI
    ai_reply = chat_response.choices[0].message.content
    await update.message.reply_text(ai_reply)


async def handle_message_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Richiesta a Gemini AI con contesto dal file
    prompt = f"Contesto: {CONTEXT_TEXT}\n\nDomanda: {user_text}"
    response = gemini_model.generate_content(prompt)
    
    # Estrai la risposta dell'AI
    ai_reply = response.text
    await update.message.reply_text(ai_reply)


async def handle_message_openai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Richiesta a OpenAI GPT con contesto dal file
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Contesto: {CONTEXT_TEXT}"},
            {"role": "user", "content": user_text}
        ]
    )
    
    # Estrai la risposta dell'AI
    ai_reply = response.choices[0].message.content
    await update.message.reply_text(ai_reply)


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message_openai))
    # app.add_handler(CommandHandler("gemini", handle_message_gemini))
    print("Bot collegato, in ascolto...")
    app.run_polling()

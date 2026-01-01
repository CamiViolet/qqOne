"""
qqOne BOT
"""

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from mistralai import Mistral
import google.genai as genai
# from openai import OpenAI

# Load environment variables from .env file
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path)

# Inizializza il client Mistral
mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Inizializza il client Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-2.0-flash-lite')

# Inizializza il client OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
        # messages=[{"role": "user", "content": f"Contesto: {CONTEXT_TEXT}\n\nDomanda: {user_text}"}]
        messages=[{"role": "user", "content": f"Domanda: {user_text}"}]
    )
    
    # Estrai la risposta dell'AI
    ai_reply = chat_response.choices[0].message.content
    await update.message.reply_text(ai_reply)


async def handle_message_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Richiesta a Gemini AI con contesto dal file
    prompt = f"Contesto: {CONTEXT_TEXT}\n\nDomanda: {user_text}"
    response = await gemini_model.generate_content_async(prompt)
    
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
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message_gemini))
    print("Bot collegato, in ascolto...")
    app.run_polling()

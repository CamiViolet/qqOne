"""
qqOne BOT
"""

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from mistralai import Mistral
import google.genai as genai

# Load environment variables from .env file
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path)

# Inizializza il client Mistral
mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# Inizializza il client Gemini
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# Carica il contesto dal file
def load_context():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    context_file = os.path.join(script_dir, "DTech.1bf.txt")
    with open(context_file, 'r', encoding='utf-8') as f:
        content = f.read()
        return content


# Carica il contesto all'avvio
CONTEXT_TEXT = load_context()


async def command_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "VPS Bot Connected"
    print(msg)
    await update.message.reply_text(msg)


async def handle_message_mistral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user_text = update.message.text
    
    use_context = False
    if "/ctx" in user_text:
        user_text = user_text.replace("/ctx", "")
        use_context = True
    
    use_gemini = False
    if "/gemini" in user_text:
        user_text = user_text.replace("/gemini", "")
        use_gemini = True

    if use_gemini:
        if use_context:
            prompt = f"Domanda: {user_text}\n\nContesto: {CONTEXT_TEXT}"
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt
            )
        else:
            prompt = f"Domanda: {user_text}"
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=prompt
            )
        
        ai_reply = response.text
    else:

        if use_context:
            chat_response = mistral_client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": f"Domanda: {user_text}\n\nContesto: {CONTEXT_TEXT}"}]
            )
        else:
            chat_response = mistral_client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": f"Domanda: {user_text}"}]
            )
        
        ai_reply = chat_response.choices[0].message.content

    await update.message.reply_text(ai_reply)


if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("check", command_check))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message_mistral))
    print("Bot collegato, in ascolto...")
    app.run_polling()

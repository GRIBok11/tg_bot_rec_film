from langchain_groq import ChatGroq
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser


load_dotenv()
groq_api_key1 = os.getenv('groq_api_key')


model = ChatGroq(
    temperature=0.7,
    groq_api_key=groq_api_key1,
    model_name="Llama3-70b-8192"
)

chain = model | StrOutputParser()

def get_movie_recommendations(genre: str) -> str:   
    prompt = f"Пожалуйста, порекомендуй 5 лучших фильмов в жанре '{genre}' и обязательно напиши ответ на русском языке."
    return chain.invoke(prompt)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Напиши жанр фильма, и я предложу 5 лучших фильмов по твоему запросу!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    await update.message.reply_text(f"Ищу фильмы в жанре: {user_input}...")


    recommendations = get_movie_recommendations(user_input)


    await update.message.reply_text(recommendations)


def main():
    

    TOKEN = os.getenv('token')

   
    application = Application.builder().token(TOKEN).build()

   
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    
    application.run_polling()

if __name__ == "__main__":
    main()

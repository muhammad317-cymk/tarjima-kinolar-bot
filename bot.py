import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎬 Assalomu alaykum!\n"
        "Tarjima kinolar botiga xush kelibsiz!\n\n"
        "🍿 Kino kodini yuboring."
    )

bot.infinity_polling() 

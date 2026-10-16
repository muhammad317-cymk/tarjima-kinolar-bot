import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- SOZLAMALAR ---
ADMIN_ID = 8731925710
CHANNEL_USERNAME = "@vexor_kino"
# Ma'lumotlar (vaqtinchalik xotirada saqlash uchun)
movies = {}
user_count = 150  # Misol uchun foydalanuvchilar soni

def check_sub(user_id):
    """Kanalga a'zolikni tekshirish"""
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception:
        return True

@bot.message_handler(commands=["start"])
def start(message):
    if not check_sub(message.from_user.id):
        bot.reply_to(
            message,
            f"🎬 Botdan foydalanish uchun avval kanalimizga a'zo bo'ling:\n\n👉 {CHANNEL_USERNAME}\n\nA'zo bo'lgach, /start ni bosing."
        )
        return

    bot.reply_to(
        message,
        "🎬 Assalomu alaykum!\nTarjima kinolar botiga xush kelibsiz!\n\n🍿 Kino kodini yuboring."
    )

@bot.message_handler(commands=["admin"])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Siz admin emassiz!")
        return

    # Tugmalarni yaratish (Rasmga o'xshash menyu)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_stat = types.KeyboardButton("📊 Statistika")
    btn_movies = types.KeyboardButton("🎬 Kinolar")
    btn_channels = types.KeyboardButton("📢 Kanallar")
    btn_send = types.KeyboardButton("✉️ Xabar yuborish")
    markup.add(btn_stat, btn_movies, btn_channels, btn_send)

    bot.send_message(
        message.chat.id,
        "👨‍💻 Admin panelga xush kelibsiz!\nKerakli bo'limni tanlang:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text

    # Admin tugmalari boshqaruvi
    if message.from_user.id == ADMIN_ID:
        if text == "📊 Statistika":
            stat_text = (
                f"📈 Bot statistikasi:\n\n"
                f"👥 Foydalanuvchilar: {user_count} ta\n"
                f"🎬 Kinolar soni: {len(movies)} ta\n"
                f"🤖 Bot: @{bot.get_me().username}"
            )
            bot.reply_to(message, stat_text, parse_mode="Markdown")
            return

        elif text == "🎬 Kinolar":
            bot.reply_to(message, "🎬 Kino qo'shish uchun quyidagi formatni yuboring:\n/add_kino KOD KINO_NOMI", parse_mode="Markdown")
            return

        elif text == "📢 Kanallar":
            bot.reply_to(message, f"📢 Ulangan majburiy obuna kanali:\n{CHANNEL_USERNAME}")
            return

        elif text == "✉️ Xabar yuborish":
            bot.reply_to(message, "Hozircha bu funksiya ishlab chiqilmoqda.")
            return

    # Oddiy kino qidirish yoki qo'shish logikasi
    if text.startswith("/add_kino") and message.from_user.id == ADMIN_ID:
        try:
            args = text.split(maxsplit=2)
            kino_code = args[1]
            kino_content = args[2]
            movies[kino_code] = kino_content
            bot.reply_to(message, f"✅ Kino saqlandi!\nKod: {kino_code}")
        except Exception:
            bot.reply_to(message, "⚠️ Xato format! Masalan: /add_kino 123 MFY", parse_mode="Markdown")
        return

    if not check_sub(message.from_user.id):
        bot.reply_to(message, f"⛔ Avval kanalga a'zo bo'ling: {CHANNEL_USERNAME}")
        return

    kino_code = text.strip()
    if kino_code in movies:
        bot.reply_to(message, f"🎬 Siz qidirgan kino:\n\n{movies[kino_code]}")
    else:
        bot.reply_to(message, "❌ Ushbu kod bo'yicha kino topilmadi.")

bot.infinity_polling()

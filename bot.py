import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- SOZLAMALAR ---
ADMIN_ID = 8731925710

# Majburiy obuna uchun kanallar ro'yxati (boshlang'ich bitta kanal bilan)
channels = ["@vexor_kino"]

# Kinolar bazasi va foydalanuvchilar hisoblagichi
movies = {}
user_count = 1

def check_sub(user_id):
    """Foydalanuvchi barcha majburiy kanallarga a'zo bo'lganini tekshirish"""
    for channel in channels:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        except Exception:
            # Agar bot kanalda admin bo'lmasa yoki xatolik bo'lsa, o'tkazib yuboradi
            pass
    return True

def get_channels_text():
    if not channels:
        return "Hozircha ulangan kanallar yo'q."
    text = "📢 Ulangan majburiy obuna kanallari:\n"
    for i, ch in enumerate(channels, 1):
        text += f"{i}. {ch}\n"
    return text

@bot.message_handler(commands=["start"])
def start(message):
    global user_count
    user_count += 1
    
    if not check_sub(message.from_user.id):
        ch_list = "\n".join([f"👉 {ch}" for ch in channels])
        bot.reply_to(
            message,
            f"🎬 Botdan foydalanish uchun avval quyidagi kanallarga a'zo bo'ling:\n\n{ch_list}\n\nA'zo bo'lgach, qayta /start ni bosing."
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

    # Tugmalarni yaratish
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
def handle_all_messages(message):
    text = message.text.strip()
    user_id = message.from_user.id

    # 1. Admin tugmalari va buyruqlari boshqaruvi
    if user_id == ADMIN_ID:
        if text == "📊 Statistika":
            stat_text = (
                f"📈 Bot statistikasi:\n\n"
                f"👥 Foydalanuvchilar: {user_count} ta\n"
                f"🎬 Kinolar soni: {len(movies)} ta\n"
                f"📢 Kanallar soni: {len(channels)} ta\n"
                f"🤖 Bot: @{bot.get_me().username}"
            )
            bot.reply_to(message, stat_text, parse_mode="Markdown")
            return

        elif text == "🎬 Kinolar":
            bot.reply_to(
                message,
                "🎬 Kino qo'shish uchun quyidagi formatda yuboring:\n"
                "/addkino KOD KINO_NOMI\n\n"
                "Masalan:\n"
                "/addkino 17 Tutqunlikda",
                parse_mode="Markdown"
            )
            return

        elif text == "📢 Kanallar":
            ch_msg = (
                f"{get_channels_text()}\n\n"
                f"➕ Kanal qo'shish uchun:\n/addkanal @username\n\n"
                f"➖ Kanalni o'chirish uchun:\n/delkanal @username"
            )
            bot.reply_to(message

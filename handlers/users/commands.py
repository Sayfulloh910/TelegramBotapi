'''KOMANDALARNI ILADIGAN HANDLERLAR'''

from telebot.types import Message
from data.loader import bot, db
from keyboards.default import main_menu


@bot.message_handler(commands=['start'], chat_types='private')
def start(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    first_name = message.from_user.first_name
    db.insert_user(from_user_id)
    bot.send_message(chat_id, f"Salom, {first_name}, online do'konimizga xush kelibsiz ☺️",
                     reply_markup=main_menu())
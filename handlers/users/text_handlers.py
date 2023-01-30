'''TEXTLARNI ILADIGAN HANDLERLAR'''
from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.default import register_button, send_phone_num
from keyboards.inline import get_categories_buttons



@bot.message_handler(regexp='Katalog 📇', chat_types='private')
def catalog(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    check = db.check_user_from_users(from_user_id)
    if None in check:
        text = '''Siz ro'yxatdan o'tmagansiz'''
        markup = register_button()
    else:
        text = '''Katalog:'''
        categories_list = db.select_all_categories()
        markup = get_categories_buttons(categories_list)
        bot.send_message(chat_id, 'Sizning so\'rovingiz amalda',
                         reply_markup=ReplyKeyboardRemove())
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish 📝")
def register(message: Message):
    data = {}
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    data[from_user_id] = {}
    msg = bot.send_message(chat_id, 'Ismingizni, familiyangizni va sharifingizni kiriting:',
                           reply_markup=ReplyKeyboardRemove())

    bot.register_next_step_handler(msg, name_save, data)

def name_save(message: Message, data):
    full_name = message.text.title()
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    data[from_user_id]['full_name'] = full_name
    msg = bot.send_message(chat_id, 'Telefon raqamingizni kiriting:', reply_markup=send_phone_num())
    bot.register_next_step_handler(msg, contact_save, data)

def contact_save(message: Message, data):
    contact = message.contact.phone_number
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    data[from_user_id]['contact'] = contact
    msg = bot.send_message(chat_id, 'Tug\'ilgan kuningizni kiriting quyidagi ko\'rinishida:\nyyyy.mm.dd',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, user_save, data)

def user_save(message: Message, data):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    birth_date = message.text
    data[from_user_id]['birth_date'] = birth_date
    name = data[from_user_id]['full_name']
    contact = data[from_user_id]['contact']
    db.save_user(name, contact, birth_date, from_user_id)
    categories_list = db.select_all_categories()
    bot.send_message(chat_id, '''Ro'yxatdan o'tdingiz''',
                     reply_markup=get_categories_buttons(categories_list))
'''
SIZ BU YERDA INLINE KNOPKALAR YARATA OLASIZ
'''
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.loader import db

def get_categories_buttons(categories_list):
    markup = InlineKeyboardMarkup(row_width=1)
    for item in categories_list:
        category_name = item[0]
        category_id = db.select_category_id_by_cat_name(category_name)[0]
        name = ''
        if category_name == 'phones':
            name = 'Telefonlar'
        elif category_name == 'tv':
            name = 'Televizorlar'
        elif category_name == 'air-conditioners':
            name = 'Konditsionerlar'
        elif category_name == 'stiralniye-mashini':
            name = 'Kir yuvish mashinalar'
        button = InlineKeyboardButton(name, callback_data=f'category|{category_id}')
        markup.add(button)
    back = InlineKeyboardButton('Ortga 🔙', callback_data='main_menu')
    markup.add(back)
    return markup


def get_products_by_pagination(category_id, page=1):
    markup = InlineKeyboardMarkup()
    limit = 6
    count = db.count_products_by_category_id(category_id)
    offset = 0 if page == 1 else (page - 1) * limit
    max_page = count // limit if count % limit == 0 else count // limit + 1
    products = db.select_products_by_pagination(category_id, offset, limit)
    for product in products:
        markup.add(InlineKeyboardButton(product[0], callback_data=f"product|{product[1]}"))

    back = InlineKeyboardButton('⏮', callback_data=f'previous_page|{category_id}')
    current_page = InlineKeyboardButton(f"{page}", callback_data='current_page')
    next = InlineKeyboardButton('⏭', callback_data=f'next_page|{category_id}')

    if 1 < page < max_page:
        markup.row(back, current_page, next)
    elif page == 1:
        markup.row(current_page, next)
    else:
        markup.row(back, current_page)


    markup.row(InlineKeyboardButton('Ortga 🔙', callback_data='back_categories'),
               InlineKeyboardButton('Asosiy menu', callback_data='main_menu'))
    return markup


def get_product_control_buttons(category_id, product_id, quantity=1):
    quantity = [InlineKeyboardButton('➖', callback_data='minus'),
                InlineKeyboardButton(quantity, callback_data='quantity'),
                InlineKeyboardButton('➕', callback_data='plus')]

    card = [InlineKeyboardButton('Savatga qo\'shish', callback_data=f'add|{product_id}'),
            InlineKeyboardButton('Savat 🛒', callback_data='show_card')]

    backs = [InlineKeyboardButton('Ortga 🔙', callback_data=f"category|{category_id}"),
             InlineKeyboardButton('Katalog 📇', callback_data='back_categories')]
    main_menu = [InlineKeyboardButton('Asosiy menu', callback_data='main_menu')]

    return InlineKeyboardMarkup(keyboard=[quantity, card, backs, main_menu], row_width=1)


def show_card_buttons(data:dict):
    markup = InlineKeyboardMarkup(row_width=1)
    for product_name, items in data.items():
        product_id = items['product_id']
        btn = InlineKeyboardButton(f"❌ {product_name}",
                                   callback_data=f'remove|{product_id}')
        markup.add(btn)
    back = InlineKeyboardButton('Katalog 📇', callback_data='back_categories')
    clear = InlineKeyboardButton('🔄 Tozalash', callback_data='clear_card')
    order = InlineKeyboardButton('Tasdiqlash ✅', callback_data='submit')
    markup.row(clear, order)
    markup.row(back)
    return markup

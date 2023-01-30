'''
BOTNI ISHGA TUSHIRISH
'''
from middlewares import SimpleMiddleware
from data.loader import bot, db
from parser import OpenShopParser

import handlers

def create_tables(database, pars_oop):
    database.create_categories_table()
    database.create_products_table()
    database.create_users_table()
    database.create_table_order()
    database.create_table_order_item()

    database.insert_categories('phones')
    database.insert_categories('tv')
    database.insert_categories('air-conditioners')
    database.insert_categories('stiralniye-mashini')

    product_list = [pars_oop('phones').get_info(), pars_oop('tv').get_info(),
                    pars_oop('air-conditioners').get_info(), pars_oop('stiralniye-mashini').get_info()]

    for item in product_list:
        for product in item:
            image = product['image']
            link = product['link']
            price = product['price']
            title = product['title']
            category_id = product['category_id']
            database.insert_products(product_name=title, product_link=link, product_image=image,
                               product_price=price, category_id=category_id)




bot.setup_middleware(SimpleMiddleware(0.5)) # bu botga qayta qayta yozmaslik uchun limit(sekundda) kiritiladi

if __name__ == '__main__':
    create_tables(db, OpenShopParser)
    bot.infinity_polling()
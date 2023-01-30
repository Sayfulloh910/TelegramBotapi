from bs4 import BeautifulSoup
import requests
from data.loader import db


class OpenShopParser:
    def __init__(self, category):
        if category == 'phones':
            self.URL = 'https://openshop.uz/shop/subcategory/'
        elif category == 'tv' or category == 'air-conditioners' or category == 'stiralniye-mashini':
            self.URL = 'https://openshop.uz/shop/subsubcategory/'

        self.category = category.lower()
        self.HEADERS = {
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }

    def get_soup(self):
        try:
            response = requests.get(self.URL + self.category, headers=self.HEADERS)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        except:
            print('404')

    def get_info(self):
        data = []
        soup = self.get_soup()
        box = soup.find('div', class_='product-wrapper row cols-lg-4 cols-md-3 cols-sm-2 cols-2')
        products = box.find_all('div', class_='product-wrap')
        for product in products:
            title = product.find('h3').get_text(strip=True)
            link = product.find('a')['href']
            price = int(product.find('ins', class_='new-price').get_text(strip=True).split('UZS')[0].replace(' ',''))
            image = product.find('img')['src']

            cat_id = db.select_category_id_by_cat_name(self.category)[0]

            data.append({
                'title': title,
                'link': link,
                'price': price,
                'image': image,
                'category_id': cat_id
            })
        return data
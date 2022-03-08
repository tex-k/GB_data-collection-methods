# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def process_item(self, item, spider):
        prices = self.process_price(item["price"])

        book = {
            "Название": self.process_name(item["name"]),
            "Автор": self.process_author(item["author"]),
            "Основная цена": prices[0],
            "Скидочная цена": prices[1],
            "Ссылка": item["link"],
            "Рейтинг": item["voting"]
        }

        print(book)

        client = MongoClient("localhost", 27017)
        db = client.books
        collection_lab = db["labirint"]
        collection_lab.insert_one(book)

        return item

    def process_name(self, name):
        return name[name.find('"')+1:-1]

    def process_author(self, author):
        if author:
            return author[0]
        else:
            return None

    def process_price(self, price):
        if price[0].isdigit():
            return price[0], price[1]
        elif price[1].isdigit():
            return price[1], price[1]

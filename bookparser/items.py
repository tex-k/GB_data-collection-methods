# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    voting = scrapy.Field()
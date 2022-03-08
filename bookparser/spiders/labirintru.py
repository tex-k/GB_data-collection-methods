import scrapy
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/python/?stype=0']

    def parse(self, response):
        next_page = response.xpath('//a[@title="Следующая"]/@href').getall()
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)

        links = response.xpath('//a[@class="product-title-link"]/@href').getall()

        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response):
        name = response.xpath("//div[@id='product-about']/h2/text()").getall()[0]
        author = response.xpath("//div[@class='authors']/a/text()").getall()
        link = response.url
        price = response.xpath("//div[@class='buying']//span/text()").getall()
        voting = response.xpath("//div[@id='rate']/text()").getall()[0]

        yield BookparserItem(name=name, author=author, link=link, price=price, voting=voting)

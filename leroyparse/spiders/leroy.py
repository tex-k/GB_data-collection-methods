import scrapy
from leroyparse.items import LeroyparseItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=%D0%BB%D0%B0%D0%BC%D0%B8%D0%BD%D0%B0%D1%82&family=laminat-201709&suggest=true']

    def parse(self, response):
        next_page = response.xpath("//a[@class='bex6mjh_plp s15wh9uj_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp'][@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class='phytpj4_plp largeCard']/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_adv)

    def parse_adv(self, response):
        name = response.xpath("//h1/text()").get()
        price = response.xpath("//uc-pdp-price-view//meta[@itemprop='price']/@content").get()
        link = response.url

        photos = []
        pictures = response.xpath("//picture[@slot='pictures']")
        for photo in pictures:
            photos.append(photo.xpath("./source/@srcset").get())

        yield LeroyparseItem(name=name, price=price, link=link, photos=photos)

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlin.items import LeroymerlinItem
from urllib.parse import urljoin


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/umnyy-dom/']
    root_url = 'https://leroymerlin.ru'

    def parse(self, response, *kwargs):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(urljoin(self.root_url, next_page), callback=self.parse)

        products_urls = response.xpath("//a[@data-qa='product-name']/@href").extract()
        yield from response.follow_all(products_urls, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', "///h1[@slot='title']]/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/source[1]/@srcset")
        yield loader.load_item()


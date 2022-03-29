# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags


def change_price(value):
    return int(''.join([str(s) for s in value.split() if s.isdigit()]))


class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, change_price), output_processor=TakeFirst())
    photos = scrapy.Field()

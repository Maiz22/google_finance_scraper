# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Stock(scrapy.Item):
    name = scrapy.Field()
    cur_price = scrapy.Field()
    closing_price = scrapy.Field()

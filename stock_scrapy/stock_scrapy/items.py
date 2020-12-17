# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class StockscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    Date = scrapy.Field()
    Open = scrapy.Field()
    High = scrapy.Field()
    Low = scrapy.Field()
    Close = scrapy.Field()
    PriceChange = scrapy.Field()
    PerChange = scrapy.Field()
    # pass

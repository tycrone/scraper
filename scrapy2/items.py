# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Extracted items -> temporary containers -> then to the csv

import scrapy

class Scrapy2Item(scrapy.Item):
    theurl = scrapy.Field()
    sku = scrapy.Field()
    title = scrapy.Field()
    artist = scrapy.Field()
    image_urls = scrapy.Field()

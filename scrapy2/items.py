# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Extracted items -> temporary containers -> then to the csv

import scrapy

class Scrapy2Item(scrapy.Item):
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    sku = scrapy.Field()
    file_name = scrapy.Field()

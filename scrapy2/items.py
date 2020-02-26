# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Extracted items -> temporary containers -> then to the csv

import scrapy

class Scrapy2Item(scrapy.Item):
    theindex = scrapy.Field()
    theurl = scrapy.Field()
    sku = scrapy.Field()
    title = scrapy.Field()
    artist = scrapy.Field()
    image_urls = scrapy.Field()
    tracklist = scrapy.Field()
    description = scrapy.Field()
    image_db_filepath = scrapy.Field()
    allowonweb = scrapy.Field()
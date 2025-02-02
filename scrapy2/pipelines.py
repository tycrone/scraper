# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

# class Scrapy2Pipeline(object):
#     def process_item(self, item, spider):
#
#         return item

import csv

class Scrapy2Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'image_name': item['sku']})
                for x in item.get('image_urls', [])]

    # write in current folder using the name we chose before
    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['image_name']

# def write_to_csv(item):
#    writer = csv.writer(open('C:/Users/Tyler/Desktop/scraper/scrapy2/spiders/csv/output.csv', 'a'), lineterminator='\n')
#    writer.writerow([item[sku] for sku in item.keys()])
#
# class WriteToCsv(object):
#
#     def process_item(self, item, info):
#         write_to_csv(item)
#         return item

class WriteToCsv(object):
    def __init__(self):
        self.csvwriter = csv.writer(open('C:/Users/Tyler/Desktop/scraper/scrapy2/spiders/csv/output.csv', 'w', newline=''))
        self.csvwriter.writerow(["INDEX","ITEMNO","SHORTDESCR","SHORTDESCRFR","ARTIST","LONGDESCEN","LONGDESCFR","TRACKLIST","STUDIO","NOOFDISCS","DURATION","RATING","RELEASE","IMAGEURL1","PRODUCTLENGTH","PRODUCTWIDTH","PRODUCTHEIGHT","PRODUCTWEIGHT","SIZE","GENDER","LVL1CODE","LVL2CODE","LVL3CODE","METATITLE","METAKEYWORD","METADESCEN","METADESCFR","WEBDEAL1","WEBDEAL2","WEBDEAL3","WEBDEAL4","WEBDEAL5","PRODUCTTAG1","PRODUCTTAG2","PRODUCTTAG3","PRODUCTTAG4","PRODUCTTAG5","ALLOWONWEB"])

    def process_item(self,item,spider):
        self.csvwriter.writerow([item['theindex'],item['sku'],item['title'],item['title'],item['artist'],item['description'],item['description'],item['tracklist'],"","","","","",item['image_db_filepath'],"","","","","","","","","","","","","","","","","","","","","","","",item['allowonweb']])
        return item

    theurl = scrapy.Field()
    image_urls = scrapy.Field()

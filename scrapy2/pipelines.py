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

class Scrapy2Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'image_name': item['sku']})
                for x in item.get('image_urls', [])]

    # write in current folder using the name we chose before
    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['image_name']
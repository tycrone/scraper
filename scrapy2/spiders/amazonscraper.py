import scrapy
import csv
from scrapy.crawler import CrawlerProcess
from scrapy2.items import Scrapy2Item

sku_list = []

with open("C:/Users/Tyler/Desktop/scrapy2/scrapy2/spiders/csv/skus.csv", newline="") as csvfile:
    skureader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in skureader:
        sku_list.append(''.join(row))

class spider1(scrapy.Spider):
    name = "spider1"
    domain = "https://www.amazon.ca/s?k="

    def start_requests(self):
        for url in sku_list:
            yield scrapy.Request(url=spider1.domain+url ,callback = self.parse)

    def parse(self, response):

        # orig_sku1 = response.url
        # orig_sku2 = orig_sku1.replace("https://www.amazon.ca/", "")
        # sep = '/'
        # orig_sku3 = orig_sku2.split(sep, 1)[0]

        items = Scrapy2Item()

        RESULT_SELECTOR = '.s-result-item'

        for dataset in response.css(RESULT_SELECTOR):

            titlevar = dataset.css('span.a-text-normal ::text').extract_first()
            imgvar = [dataset.css('img ::attr(src)').extract_first()]
            skuvar = response.xpath('//meta[@name="keywords"]/@content')[0].extract()

            skuvar_split = skuvar.split(',', 1)[0]

            items['title'] = titlevar
            items['image_urls'] = imgvar
            items['sku'] = skuvar_split

            yield items




# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# process.crawl(spider1)
# process.start()
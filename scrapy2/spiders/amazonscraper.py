import scrapy
import csv
from scrapy2.items import Scrapy2Item
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

class spider1(scrapy.Spider):
    name = "spider1"
    domain = "https://www.amazon.ca/s?k="

    with open("C:/Users/Tyler/Desktop/scraper/scrapy2/spiders/csv/input.csv", newline="") as csvfile:
        skureader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        sku_list = []

        for row in skureader:
            sku_list.append(''.join(row))

    def start_requests(self):
        for url in self.sku_list:
            yield scrapy.Request(url=spider1.domain+url ,callback = self.parse)

    def parse(self, response):

        #use original searched sku as opposed to sku pulled from page (current skuvar)
        # orig_sku1 = response.url
        # orig_sku2 = orig_sku1.replace("https://www.amazon.ca/", "")
        # sep = '/'
        # orig_sku3 = orig_sku2.split(sep, 1)[0]

        items = Scrapy2Item()

        RESULT_SELECTOR = ".sg-col-20-of-24" + \
                          ".s-result-item" + \
                          ".sg-col-0-of-12" + \
                          ".sg-col-28-of-32" + \
                          ".sg-col-16-of-20" + \
                          ".sg-col" + \
                          ".sg-col-32-of-36" + \
                          ".sg-col-12-of-16" + \
                          ".sg-col-24-of-28"

        for dataset in response.css(RESULT_SELECTOR):

            titlevar = dataset.css('span.a-text-normal ::text').extract_first()
            # artistvar = response.xpath('//span[@class="a-size-base"]/text()')[1].extract()
            artistvar = dataset.css('span.a-size-base ::text').extract()

            imgvar = [dataset.css('img ::attr(src)').extract_first()]
            skuvar = response.xpath('//meta[@name="keywords"]/@content')[0].extract()

            skuvar_split = skuvar.split(',', 1)[0]
            artistvar_split = artistvar[1]

            if any("by " in s for s in artistvar):
                items['artist'] = artistvar_split
            else:
                items['artist'] = ""


            items['sku'] = skuvar_split
            items['title'] = titlevar
            # items['artist'] = artistvar_split
            items['image_urls'] = imgvar

            yield items

# process = CrawlerProcess(get_project_settings())
# process.crawl(spider1)
# process.start()

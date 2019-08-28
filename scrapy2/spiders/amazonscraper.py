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
            yield scrapy.Request(url=spider1.domain+url, callback = self.parse)

    custom_settings = {
        'DEPTH_LIMIT': 1
    }

    def parse(self, response):

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

            items = Scrapy2Item()

            titlevar = dataset.css('span.a-text-normal ::text').extract_first()
            artistvar = dataset.css('span.a-size-base ::text').extract()

            skuvar = response.xpath('//meta[@name="keywords"]/@content')[0].extract()

            skuvar_split = skuvar.split(',', 1)[0]
            artistvar_split = artistvar[1]

            if any ("Sponsored" in s for s in artistvar):
                items['artist'] = "DELETE THIS"
                items['sku'] = "DELETE THIS"
                items['title'] = "DELETE THIS"
            elif any("by " in s for s in artistvar):
                items['artist'] = artistvar_split
                items['sku'] = skuvar_split
                items['title'] = titlevar
            else:
                items['artist'] = ""
                items['sku'] = skuvar_split
                items['title'] = titlevar

            itempage = response.urljoin(dataset.css('div.a-section > h2.a-size-mini > a ::attr(href)').extract_first())

            items['theurl'] = itempage

            request = scrapy.Request(itempage, callback=self.get_iteminfo)
            request.meta['items'] = items  # By calling .meta, we can pass our item object into the callback.
            yield request  # Return the item info back to the parser.

    def get_iteminfo(self, response):

        items = response.meta['items']  # Get the item we passed from scrape()

        imgvar = [response.css('img#landingImage ::attr(data-old-hires)').extract_first()]

        if len(imgvar) < 2:
            imgvar = [response.css('img#landingImage ::attr(src)').extract_first()]

        items['image_urls'] = imgvar

        yield items

# process = CrawlerProcess(get_project_settings())
# process.crawl(spider1)
# process.start()

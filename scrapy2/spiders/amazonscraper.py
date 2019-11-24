import scrapy
import csv
from scrapy2.items import Scrapy2Item
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings

class spider1(scrapy.Spider):
    name = "spider1"
    rotate_user_agent = True
    domain = "https://www.amazon.ca/s?k="

    with open("C:/Users/Tyler/Desktop/scraper/scrapy2/spiders/csv/input.csv", newline="") as csvfile:
        skureader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        sku_list = []

        for row in skureader:
            sku_list.append(''.join(row))

    def start_requests(self):

        for index, url in enumerate(self.sku_list):
            yield scrapy.Request(url=spider1.domain+url, callback = self.parse, meta={'index_number': index})

    def parse(self, response):

        #RUN SCRAPY SHELL FOR DEBUGGING PURPOSES
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = Scrapy2Item()

        items['theindex'] = response.meta['index_number']

        results_exist = response.css('span.a-size-medium').extract()


        results_exist_type1 = response.css('div.sg-col-20-of-24.s-result-item.sg-col-0-of-12.sg-col-28-of-32.sg-col-16-of-20.sg-col.sg-col-32-of-36.sg-col-12-of-16.sg-col-24-of-28').extract()
        results_exist_type2 = response.css('div.sg-col-4-of-24.sg-col-4-of-12.sg-col-4-of-36.s-result-item.sg-col-4-of-28.sg-col-4-of-16.sg-col.sg-col-4-of-20.sg-col-4-of-32').extract()

        RESULT_SELECTOR_TEST1 = ".sg-col-20-of-24" + \
                          ".s-result-item" + \
                          ".sg-col-0-of-12" + \
                          ".sg-col-28-of-32" + \
                          ".sg-col-16-of-20" + \
                          ".sg-col" + \
                          ".sg-col-32-of-36" + \
                          ".sg-col-12-of-16" + \
                          ".sg-col-24-of-28"

        RESULT_SELECTOR_TEST2 = "[data-index='0']"

        #IF NO RESULTS EXIST
        if any("No results for" in s for s in results_exist):
            skuvar = response.xpath('//meta[@name="keywords"]/@content')[0].extract()
            skuvar_split = skuvar.split(',', 1)[0]

            items['sku'] = str(skuvar_split.encode('utf-8'))[2:-1]
            items['theurl'] = ""
            items['title'] = ""
            items['artist'] = ""
            items['image_urls'] = ["https://www.sunriserecords.com/wp-content/uploads/2019/03/ENG-Sunrise-Records-Logo-Dark-Background-nobg.png"]
            items['tracklist'] = ""
            items['description'] = ""
            items['image_db_filepath'] = ""
            yield items

            print("NO RESULTS EXIST 1")

        #IF RESULTS EXIST
        else:
            if (len(results_exist_type1) > 4):
                RESULT_SELECTOR = RESULT_SELECTOR_TEST1

                print("RESULTS EXIST 1")
            else:
                RESULT_SELECTOR = RESULT_SELECTOR_TEST2

                print("RESULTS EXIST 2")

            for dataset in response.css(RESULT_SELECTOR):

                titlevar = dataset.css('span.a-text-normal ::text').extract_first()

                artistvar = dataset.css('span.a-size-base ::text').extract()

                if len(artistvar) > 1:
                    artistvar_split = artistvar[1]
                else:
                    artistvar_split = "artist"

                print("ITEMCOUNT")
                print(len(artistvar))

                skuvar = response.xpath('//meta[@name="keywords"]/@content')[0].extract()
                skuvar_split = skuvar.split(',', 1)[0]

                if any ("Sponsored" in s for s in artistvar):
                    items['sku'] = "DELETE THIS"
                    items['title'] = "DELETE THIS"
                    items['artist'] = "DELETE THIS"
                    print(artistvar)
                elif any("by " in s for s in artistvar):
                    items['sku'] = str(skuvar_split.encode('utf-8'))[2:-1]
                    items['title'] = titlevar
                    items['artist'] = artistvar_split
                else:
                    items['sku'] = str(skuvar_split.encode('utf-8'))[2:-1]
                    items['title'] = titlevar
                    items['artist'] = ""


                items['image_db_filepath'] = "\\" + "\\"  + "everest-nas3\srweb_images" + "\\" + skuvar_split + ".jpg"

                itempage = response.urljoin(dataset.css('div.a-section > h2.a-size-mini > a ::attr(href)').extract_first())
                items['theurl'] = itempage

                request = scrapy.Request(itempage, callback=self.get_iteminfo)
                request.meta['items'] = items  # By calling .meta, we can pass our item object into the callback.
                yield request  # Return the item info back to the parser.

    def get_iteminfo(self, response):

        items = response.meta['items']  # Get the item we passed from scrape()

        #----------FIND IMG SOURCE AND ASSIGN
        imgvar_test1 = response.css('img#landingImage').extract_first()
        imgvar_test2 = response.css('img#landingImage ::attr(data-old-hires)').extract_first()
        imgvar_test3 = response.css('div#img-canvas > img ::attr(src)').extract_first()
        imgvar_hires1 = [response.css('img#landingImage ::attr(data-old-hires)').extract_first()]
        imgvar_hires2 = [response.css('img#landingImage ::attr(src)').extract_first()]
        imgvar_lores = [response.css('div#img-canvas > img ::attr(src)').extract_first()]

        if imgvar_test1 is None:
            items['image_urls'] = imgvar_lores
        elif len(imgvar_test2) <  5:
            items['image_urls'] = imgvar_hires2
        else:
            items['image_urls'] = imgvar_hires1

        #----------FIND TRACKLIST AND ASSIGN
        trackvar = response.css('div#musicTracksFeature > div.content > table > tbody > tr > td ::text').extract()
        trackvar_str = ''.join(trackvar)
        trackvar_tweaked = trackvar_str.replace('\n', ' ')

        if trackvar is None:
            items['tracklist'] = ""
        else:
            items['tracklist'] = trackvar_tweaked

        #----------FIND DESCRIPTION AND ASSIGN
        descvar = response.css('div#productDescription > p ::text').extract()
        descvar_str = ''.join(descvar)
        descvar_tweaked1 = descvar_str.replace('\n', '')
        descvar_tweaked2 = descvar_tweaked1.replace('\t', '')

        if descvar is None:
            items['description'] = ""
        else:
            items['description'] = descvar_tweaked2

        yield items

# process = CrawlerProcess(get_project_settings())
# process.crawl(spider1)
# process.start()

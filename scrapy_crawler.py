'''Scrapy Web Crawler
site: https://scrapy.org/, docs: https://docs.scrapy.org/en/latest/

what does it do? bundles together making of HTTP request, extraction of data, and writing data to file.
+ve: with just a couple of lines we can get some REALLY impressive results 
-ve: we have to follow the rules of the framework

The demo below features a spider / web crawler. To steal from the explanation on scrapy's site:

    'Spiders are classes which define how a certain site (or a group of sites) will be scraped, 
    including how to perform the crawl (i.e. follow links) and how to extract structured data 
    from their pages (i.e. scraping items). In other words, Spiders are the place where you 
    define the custom behaviour for crawling and parsing pages for a particular site (or, in 
    some cases, a group of sites).'

'''

import scrapy

#our defined class HAS TO inherit from scrapy.Spider
class BookSpider(scrapy.Spider):
    name = 'bookspider'
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        for article in response.css('article.product_pod'):
            yield {
                'price': article.css(".price_color::text").extract_first(),
                'title': article.css("h3 > a::attr(title)").extract_first()
            }

            next = response.css(".next > a::attr(href)").extract_first()

            #if there's a next button, follow it thru and scrape that page as well
            if next:
                yield response.follow(next, self.parse)
                
#to execute scraper, type the following into terminal: "scrapy runspider -o books.csv scrapy_crawler.py"
##"books.csv": name of .csv file we'd like to create
##"scrapy_crawler.py": name of our crawler Python file

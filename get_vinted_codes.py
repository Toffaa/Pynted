import scrapy

class CodesSpider(scrapy.Spider):
    name = "codes"

    def start_requests(self):
        
# -*- coding: utf-8 -*-
import scrapy

class VintedcodeSpider(scrapy.Spider):
    name = 'VintedCode'
    allowed_domains = ['vinted.fr/']
    base_url = "https://www.vinted.fr/vetements?"
    first_code = 0
    last_code = 100
    tag = 'catalog'


    def start_requests(self):
        for i in range(self.first_code, self.last_code):
            yield Request(base_url + tag + "[]=%d" % i, callback=self.parse)

    def parse(self, response):
        code = response.request.url

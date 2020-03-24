# -*- coding: utf-8 -*-
import scrapy


class VintedadSpider(scrapy.Spider):
    name = 'VintedAd'
    allowed_domains = ['https://www.vinted.fr/']
    start_urls = ['http://https://www.vinted.fr//']

    def parse_index(self, response):
        pass

    def parse_ad(self, response):
        pass
 
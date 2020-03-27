# -*- coding: utf-8 -*-
import scrapy

class VintedcodeSpider(scrapy.Spider):
    name = 'VintedCode'
    allowed_domains = ['vinted.fr']
    base_url = 'https://www.vinted.fr/vetements?'
    first_code = 0
    last_code = 100
    tag = 'catalog'
    lang = 'es-fr'


    def start_requests(self):
        # Initial way to send data with scrapy.http.Request
        formatted_lang = '{"locale":"%s"}' % self.lang
        # New way with JsonRequest, but still not working yet...
        formatted_lang = {"locale" : self.lang}
        scrapy.http.JsonRequest('https://www.vinted.fr/session_locale', method='PUT', data=formatted_lang, callback=self.parse_lang)
        for i in range(self.first_code, self.last_code):
            yield scrapy.http.Request(self.base_url + self.tag + '[]=%d' % i, meta={'index':i}, callback=self.parse)
    
    def parse_lang(self, response):
        return

    def parse(self, response):
        code = response.meta['index']
        value = response.xpath('//*[@id="catalog"]/div[1]/div[1]/h1/text()').get()

        return {str(code):value}

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
        formatted_lang = '{"locale":"%s"}' % self.lang
        scrapy.http.Request('https://www.vinted.fr/session_locale', method='PUT', body=formatted_lang)
        for i in range(self.first_code, self.last_code):
            yield scrapy.http.Request(self.base_url + self.tag + '[]=%d' % i, meta={'index':i}, callback=self.parse)

    def parse(self, response):
        code = response.meta['index']
        value = response.xpath('//*[@id="catalog"]/div[1]/div[1]/h1/text()').get()

        return {str(code):value}

# -*- coding: utf-8 -*-
import scrapy
from PyntedScrapers.items import Catalog_id
from PyntedScrapers.loaders import CodeLoader

class VintedcodeSpider(scrapy.Spider):
    name = 'VintedCode'
    allowed_domains = ['vinted.fr']
    base_url = 'https://www.vinted.fr/vetements?'
    first_code = 0
    # Last code is about 3000
    last_code = 100
    tag = 'catalog'
    lang = 'es-fr'

    kind_translation = {
        'men' : 'Hommes',
        'women' : 'Femmes',
        'kids' : 'Enfants',
        'boys' : 'Garcons',
        'girls' : 'Filles',
        'home' : 'Maison'
    } 


    def start_requests(self):
        # Initial way to send data with scrapy.http.Request
        formatted_lang = '{"locale":"%s"}' % self.lang
        # New way with JsonRequest, but still not working yet...
        formatted_lang = {"locale" : self.lang}
        scrapy.http.JsonRequest('https://www.vinted.fr/session_locale', method='PUT', data=formatted_lang)
        for i in range(self.first_code, self.last_code):
            yield scrapy.http.Request(self.base_url + self.tag + '[]=%d' % i, meta={'index':i}, callback=self.parse)

    def parse(self, response):

        if self.tag == 'catalog':
            il = CodeLoader(item=Catalog_id(), response=response)
            il.add_xpath('value', '//*[@id="catalog"]/div[1]/div[1]/h1/text()')

            nav_bar = il.nested_xpath('//*[@id="catalog"]/div[1]/div[1]/nav')
            #category = 
            #il.add_xpath('')

        if self.tag == 'brand_id':
            pass
        il.add_value('code', response.meta['index'])

        return il.load_item()

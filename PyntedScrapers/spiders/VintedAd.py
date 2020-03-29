# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from PyntedScrapers.items import Ad
from PyntedScrapers.loaders import AdLoader

import json
import re
import w3lib.html




class VintedadSpider(scrapy.Spider):
    name = 'VintedAd'
    allowed_domains = ['vinted.fr']

    last_ad = False
    base_url = 'https://www.vinted.fr/vetements?'

    properties_name = {
        'brand' : 'Marque',
        'size' : 'Taille',
        'condition' : 'État',
        'color' : 'Couleur',
        'location' : 'Emplacement',
        'views' : 'Nombre de vues',
        'interested' : 'Intéressés·ées',
        'uploadedDatetime' : 'Ajouté'
    }

    def start_requests(self):
        i = 1
        while self.last_ad is not True:
            yield scrapy.http.Request(self.base_url + 'page=%d' % i)
            i = i + 1

    def parse(self, response):
        for i in range(1, 25):
            ad_url = response.xpath('//*[@id="catalog"]/div[4]/div/div[2]/div[%d]/section/figure/div/a/@href' % i).get()
            if ad_url is not None:
                yield response.follow(ad_url, callback=self.parse_ad)
            else:
                self.last_ad = True
                break
    
    def parse_ad(self, response):
        il = AdLoader(item=Ad(), response=response)

        ## Scraping the properties of the announce
        property_loader = il.nested_xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]')
        for div in range(1,9):
            current_property = property_loader.get_xpath('.//div[%d]/div[1]/text()' % div)
            if current_property == []:
                break
            elif current_property[0].find(self.properties_name['brand']) != -1:
                property_loader.add_xpath('brand', './/div[%d]/div[2]/a/span/text()' % div)

            elif current_property[0].find(self.properties_name['size']) != -1:
                property_loader.add_xpath('size', './/div[%d]/div[2]/text()' % div)
                
            elif current_property[0].find(self.properties_name['condition']) != -1:
                property_loader.add_xpath('condition', './/div[%d]/div[2]/text()' % div)

            elif current_property[0].find(self.properties_name['color']) != -1:
                property_loader.add_xpath('color', './/div[%d]/div[2]/text()' % div)

            elif current_property[0].find(self.properties_name['location']) != -1:
                location = property_loader.get_xpath('.//div[%d]/div[2]/text()' % div)[0]
                location = w3lib.html.strip_html5_whitespace(location).split(',')
                if len(location) == 2:
                    property_loader.add_value('city', location[0])
                    property_loader.add_value('country', location[1])
                else:
                    property_loader.add_value('city', None)
                    property_loader.add_value('country', location[0])

            elif current_property[0].find(self.properties_name['views']) != -1:
                property_loader.add_xpath('views', './/div[%d]/div[2]/text()' % div)

            elif current_property[0].find(self.properties_name['interested']) != -1:
                property_loader.add_xpath('interested', './/div[%d]/div[2]/text()' % div, re=r'\d+')

            elif current_property[0].find(self.properties_name['uploadedDatetime']) != -1:
                property_loader.add_xpath('uploadedDatetime', './/div[8]/div[2]/time/@datetime')

        il.add_xpath('price', '/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[1]/div[1]/span/div/text()', re=r'\d+,\d+')
        
        ## Scraping title and description
        description = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[2]/script/text()').get()
        description = json.loads(description)
        il.add_value('title', description['content']['title'])
        il.add_value('description', description['content']['description'])
        il.add_value('itemId', description['itemId'])

        ## Scraping user information
        user_loader = il.nested_xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[2]')
        user_url = user_loader.get_xpath('.//div/a/@href')[0]
        user_loader.add_value('userId', user_url.split('/')[2])
        user_loader.add_xpath('userName', './/div[1]/div[2]/div[1]/h4/span/span/a/text()')
        user_loader.add_xpath('lastSeen', './/div[1]/div[2]/div[3]/div/span/time/@datetime')

        # Scraping ratings information
        ratings_loader = user_loader.nested_xpath('.//div[1]/div[2]/div[1]/a/div')
        nbRating = ratings_loader.get_xpath('.//div[6]/div/text()')
        if nbRating == []:
            ratings_loader.add_value('nbRating', 0)
        else:
            ratings_loader.add_value('nbRating', nbRating[0])
            rate = 0
            for i in range(1, 6):
                star = ratings_loader.get_xpath('.//div[%d]/@class' % i)[0]
                if star == 'c-rating__star c-rating__star--full':
                    rate = rate + 1
                elif star == 'c-rating__star c-rating__star--half-full':
                    rate = rate + 0.5
                    break
                else:
                    break
            ratings_loader.add_value('rate', rate)

        il.add_value('url', response.request.url)

        #response.xpath('/text()').get()
        yield il.load_item()
 
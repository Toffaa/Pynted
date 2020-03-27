# -*- coding: utf-8 -*-
import scrapy
import json
import re


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
        ad_details = {}
        
        ## Scraping the properties
        property_divs = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]')

        for div in range(1,9):
            current_property = property_divs.xpath('.//div[%d]/div[1]/text()' % div).get()
            
            if current_property is None:
                break

            elif current_property.find(self.properties_name['brand']) != -1:
                ad_details['brand'] = property_divs.xpath('.//div[%d]/div[2]/a/span/text()' % div).get()

            elif current_property.find(self.properties_name['size']) != -1:
                size = property_divs.xpath('.//div[%d]/div[2]/text()' % div).get()
                ad_details['size'] = re.sub(' +', ' ',size.replace('\n', ''))
                
            elif current_property.find(self.properties_name['condition']) != -1:
                ad_details['condition'] = property_divs.xpath('.//div[%d]/div[2]/text()' % div).get()

            elif current_property.find(self.properties_name['color']) != -1:
                color = property_divs.xpath('.//div[%d]/div[2]/text()' % div).get()
                ad_details['color'] = color.split(', ')

            elif current_property.find(self.properties_name['location']) != -1:
                location = property_divs.xpath('.//div[%d]/div[2]/text()' % div).get()
                location = location.replace(' ','').replace('\n', '').split(',')
                if len(location) == 2:
                    ad_details['City'] = location[0]
                    ad_details['Country'] = location[1]
                else:
                    ad_details['City'] = None
                    ad_details['Country'] = location[0]

            elif current_property.find(self.properties_name['views']) != -1:
                views = property_divs.xpath('.//div[%d]/div[2]/text()' % div).get()
                ad_details['views'] = int(views)
            elif current_property.find(self.properties_name['interested']) != -1:
                interested = property_divs.xpath('.//div[%d]/div[2]/text()'  % div).get()
                interested = [str(i) for i in interested.split() if i.isdigit()]
                ad_details['interested'] = int(''.join(interested))

            elif current_property.find(self.properties_name['uploadedDatetime']) != -1:
                ad_details['uploadedDatetime'] = property_divs.xpath('.//div[8]/div[2]/time/@datetime').get()

        price = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[1]/div[1]/span/div/text()').get()
        ad_details['price'] = float(price.replace(',', '.')[:-2])
        
        description = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[2]/script/text()').get()
        description = json.loads(description)
        ad_details['title'] = description['content']['title']
        ad_details['description'] = description['content']['description']
        ad_details['itemId'] = description['itemId']
        ad_details['userName'] = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[2]/div[1]/div[2]/div[1]/h4/span/span/a/text()').get()

        #response.xpath('/text()').get()
        #response.xpath('/text()').get()

        yield ad_details
 
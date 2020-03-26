# -*- coding: utf-8 -*-
import scrapy
import re


class VintedadSpider(scrapy.Spider):
    name = 'VintedAd'
    allowed_domains = ['vinted.fr']

    last_ad = False
    base_url = 'https://www.vinted.fr/vetements?'

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
        
        price = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[1]/div[1]/text()').get()
        ad_details['price'] = price.replace(',', '.')[:-2]
        
        ad_details['brand'] = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[1]/div[2]/a/span/text()').get()

        size = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[2]/div[2]/text()').get()
        ad_details['size'] = re.sub(' +', ' ',size.replace('\n', ''))

        ad_details['condition'] = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[3]/div[2]/text()').get()
        
        colors = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[4]/div[2]/text()').get()
        ad_details['colors'] = colors.split(', ')

        location = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[5]/div[2]/text()').get()
        location = location.replace(' ','').replace('\n', '').split(',')
        if len(location) == 2:
            ad_details['City'] = location[0]
            ad_details['Country'] = location[1]
        else:
            ad_details['City'] = None
            ad_details['Country'] = location[0]
        
        views = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[6]/div[2]/text()').get()
        ad_details['views'] = int(views)

        interested = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[7]/div[2]/text()').get()
        interested = [str(i) for i in interested.split() if i.isdigit()]
        ad_details['interested'] = int(''.join(interested))

        ad_details['uploadedDatetime'] = response.xpath('/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[1]/div[2]/div[8]/div[2]/time/@datetime').get()

        #/html/body/div[4]/div/section/div/div[2]/main/aside/div[1]/div[2]/div[1]/div/div/div/div[1]/span
        #response.xpath('/text()').get()
        #response.xpath('/text()').get()

        yield ad_details
 
# -*- coding: utf-8 -*-
import scrapy


class VintedadSpider(scrapy.Spider):
    name = 'VintedAd'
    allowed_domains = ['vinted.fr']

    last_ad = False
    base_url = 'https://www.vinted.fr/vetements?'

    def start_requests(self):
        i = 1
        while last_ad is not True:
            yield scrapy.http.Request(base_url + 'page=%d' % i)

    def parse(self, response):
        for i in range(1, 25):
            ad_url = response.xpath('//*[@id="catalog"]/div[4]/div/div[2]/div[%d]/section/figure/div/a/@href' % i).get()
            if ad_url is not None:
                yield response.follow(ad_url, callback=self.parse_ad)
            else:
                self.parse_ad = True
                break
    def parse_ad(self, response):
        print(response.xpath('//*[@id="ItemDescription-react-component-33aefb57-93c6-4f7a-8340-e2e589e587ec"]/div/div/div/div[1]/span/text()').get())
 
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PyntedscrapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Ad(scrapy.Item):
    itemId = scrapy.Field()
    url = scrapy.Field()

    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()

    brand = scrapy.Field()
    size = scrapy.Field()
    condition = scrapy.Field()
    color = scrapy.Field()
    City = scrapy.Field()
    Country = scrapy.Field()
    views = scrapy.Field()
    interested = scrapy.Field()
    uploadedDatetime = scrapy.Field()
    
    userId = scrapy.Field()
    userName = scrapy.Field()
    lastSeen = scrapy.Field()
    nbRating = scrapy.Field()
    rate = scrapy.Field()
    
    
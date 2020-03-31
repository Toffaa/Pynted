# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

import w3lib.html

#input_processor=MapCompose()
class Ad(scrapy.Item):
    itemId = scrapy.Field()
    url = scrapy.Field()

    title = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(lambda x: x.replace(',', '.'), float)
    )

    brand = scrapy.Field()
    size = scrapy.Field(
        input_processor=MapCompose(w3lib.html.strip_html5_whitespace),
    )
    condition = scrapy.Field()
    color = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    views = scrapy.Field(
        input_processor=MapCompose(int)
    )
    interested = scrapy.Field(
        input_processor=MapCompose(int)
    )
    uploadedDatetime = scrapy.Field()
    
    userId = scrapy.Field()
    userName = scrapy.Field()
    lastSeen = scrapy.Field()
    nbRating = scrapy.Field(
        input_processor=MapCompose(int)
    )
    rate = scrapy.Field(
        input_processor=MapCompose(int)
    )

    reserved = scrapy.Field()
    daysLeft = scrapy.Field(
        input_processor=MapCompose(int)
    )



    
    
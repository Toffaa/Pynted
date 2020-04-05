import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst

class AdLoader(ItemLoader):
    default_output_processor = TakeFirst()
import scrapy.loader
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from price_parser import Price


def get_price(raw_price):
    price = Price.fromstring(raw_price)
    return price.amount


class TestProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in = MapCompose(str.strip, str.lower)
    price_in = MapCompose(get_price)

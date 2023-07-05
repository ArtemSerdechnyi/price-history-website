from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from price_parser import Price
from Scrapy.grocery_stores.items import Product, ProductUpdate


def get_price(raw_price):
    price = Price.fromstring(raw_price)
    return price.amount


class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in = MapCompose(str.strip)
    price_in = MapCompose(get_price)


class ProductUpdateLoader(ItemLoader):
    default_output_processor = TakeFirst()

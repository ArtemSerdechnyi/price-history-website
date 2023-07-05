from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from price_parser import Price
from Scrapy.grocery_stores.items import Product
from ._base import ProductLoader, ProductUpdateLoader


def weight_from_name(weight: str):
    if weight is not None:
        return weight.strip()


class CreateProductLoader(ProductLoader):
    ...


class UpdateProductLoader(ProductUpdateLoader):
    ...

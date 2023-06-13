# Define here the models for your scraped items
from django.db import models

# See documentation in: import models

# See documentation in:
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    shop_id = scrapy.Field()
    category_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    image_path = scrapy.Field()
    weight = scrapy.Field()
    unit = scrapy.Field()
    description = scrapy.Field()
    composition = scrapy.Field()


class ProductPriceHistory(scrapy.Item):
    product_id = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    date = scrapy.Field()


class GroceryStoresItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=None, output_processor=None)
    pass

import scrapy


class TestItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field(default=2)
    price = scrapy.Field()


class Product(scrapy.Item):
    shop_id = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    raw_name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    image_path = scrapy.Field()
    weight = scrapy.Field()
    unit = scrapy.Field()
    description = scrapy.Field()
    composition = scrapy.Field()
    country = scrapy.Field()
    calories = scrapy.Field()
    carbohydrates = scrapy.Field()
    fats = scrapy.Field()
    proteins = scrapy.Field()


class ProductUpdate(scrapy.Item):
    product_id = scrapy.Field()
    raw_price = scrapy.Field()
    price = scrapy.Field()
    raw_old_price = scrapy.Field()
    old_price = scrapy.Field()
    date = scrapy.Field()

from Scrapy.grocery_stores.items import Product
from ._base_selector import BaseSelector

from dataclasses import dataclass


@dataclass(frozen=True, eq=False, slots=True)
class NovusSelector(BaseSelector):
    subcategory_list: str
    products_list: str


@dataclass(frozen=True, eq=False, slots=True)
class PriceXpath:
    selector_xpath: str
    alternative_xpath: str


@dataclass(frozen=True, eq=False, slots=True)
class NovusXpath(NovusSelector):
    subcategory_list: str = "//div[@class='subcategories-list__item']/a/@href"
    products_list: str = "//a[@class='base-is-link base-card catalog-products__item']"
    product: Product = Product(name=".//p[@class='base-card__label regular p2']/text()",
                               product_url="./@href",
                               image_url=".//img[@class='base-image__img']/@src",
                               price=PriceXpath(
                                   selector_xpath=".//p[@class='base-card__price-current']/text()",
                                   alternative_xpath=".//p[@class='base-card__price-current "
                                                     "base-card__price-current_red']/text()"),
                               full_price=".//p[@class='base-card__price-old p3']/text()",
                               capacity=".//p[@class='base-card__capacity p3']/text()")


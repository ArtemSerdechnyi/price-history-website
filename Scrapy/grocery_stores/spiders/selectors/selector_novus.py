from ..spidertools import Product

from _base_selector import BaseSelector
from dataclasses import dataclass


@dataclass(frozen=True, eq=False, slots=True)
class NovusSelector(BaseSelector):
    subcategory_list: str
    partial_url_product_list: str


@dataclass(frozen=True, eq=False, slots=True)
class NovusXpath(NovusSelector):
    subcategory_list = "//div[@class='subcategories-list__item']/a/@href"
    partial_url_product_list = "//a[@class='base-is-link base-card catalog-products__item']/@href"
    product = Product(name="//h1[@class='product-card__label h3']/text()",
                      product_url=None,
                      image_url=
                      "//div[@class='base-slider product-card__slider']"
                      "//img[@class='base-image__img']/@src",
                      price={'selector_xpath':
                                 "//p[@class='product-card__price-current h4 product-card__price-current_red']/text()",
                             'alternative_xpath':
                                 "//p[@class='product-card__price-current h4']/text()"},
                      full_price=
                      "//div[@class='product-card__price-inner']//p[1]/text()",
                      product_weight=None,  # get from name
                      unit=None,  # get from name
                      brand=
                      "//div[@class='product-additional__parameter-item']/*[contains(text(),'Бренд')]"
                      "/following-sibling::*/text()",
                      country=
                      "//div[@class='product-additional__parameter-item']/*[contains(text(),'Країна')]"
                      "/following-sibling::*/text()",
                      expiration_date=
                      "//div[@class='product-additional__parameter-item']"
                      "/*[contains(text(),'Термін придатності')]"
                      "/following-sibling::*/text()",
                      calories=
                      "//div[@class='product-additional__parameter']"
                      "//*[contains(text(),'Калорійність')]//following-sibling::*/text()",
                      protein=
                      "//div[@class='product-additional__parameter']"
                      "//*[contains(text(),'Білки')]//following-sibling::*/text()",
                      fats=
                      "//div[@class='product-additional__parameter']"
                      "//*[contains(text(),'Жири')]//following-sibling::*/text()",
                      carbohydrates=
                      "//div[@class='product-additional__parameter']"
                      "//*[contains(text(),'Вуглеводи')]//following-sibling::*/text()",
                      composition=
                      "//p[@class='p1']/text()"
                      )

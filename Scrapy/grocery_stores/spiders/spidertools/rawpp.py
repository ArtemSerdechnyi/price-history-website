import logging
from scrapy.http import Response
from abc import ABC, abstractmethod
from typing import Optional


class RawProductParser(ABC):

    def __init__(self, response: Response):
        self.response: Response = response

    def __get_item(self, item_name: str, selector_xpath: str = None, selector_css: str = None) -> str | None:
        if selector_xpath is not None:
            item: str = self.response.xpath(selector_xpath).get()
            selector = selector_xpath
        elif selector_css is not None:
            item: str = self.response.css(selector_css).get()
            selector = selector_css
        else:
            raise AttributeError('Selector not found')

        if item is not None:
            return item
        else:
            logging.log(logging.DEBUG, f'{item_name} not found in URL: {self.response.url}\nSelector: {selector}')

    def get_item(self, item_name: str, selector_xpath: str = None,
                 selector_css: str = None, strip: bool = True) -> str | None:
        item: str = self.__get_item(item_name, selector_xpath, selector_css)
        if strip is True and item is not None:
            return item.strip()
        else:
            return item

    @staticmethod
    def get_marketplace(marketplace: str) -> str:
        return marketplace

    def get_name(self, selector_xpath: str = None,
                 selector_css: str = None,
                 item: str = 'name') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_product_url(self) -> str:
        return self.response.url

    def get_price(self, selector_xpath: str = None,
                  selector_css: str = None,
                  item: str = 'price') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_full_price(self, selector_xpath: str = None,
                       selector_css: str = None,
                       item: str = 'full_price') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_unit(self, selector_xpath: str = None,
                 selector_css: str = None,
                 item: str = 'unit') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_image_url(self, selector_xpath: str = None,
                      selector_css: str = None,
                      item: str = 'image_url') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_product_weight(self, selector_xpath: str = None,
                           selector_css: str = None,
                           item: str = 'product_weight') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_brand(self, selector_xpath: str = None,
                  selector_css: str = None,
                  item: str = 'brand') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_country(self, selector_xpath: str = None,
                    selector_css: str = None,
                    item: str = 'country') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_expiration_date(self, selector_xpath: str = None,
                            selector_css: str = None,
                            item: str = 'expiration_date') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_calories(self, selector_xpath: str = None,
                     selector_css: str = None,
                     item: str = 'calories') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_protein(self, selector_xpath: str = None,
                    selector_css: str = None,
                    item: str = 'protein') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_fats(self, selector_xpath: str = None,
                 selector_css: str = None,
                 item: str = 'fats') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_carbohydrates(self, selector_xpath: str = None,
                          selector_css: str = None,
                          item: str = 'carbohydrates') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

    def get_composition(self, selector_xpath: str = None,
                        selector_css: str = None,
                        item: str = 'composition') -> str | None:
        return self.get_item(item, selector_xpath, selector_css)

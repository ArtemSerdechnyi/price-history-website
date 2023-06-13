import logging

from scrapy import Selector
from scrapy.http import Response
from abc import ABC, abstractmethod
from typing import Optional


class RawProductParser(ABC):

    def __init__(self, response: Response, selector: Selector = None):
        self.response: Response = response
        self.selector: Selector = selector

    def __get_all_items(self, item_name: str, selector_xpath: str = None) -> list[str | None]:
        if selector_xpath is not None:
            if self.selector is not None:
                items: list[str] = self.selector.xpath(selector_xpath).getall()
                print(self.selector)
            else:
                items: list[str] = self.response.xpath(selector_xpath).getall()
        else:
            raise AttributeError('Selector not found')
        if items:
            return items
        else:
            logging.log(logging.DEBUG, f'{item_name} not found in URL: {self.response.url}\n'
                                       f'Xpath selector: {selector_xpath}')
        return []

    def _get_all_items(self, item_name: str,
                       selector_xpath: str = None,
                       strip: bool = True) -> list[str | None]:
        items: list[str | None] = self.__get_all_items(item_name=item_name,
                                                       selector_xpath=selector_xpath)
        if strip is True and items:
            return [item.strip() if item is not None else item for item in items]
        else:
            return items

    def __get_item(self, item_name: str, selector_xpath: str = None) -> str | None:
        if selector_xpath is not None:
            if self.selector is not None:
                item: str = self.selector.xpath(selector_xpath).get()
            else:
                item: str = self.response.xpath(selector_xpath).get()
        else:
            raise AttributeError('Selector not found')

        if item is not None:
            return item
        else:
            logging.log(logging.DEBUG, f'{item_name} not found in URL: {self.response.url}\n'
                                       f'Xpath selector: {selector_xpath}')

    def _get_item(self, item_name: str,
                  selector_xpath: str = None,
                  strip: bool = True) -> str | None:
        item: str | None = self.__get_item(item_name=item_name,
                                           selector_xpath=selector_xpath)
        if strip is True and item is not None:
            return item.strip()
        else:
            return item

    @staticmethod
    def get_marketplace(marketplace: str) -> str:
        return marketplace

    def get_name(self, selector_xpath: str = None,
                 item: str = 'name') -> str | None:
        return self._get_item(item, selector_xpath)

    def get_product_url(self) -> str:
        return self.response.url

    def get_price(self, selector_xpath: str = None,
                  item: str = 'price') -> str | None:
        return self._get_item(item, selector_xpath)

    def get_full_price(self, selector_xpath: str = None,
                       item: str = 'full_price') -> str | None:
        return self._get_item(item, selector_xpath)

    def get_image_url(self, selector_xpath: str = None,
                      item: str = 'image_url') -> str | None:
        return self._get_item(item, selector_xpath)

    def get_capacity(self, selector_xpath: str = None,
                     item: str = 'capacity') -> str | None:
        return self._get_item(item, selector_xpath)

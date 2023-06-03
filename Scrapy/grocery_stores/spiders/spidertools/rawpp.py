from scrapy.http import Response
from abc import ABC


class RawProductParser(ABC):

    def __init__(self, response: Response):
        self.response: Response = response

    @staticmethod
    def get_marketplace(marketplace: str) -> str:
        return marketplace

    @staticmethod
    def get_name(name: str) -> str:
        return name

    def get_product_url(self) -> str:
        return self.response.url

    def get_item(self, selector_xpath: str = None, selector_css: str = None) -> str:
        if selector_xpath is not None:
            item: str = self.response.xpath(selector_xpath).get()
            selector = selector_xpath
        elif selector_css is not None:
            item: str = self.response.css(selector_css).get()
            selector = selector_css
        else:
            raise AttributeError('Selector not found')

        if not item:
            raise Exception(f'Item not found in URL: {self.response.url}\nSelector: {selector}')
        return item.strip()

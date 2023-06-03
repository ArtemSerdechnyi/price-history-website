from ..spidertools.rawpp import RawProductParser


class NovusParser(RawProductParser):

    def get_image_url(self, selector_xpath: str = None, selector_css: str = None,
                      item: str = 'image_url') -> str | None:
        tail = self.get_item(item, selector_xpath, selector_css)
        if tail is not None:
            return self.response.urljoin(tail)

    def get_price(self, selector_xpath: str = None, selector_css: str = None,
                  alternative_xpath: str = None, alternative_css: str = None,
                  item: str = 'price') -> str | None:
        price = self.get_item(item, selector_xpath, selector_css)
        if price is not None:
            return price
        elif alternative_xpath or alternative_css:
            price = self.get_item(item, alternative_xpath, alternative_css)
            return price

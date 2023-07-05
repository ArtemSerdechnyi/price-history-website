from ._rawpp import RawProductParser


class NovusParser(RawProductParser):

    def get_name(self, selector_xpath: str = None,
                 item: str = 'name') -> str | None:
        name: str | None = self._get_item(item, selector_xpath)
        return name

    def get_image_url(self, selector_xpath: str = None,
                      item: str = 'image_url') -> str | None:
        tail = self._get_item(item, selector_xpath)
        if tail is not None:
            return self.response.urljoin(tail)

    def get_product_url(self, selector_xpath: str = None,
                        item: str = 'product_url') -> str | None:
        tail = self._get_item(item, selector_xpath)
        if tail is not None:
            return self.response.urljoin(tail)

    def get_price(self, selector_xpath: str = None,
                  alternative_xpath: str = None,
                  item: str = 'price') -> str | None:
        price = self._get_item(item, selector_xpath)
        if price is not None:
            return price
        elif alternative_xpath:
            price = self._get_item(item, alternative_xpath)
            return price

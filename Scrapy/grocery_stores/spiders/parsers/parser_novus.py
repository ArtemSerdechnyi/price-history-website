from ..spidertools.rawpp import RawProductParser


class NovusParser(RawProductParser):

    def get_price(self, selector_xpath: str = None, selector_css: str = None):
        if selector_xpath is not None:
            price: str = self.response.xpath(selector_xpath).get()
            selector = selector_xpath
        elif selector_css is not None:
            price: str = self.response.css(selector_css).get()
            selector = selector_css
        else:
            raise AttributeError('Selector not found')

        if price:
            if len(price) == 1:
                return price[0]
            elif len(price) == 3:
                return price[2]
        else:
            raise Exception(f'Price not found in URL: {self.response.url}\nSelector: {selector}')

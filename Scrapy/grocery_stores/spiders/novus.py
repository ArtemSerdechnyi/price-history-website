import scrapy
import logging
from scrapy_splash import SplashRequest

from .spidertools import UtilitySpider
from Scrapy.grocery_stores.spiders.spidertools.selectors import NovusXpath


class NovusSpider(scrapy.Spider, UtilitySpider):
    name = "novus"
    allowed_domains = ["novus.online"]
    # start_urls = NOVUS_START_URLS
    start_urls = ['https://novus.online/category/ovochi-frukty-ta-horikhy']

    @staticmethod
    def __next_page(url: str) -> str:
        if 'page-' in url:
            split_url = url.rsplit("-", 1)
            page_num = int(split_url[-1])
            page_num += 1
            return f'{split_url[0]}-{page_num}'
        else:
            return f'{url}/page-2'

    def start_requests(self) -> SplashRequest:
        for url_category in self.start_urls:
            yield SplashRequest(url=url_category,
                                callback=self.parse_url_subcategory,
                                args={'lua_source': self.lua_script,
                                      'wait': self._WAIT},
                                meta={'url_category': url_category})

    def parse_url_subcategory(self, response: scrapy.http.Response) -> scrapy.Request:
        subcategory_list = response.xpath(NovusXpath().subcategory_list).getall()
        for subcategory in subcategory_list:
            subcategory_url = response.urljoin(subcategory)
            yield SplashRequest(url=subcategory_url,
                                callback=self.parse_subcategory_page_recursive,
                                args={'lua_source': self.lua_script,
                                      'wait': self._WAIT},
                                meta={'url_category': response.meta.get('url_category'),
                                      'url_subcategory': subcategory_url})

    def parse_subcategory_page_recursive(self, response: scrapy.http.Response):
        if products_list := response.xpath(NovusXpath().products_list):
            xp_p = NovusXpath().product
            for product_card in products_list:
                name = product_card.xpath(xp_p.name)




                # pp = ParserProduct(response=response, selector=product_card)
                # xp_p = Xpath().product
                # product_raw: RawProduct = RawProduct(
                #     marketplace='Novus',
                #     name=pp.get_name(selector_xpath=xp_p.name),
                #     product_url=pp.get_product_url(selector_xpath=xp_p.product_url),
                #     image_url=pp.get_image_url(selector_xpath=xp_p.image_url),
                #     price=pp.get_price(selector_xpath=xp_p.price.selector_xpath,
                #                        alternative_xpath=xp_p.price.alternative_xpath),
                #     full_price=pp.get_full_price(selector_xpath=xp_p.full_price),
                #     capacity=pp.get_capacity(selector_xpath=xp_p.capacity),
                # )
                # yield product_raw

            yield SplashRequest(url=self.__next_page(response.url),
                                callback=self.parse_subcategory_page_recursive,
                                args={'lua_source': self.lua_script,
                                      'wait': self._WAIT},
                                meta={'url_category': response.meta.get('url_category'),
                                      'url_subcategory': response.meta.get('url_subcategory')})
        else:
            logging.log(logging.DEBUG, f'Category ended : {response.url}')

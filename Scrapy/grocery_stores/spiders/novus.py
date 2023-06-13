import scrapy
import logging
from scrapy_splash import SplashRequest

from .spidertools import UtilitySpider, RawProduct
from .parsers import NovusParser as ParserProduct
from .selectors import NovusXpath as Xpath


class NovusSpider(scrapy.Spider, UtilitySpider):
    name = "novus"
    allowed_domains = ["novus.online"]
    # start_urls_category = ('https://novus.online/category/ovochi-frukty-ta-horikhy',
    #                        'https://novus.online/category/molocne-ajca-sir',
    #                        'https://novus.online/category/maso-riba',
    #                        'https://novus.online/category/bakalia',
    #                        'https://novus.online/category/zootovari',
    #                        'https://novus.online/category/solodosi-sneki',
    #                        'https://novus.online/category/napoi',
    #                    -    'https://novus.online/category/zamorozeni-produkti',
    #                        'https://novus.online/category/alkogol'
    #                        'https://novus.online/category/tutunovi-virobi-ta-aksesuari')
    start_urls_categories = ['https://novus.online/category/ovochi-frukty-ta-horikhy']
    custom_settings = {
        'PLAYWRIGHT_ABORT_REQUEST': lambda request:
        False if request.method == 'GET' and request.resource_type in {
            'script', 'txt', 'document'
        } else True
    }

    @staticmethod
    def next_page(url: str) -> str:
        if url.endswith("/"):
            return url + "page-2"
        else:
            parts = url.rsplit("/", 1)
            if parts[-1].startswith("page-"):
                page_num = int(parts[-1].split("-")[-1])
                new_page_num = page_num + 1
                return parts[0] + "/page-" + str(new_page_num)
            else:
                return url + "/page-2"

    def start_requests(self) -> SplashRequest:
        for url_category in self.start_urls_categories:
            yield from self.request_splash(url=url_category,
                                           callback=self.parse_url_subcategory)

    def parse_url_subcategory(self, response: scrapy.http.Response) -> scrapy.Request:
        subcategory_list = response.xpath(Xpath().subcategory_list).getall()
        for subcategory in subcategory_list:
            if not subcategory:
                logging.log(logging.ERROR, f'Subcategory is not exist: {subcategory}\n'
                                           f'Subcategory URL: {response.url}')
            subcategory_url = response.urljoin(subcategory)
            yield from self.request_splash(url=subcategory_url,
                                           callback=self.parse_subcategory_page_recursive)

    def parse_subcategory_page_recursive(self, response: scrapy.http.Response):
        products_list: list[scrapy.Selector] = response.xpath(Xpath().products_list)
        if products_list:
            for product_card in products_list:
                pp = ParserProduct(response=response, selector=product_card)
                xp_p = Xpath().product
                product_raw: RawProduct = RawProduct(
                    marketplace='Novus',
                    name=pp.get_name(selector_xpath=xp_p.name),
                    product_url=pp.get_product_url(selector_xpath=xp_p.product_url),
                    image_url=pp.get_image_url(selector_xpath=xp_p.image_url),
                    price=pp.get_price(selector_xpath=xp_p.price.selector_xpath,
                                       alternative_xpath=xp_p.price.alternative_xpath),
                    full_price=pp.get_full_price(selector_xpath=xp_p.full_price),
                    capacity=pp.get_capacity(selector_xpath=xp_p.capacity),
                )
                

            yield from self.request_splash(url=self.next_page(response.url),
                                           callback=self.parse_subcategory_page_recursive)
        else:
            logging.log(logging.DEBUG, f'Category ended : {response.url}')

import scrapy
import logging
from scrapy_splash import SplashRequest

from .spidertools import UtilitySpider, RawProduct
from .parsers import NovusParser as ParserProduct


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
    #                        'https://novus.online/category/zamorozeni-produkti',
    #                        'https://novus.online/category/alkogol'
    #                        'https://novus.online/category/tutunovi-virobi-ta-aksesuari')
    start_urls_category = ['https://novus.online/category/ovochi-frukty-ta-horikhy',
                           'https://novus.online/category/maso-riba']
    custom_settings = {
        'PLAYWRIGHT_ABORT_REQUEST': lambda request:
        False if request.method == 'GET' and request.resource_type in {
            'script', 'txt', 'document'
        } else True
    }

    @staticmethod
    def add_pagination(url: str, page: int) -> str:
        if page > 1:
            return f'{url}/page-{page}'
        return url

    def start_requests(self) -> SplashRequest:
        for url_category in self.start_urls_category:
            yield from self.request_splash(url=url_category,
                                           callback=self.parse_url_subcategory)

    def parse_url_subcategory(self, response: scrapy.http.Response) -> scrapy.Request:
        subcategory_list = response.xpath("//div[@class='subcategories-list__item']/a/@href").getall()
        for subcategory in subcategory_list:
            subcategory_url = response.urljoin(subcategory)
            yield from self.request_pw(url=subcategory_url,
                                       callback=self.parse_subcategory_first_page)

    def parse_subcategory_first_page(self, response: scrapy.http.Response):
        # parse product in first page
        self.parse_url_product(response=response)

        # parse all next pages
        last_page_number: str | None = response.xpath(
            "//div[@class='base-pagination__breakpoint base-pagination__end']"
            "//a[@class='base-is-link base-pagination__item p2']/text()").get()
        if last_page_number is None:
            last_page_number: str | None = response.xpath(
                "//a[@class='base-is-link base-pagination__item p2'][last()]/text()").get()
        if last_page_number is not None:
            last_page_number: int = int(last_page_number.strip())
            subcategory_url = response.url
            for page in range(2, last_page_number + 1):
                subcategory_page_url = self.add_pagination(url=subcategory_url, page=page)
                print(subcategory_page_url, '---------')
                yield from self.request_splash(url=subcategory_page_url,
                                               callback=self.parse_url_product)

    def parse_url_product(self, response: scrapy.http.Response):
        partial_product_url_list = response.xpath(
            "//a[@class='base-is-link base-card catalog-products__item']/@href").getall()
        product_url_list = map(response.urljoin, partial_product_url_list)
        for product_url in product_url_list:
            yield from self.request_splash(url=product_url,
                                           callback=self.parse_product)

    def parse_product(self, response: scrapy.http.Response):
        pp = ParserProduct(response)

        product_raw: RawProduct = RawProduct(
            marketplace=pp.get_marketplace('Novus'),
            name=pp.get_name(selector_xpath=
                             "//h1[@class='product-card__label h3']/text()"),
            product_url=pp.get_product_url(),
            image_url=pp.get_image_url(selector_xpath=
                                       "//div[@class='base-slider product-card__slider']"
                                       "//img[@class='base-image__img']/@src"),
            price=pp.get_price(selector_xpath=
                               "//p[@class='product-card__price-current h4 product-card__price-current_red']/text()",
                               alternative_xpath=
                               "//p[@class='product-card__price-current h4']/text()"),
            full_price=pp.get_full_price(selector_xpath=
                                         "//div[@class='product-card__price-inner']//p[1]/text()"),
            product_weight=None,  # get from name
            brand=pp.get_brand(selector_xpath=
                               "//div[@class='product-additional__parameter-item']/*[contains(text(),'Бренд')]"
                               "/following-sibling::*/text()"),
            country=pp.get_country(selector_xpath=
                                   "//div[@class='product-additional__parameter-item']/*[contains(text(),'Країна')]"
                                   "/following-sibling::*/text()"),
            expiration_date=pp.get_expiration_date(selector_xpath=
                                                   "//div[@class='product-additional__parameter-item']"
                                                   "/*[contains(text(),'Термін придатності')]"
                                                   "/following-sibling::*/text()"),
            calories=pp.get_calories(selector_xpath=
                                     "//div[@class='product-additional__parameter']"
                                     "//*[contains(text(),'Калорійність')]//following-sibling::*/text()"),
            protein=pp.get_protein(selector_xpath=
                                   "//div[@class='product-additional__parameter']"
                                   "//*[contains(text(),'Білки')]//following-sibling::*/text()"),
            fats=pp.get_fats(selector_xpath=
                             "//div[@class='product-additional__parameter']"
                             "//*[contains(text(),'Жири')]//following-sibling::*/text()"),
            carbohydrates=pp.get_carbohydrates(selector_xpath=
                                               "//div[@class='product-additional__parameter']"
                                               "//*[contains(text(),'Вуглеводи')]//following-sibling::*/text()"),
            composition=pp.get_composition(selector_xpath=
                                           "//p[@class='p1']/text()")
        )

        print(product_raw)

import scrapy
from scrapy_splash import SplashRequest
from .spidertools import UtilitySpider, RawProduct
from .parsers import NovusParser as Parser


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
            print(url_category, 'url_category--------------')
            yield from self.request_splash(url=url_category,
                                           callback=self.parse_url_subcategory)

    def parse_url_subcategory(self, response: scrapy.http.Response) -> scrapy.Request:
        subcategory_list = response.xpath("//div[@class='subcategories-list__item']/a/@href").getall()
        for subcategory in subcategory_list:
            print(subcategory, 'subcategory--------------')
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
        if last_page_number is not None:
            last_page_number: int = int(last_page_number.strip())
            subcategory_url = response.url
            for page in range(2, last_page_number + 1):
                subcategory_page_url = self.add_pagination(url=subcategory_url, page=page)
                print(subcategory_page_url, 'subcategory_page_url--------------')
                yield from self.request_splash(url=subcategory_page_url,
                                               callback=self.parse_url_product)

    def parse_url_product(self, response: scrapy.http.Response):
        partial_product_url_list = response.xpath(
            "//a[@class='base-is-link base-card catalog-products__item']/@href").getall()
        product_url_list = map(response.urljoin, partial_product_url_list)
        for product_url in product_url_list:
            print(product_url)
            yield from self.request_splash(url=product_url,
                                           callback=self.parse_product)

    def parse_product(self, response: scrapy.http.Response):

        parse = Parser(response)

        product: RawProduct = RawProduct(
            marketplace='Novus',
            name=response.xpath(
                "//h1[@class='product-card__label h3']/text()").get(),
            product_url=response.url,
            image_url=response.urljoin(
                response.xpath("//div[@class='base-slider product-card__slider']"
                               "//img[@class='base-image__img']/@src").get()),
            price=get_price(response=response),
            full_price=response.xpath("//div[@class='product-card__price-inner']//p[1]").get(),
            brand=response.xpath(
                "//div[@class='product-additional__parameter-item']/*[contains(text(),'Бренд')]"
                "/following-sibling::*/text()").get(),
            country=response.xpath(
                "//div[@class='product-additional__parameter-item']/*[contains(text(),'Країна')]"
                "/following-sibling::*/text()").get(),
            expiration_date=response.xpath(
                "//div[@class='product-additional__parameter-item']/*[contains(text(),'Термін придатності')]"
                "/following-sibling::*/text()").get(),
            calories=response.xpath(
                "//div[@class='product-additional__parameter']"
                "//*[contains(text(),'Калорійність')]//following-sibling::*/text()").get(),
            protein=response.xpath(
                "//div[@class='product-additional__parameter']"
                "//*[contains(text(),'Білки')]//following-sibling::*/text()").get(),
            fats=response.xpath(
                "//div[@class='product-additional__parameter']"
                "//*[contains(text(),'Жири')]//following-sibling::*/text()").get(),
            carbohydrates=response.xpath(
                "//div[@class='product-additional__parameter']"
                "//*[contains(text(),'Вуглеводи')]//following-sibling::*/text()").get(),
            composition=response.xpath(
                "//p[@class='p1']/text()").get()
        )


        print(product)

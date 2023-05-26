import scrapy
from scrapy_splash import SplashRequest

from .common import DefaultSpider


class NovusSpider(scrapy.Spider, DefaultSpider):
    name = "sp_novus"
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
    start_urls_category = ('https://novus.online/category/ovochi-frukty-ta-horikhy',
                           'https://novus.online/category/maso-riba')

    @staticmethod
    def add_page_to_url(url: str):
        page_number = 1
        page_pattern = ''
        for _ in range(999):
            if page_number > 1:
                page_pattern = f'/page-{page_number}'
            yield f'{url}{page_pattern}'
            page_number += 1
        raise StopIteration(f'Page number is over 999 for {url}!')

    def start_requests(self) -> SplashRequest:
        for url_category in self.start_urls_category:
            yield from self.splash_request(url_s=url_category,
                                           callback=self.parse_url_subcategory)

    def parse_url_subcategory(self, response: scrapy.http.Response) -> SplashRequest:
        subcategory_list = response.xpath("//div[@class='subcategories-list__item']/a/@href").getall()
        for subcategory in subcategory_list:
            subcategory_url = response.urljoin(subcategory)
            yield from self.splash_request(url_s=subcategory_url,
                                           callback=self.parse_subcategory)

    def parse_subcategory(self, response: scrapy.http.Response):
        partial_product_url_list = response.xpath(
            "//a[@class='base-is-link base-card catalog-products__item']/@href").getall()
        product_url_list = map(response.urljoin, partial_product_url_list)
        for product_url in product_url_list:
            yield from self.splash_request(url_s=product_url,
                                           callback=self.parse_subcategory)

    def parse_product(self, response: scrapy.http.Response):
        product_parameters = {}

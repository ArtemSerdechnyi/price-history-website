import scrapy
# from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from _spidertools import SpiderToolsPlaywright as SpiderTools


class NovusSpider(scrapy.Spider, SpiderTools):
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

    COUNT_PRODUCTS = 0

    def start_requests(self) -> SplashRequest:
        for url_category in self.start_urls_category:
            yield SplashRequest(url=url_category,
                                callback=self.parse_url_subcategory,
                                args={'wait': self.WAIT})

    def parse_url_subcategory(self, response: scrapy.http.Response) -> SplashRequest:
        subcategory_list = response.xpath("//div[@class='subcategories-list__item']/a/@href").getall()
        for subcategory in subcategory_list:
            print(subcategory)
            subcategory_url = response.urljoin(subcategory)
            yield SplashRequest(url=subcategory_url,
                                callback=self.parse_subcategory,
                                args={'wait': self.WAIT})

    def parse_subcategory(self, response: scrapy.http.Response):
        ...
        # next_page = response.xpath("//a[@class='base-is-link base-pagination__item p2 nuxt-link-exact-active nuxt-link-active active bold']/following-sibling::*[1]/@href").getall()
        # print('nextpage----', next_page)
        # partial_product_url_list = response.xpath(
        #     "//a[@class='base-is-link base-card catalog-products__item']/@href").getall()
        # product_url_list = map(response.urljoin, partial_product_url_list)
        # for product_url in product_url_list:
        #     print(product_url)
        #     yield SplashRequest(url=product_url,
        #                         callback=self.parse_product,
        #                         args={'wait': self.WAIT})
        #
        # if next_page:
        #     next_page_url = response.urljoin(next_page)
        #     print('next_page_url', next_page_url)
        #     yield from self.splash_request(url_s=next_page_url,
        #                                    callback=self.parse_subcategory)

    def parse_product(self, response: scrapy.http.Response):
        print('COUNT_PRODUCTS', self.COUNT_PRODUCTS)
        self.COUNT_PRODUCTS += 1
        name = response.xpath("//h1[@class='product-card__label h3']/text()").get()
        print(name)

import scrapy
from scrapy_splash import SplashRequest

from .common import DefaultSpider, DefaultLuaSpider


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
                           'https://novus.online/category/molocne-ajca-sir',
                           'https://novus.online/category/maso-riba')

    def start_requests(self):
        for url_category in self.start_urls_category:
            yield from self.splash_request(urls=url_category,
                                           callback=self.get_url_subcategory)

    def get_url_subcategory(self, response: scrapy.http.Response):
        subcategory_list = response.xpath("//div[@class='subcategories-list__item']/a/@href").getall()
        for subcategory in subcategory_list:
            subcategory_url = response.urljoin(subcategory)
            print('-----', subcategory_url)


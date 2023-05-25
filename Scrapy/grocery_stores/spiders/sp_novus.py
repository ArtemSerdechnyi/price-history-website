import scrapy
from scrapy_splash import SplashRequest
from typing import Iterable


class NovusSpider(scrapy.Spider):
    name = "sp_novus"
    allowed_domains = ["novus.online"]
    start_urls_category = ('https://novus.online/category/ovochi-frukty-ta-horikhy',
                           'https://novus.online/category/molocne-ajca-sir',
                           'https://novus.online/category/maso-riba',
                           'https://novus.online/category/bakalia',
                           'https://novus.online/category/zootovari',
                           'https://novus.online/category/solodosi-sneki',
                           'https://novus.online/category/napoi',
                           'https://novus.online/category/zamorozeni-produkti',
                           'https://novus.online/category/alkogol'
                           'https://novus.online/category/tutunovi-virobi-ta-aksesuari')

    lua_get_page_script = """
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            return splash:html()
        end
    """

    def start_requests(self):
        for url_category in self.start_urls_category:
            yield SplashRequest(
                url=url_category,
                callback=self.get_url_subcategory,
                endpoint='execute',
                args={'lua_source': self.lua_get_page_script}
            )

    def get_url_subcategory(self, response: scrapy.http.Response):
        subcategory_list = response.xpath("//div[@class='subcategories-list__item']/a/@href").getall()
        for subcategory in subcategory_list:
            subcategory_url = response.urljoin(subcategory)
            yield

    def parse(self, response):
        print('--' * 20, response)

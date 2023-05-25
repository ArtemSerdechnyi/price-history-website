import scrapy
from scrapy_splash import SplashRequest


class NovusSpider(scrapy.Spider):
    name = "novus.online"
    allowed_domains = ["novus.online"]
    start_urls_category = ['https://novus.online/category/ovochi-frukty-ta-horikhy',
                           'https://novus.online/category/molocne-ajca-sir',
                           'https://novus.online/category/maso-riba',
                           'https://novus.online/category/bakalia',
                           'https://novus.online/category/zootovari',
                           'https://novus.online/category/solodosi-sneki',
                           'https://novus.online/category/napoi',
                           'https://novus.online/category/zamorozeni-produkti',
                           'https://novus.online/category/alkogol'
                           'https://novus.online/category/tutunovi-virobi-ta-aksesuari']

    lua_get_page_script = """
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            return splash:html()
        end
    """

    def start_requests(self):
        yield SplashRequest(
            url='https://novus.online/',
            callback=self.get_url_category,
            endpoint='execute',
            args={'lua_source': self.lua_get_page_script}
        )

    def get_url_category(self, response: scrapy.http.Response):
        category_list = response.xpath("")

    def parse(self, response):
        print('--' * 20, response)

import scrapy
from scrapy_splash import SplashRequest




class TestspiderSpider(DefaultLuaSpider):
    name = "Testspider"
    allowed_domains = ["quotes.toscrape.com"]
    start_url = "https://quotes.toscrape.com/js/"
    lua_script = """
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            return splash:html()
        end
    """

    def start_requests(self, url=start_url):
        yield SplashRequest(url=url,
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': self.lua_script, 'wait': 0.2})

    def parse(self, response: scrapy.http.Response):
        quotes: scrapy.selector.unified.SelectorList = response.xpath("//div[@class='quote']")
        for quote in quotes:
            yield {'autor': quote.xpath(".//small[@class='author']/text()").get(),
                   'text': quote.xpath(".//span[@class='text']/text()").get(),
                   'tags': quote.xpath(".//a[@class='tag']/text()").getall()}

        next_page = quotes.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None:
            url = response.urljoin(next_page)
            yield next(self.start_requests(url=url))

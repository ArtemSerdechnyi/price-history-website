import scrapy
from scrapy_splash import SplashRequest
from typing import Any, Callable, Iterable


class DefaultSpider:
    start_urls: list[str]

    @staticmethod
    def splash_request(urls: Iterable[str] | str,
                       callback: Callable,
                       endpoint: str = 'execute',
                       args: dict[str, Any] = None) -> SplashRequest:
        if args is None:
            args = {'wait': 0.2}
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            yield SplashRequest(url=url,
                                callback=callback,
                                endpoint=endpoint,
                                args=args)

    def parse(self, response: scrapy.http.Response):
        res = response.xpath("//small[@class='author']/text()").getall()
        print(res, '-----')


class DefaultLuaSpider:
    lua_get_page_script = """
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            return splash:html()
        end
    """
    args = {'lua_source': lua_get_page_script}

    def splash_request(self,
                       urls: Iterable[str] | str,
                       callback: Callable,
                       endpoint: str = 'execute',
                       args: dict[str, Any] = None) -> SplashRequest:
        if args is None:
            args = {'lua_source': self.lua_get_page_script}
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            yield SplashRequest(url=url,
                                callback=callback,
                                endpoint=endpoint,
                                args=args)

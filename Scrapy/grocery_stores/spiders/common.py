from scrapy_splash import SplashRequest

from typing import Any, Callable, Iterable


class DefaultSpider:

    @staticmethod
    def splash_request(urls: Iterable[str] | str,
                       callback: Callable,
                       args: dict[str, Any] = None) -> SplashRequest:

        if args is None:
            args = {'wait': 1}
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            yield SplashRequest(url=url,
                                callback=callback,
                                args=args)


class DefaultLuaSpider:

    @staticmethod
    def splash_request(urls: Iterable[str] | str,
                       callback: Callable,
                       endpoint: str = 'execute',
                       args: dict[str, Any] = None) -> SplashRequest:

        lua_get_page_script = """
            function main(splash, args)
                url = args.url
                assert(splash:go(url))
                return splash:html()
            end
        """

        if args is None:
            args = {'lua_source': lua_get_page_script,
                    'wait': 1}
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            yield SplashRequest(url=url,
                                callback=callback,
                                endpoint=endpoint,
                                args=args)

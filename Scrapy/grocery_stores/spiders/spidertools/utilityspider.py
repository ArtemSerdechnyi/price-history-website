import scrapy
from scrapy import Request as ScrapyRequest
from scrapy_splash import SplashRequest

from typing import Callable, Iterable


class UtilitySpider:

    @staticmethod
    def request_splash(url: str,
                       callback: Callable,
                       lua_script: str = None,
                       args: dict = None) -> SplashRequest:
        if lua_script is None:
            lua_script = """
                function main(splash, args)
                    url = args.url
                    assert(splash:go(url))
                    assert(splash:wait(1))
                    return splash:html()
                end
            """
        if args is None:
            args = {}
        endpoint: str = 'execute'
        args.setdefault('wait', 0.5)
        args.setdefault('lua_source', lua_script)
        print('splash_request', url)
        yield SplashRequest(url=url,
                            callback=callback,
                            endpoint=endpoint,
                            args=args)

    @staticmethod
    def request_pw(url: str,
                   callback: Callable) -> ScrapyRequest:
        meta = {'playwright': True}
        print('pw_request', url)
        yield ScrapyRequest(url=url, callback=callback, meta=meta)

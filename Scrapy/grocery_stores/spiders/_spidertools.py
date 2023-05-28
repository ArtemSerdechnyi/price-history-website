from scrapy import Request as ScrapyRequest
from scrapy_splash import SplashRequest

from typing import Callable, Iterable
from abc import ABC, abstractmethod


class SpiderTools(ABC):
    @abstractmethod
    def request(self, *args, **kwargs):
        pass


class SpiderToolsPlaywright(SpiderTools):
    @staticmethod
    def request(url_s: Iterable[str] | str,
                callback: Callable) -> ScrapyRequest:
        meta = {'playwright': True}
        if isinstance(url_s, str):
            url_s = [url_s]
        for url in url_s:
            yield ScrapyRequest(url=url, callback=callback, meta=meta)


class SpiderToolsSplash(SpiderTools):

    @staticmethod
    def request(url_s: Iterable[str] | str,
                callback: Callable) -> SplashRequest:

        args = {'wait': 0.5}
        if isinstance(url_s, str):
            url_s = [url_s]
        for url in url_s:
            yield SplashRequest(url=url,
                                callback=callback,
                                args=args)


class SpiderToolsSplashLua(SpiderTools):
    lua_script = """
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            return splash:html()
        end
    """

    def request(self, url_s: Iterable[str] | str,
                callback: Callable,
                lua_script: str = None) -> SplashRequest:
        if isinstance(url_s, str):
            url_s = [url_s]
        if lua_script is not None:
            self.lua_script = lua_script
        args = {'lua_source': self.lua_script,
                'wait': 0.5}
        for url in url_s:
            yield SplashRequest(url=url,
                                callback=callback,
                                args=args)
        endpoint: str = 'execute'
        args = {'lua_source': self.lua_script,
                'wait': 0.5}
        if isinstance(url_s, str):
            url_s = [url_s]
        for url in url_s:
            yield SplashRequest(url=url,
                                callback=callback,
                                endpoint=endpoint,
                                args=args)

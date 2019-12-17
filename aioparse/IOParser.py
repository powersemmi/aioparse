#!/bin/env python3
from aiolpiogger import Logger
from collections import deque
import asyncio
from asyncio import new_event_loop, get_running_loop, get_event_loop, Future
from typing import List, Tuple, Callable, Awaitable, Any, TypedDict, Generic, AsyncGenerator, AsyncIterable


# init logger


class UrlsFuture(object):
    """Urls future type"""

    def __init__(self, urls: Tuple[str]) -> None:
        self.future = Future()
        self.future.set_result(urls)
        self.urls: tuple = urls
        self.current = deque()

    def __str__(self) -> str:
        return str(self.urls)


class ParserConfig(TypedDict):
    multi_cores: bool


class AIOParse:
    def __init__(self, data: UrlsFuture, parse_handlers: List[Any],
                 **kwargs: ParserConfig) -> None:
        self.parse_handlers = parse_handlers
        self.data: asyncio.Future = asyncio.ensure_future(data.future)
        self.logger: Logger
        self.loop = None

    def __await__(self):
        self.logger.debug("GGVP")

    async def __aenter__(self):
        self.logger = Logger.with_default_handlers(name='IOParser')
        self.logger.debug("GGVP")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.logger.debug("GGVP")
        pass

    async def request(self):
        pass

    async def crawl(self):
        print(await self.data)

    def start(self):
        self.loop = get_event_loop()
        self.loop.run_until_complete(self.crawl())


if __name__ == '__main__':
    async def parse_1st_layer(urls: Any) -> AsyncGenerator[Any, Any]:
        yield await urls


    parse_layers = [parse_1st_layer]
    mytuple: Tuple = tuple("https://google.com" for i in range(5))
    urls: UrlsFuture = UrlsFuture(mytuple)

    new_parse: AIOParse = AIOParse(urls, parse_layers)

    aaa = AIOParse(urls, parse_layers)

    test: UrlsFuture = UrlsFuture(mytuple)


    async def awaiting(var):
        async for i in test:
            print(i)


    test_loop = get_event_loop()
    test_loop.run_until_complete(awaiting(test))

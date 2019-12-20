import asyncio
import os
from asyncio import Future
from concurrent.futures.process import ProcessPoolExecutor
from typing import List, Callable, Dict, Union, Any

import aiohttp
from aiologger import Logger


class AIOParse:
    def __init__(self, root_urls: List[str], parse_funcs: Dict[str, Callable]):
        self.event_loop = asyncio.get_event_loop()
        self.root_urls = root_urls
        self.parse_funcs = parse_funcs
        self.logger = Logger.with_default_handlers()
        self.page = []

    async def parse(self, page: List) -> Union[asyncio.Future[Any], List[str]]:
        self.page[1] = page
        return self.page

    async def request(self, client, url) -> asyncio.Future:
        # time.sleep(0.1)
        self.logger.debug(f"[GET] {url} start")
        if "h" in url:
            while True:
                # await sleep(0.1)
                try:
                    async with client.get(url) as resp:
                        assert resp.status == 200
                        result = await resp.text()
                    self.logger.debug(f"[GET] {url} success")
                    break
                except aiohttp.ClientConnectorError:
                    self.logger.debug(f"[GET] ClientConnectorError {url} ERROR")
                    continue
                except aiohttp.ServerTimeoutError:
                    self.logger.debug(f"[GET] ServerTimeoutError {url} ERROR")
                    continue
        return result

    async def crawl(self, future: Union[List[Union[str, Future[Any]]], Future[Any], Any],
                    client, pool) -> None:
        futures: Any = []
        # Получаем из футуры ссылки
        if isinstance(future, Future):
            urls: Union[Any] = await future
            # Выгребаем для каждой ссылки разметку страницы
            for request_future in asyncio.as_completed([self.request(client, url)
                                                        for url in urls]):
                parse_future: List[Union[Future[Any],
                                         List[str]]] = [await self.parse(await request_future)]

                futures.append(asyncio.ensure_future(self.crawl(parse_future, client, pool)))
            if futures:
                await asyncio.wait(futures)
        elif isinstance(future, List):
            # Выгребаем для каждой ссылки разметку страницы
            for urls in future:
                for request_future in asyncio.as_completed([self.request(client, url)
                                                            for url in urls]):
                    parse_future: List[Union[str, Future[Any]]] = \
                        [await self.parse(await request_future)]

                    futures.append(asyncio.ensure_future(self.crawl(parse_future, client, pool)))
                if futures:
                    await asyncio.wait(futures)
        # else:
        #     pass

    async def main(self):
        # Создаём пул потоков по количеству процессоров
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
            # Создаём клиентскую сессию
            conn = aiohttp.TCPConnector()
            async with aiohttp.ClientSession(connector=conn) as client:
                # Создаём корневую футуру
                initial_future = self.event_loop.create_future()
                # Помещаем в неё ссылки, с которых начнём парсить
                initial_future.set_result(self.root_urls)
                # Передаём эту футуру в сопрограмму обхода
                await self.crawl(initial_future, client, pool)


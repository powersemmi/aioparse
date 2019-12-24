"""
AIOParser
"""
import asyncio
import os
from asyncio import Future
from concurrent.futures.process import ProcessPoolExecutor
from contextlib import suppress
from typing import List, Callable, Dict, Union, Any, AsyncGenerator, Awaitable

import aiohttp
from aiohttp import ClientConnectorError, ServerTimeoutError
from aiologger import Logger
from lxml import html


class AIOParse:
    """
    tralala
    """

    def __init__(self, root_urls: List[str], parse_funcs: Dict[str, Callable]) -> None:
        """
        :param root_urls:
        :param parse_funcs:
        """
        self.event_loop = asyncio.get_event_loop()
        self.root_urls: List[str] = root_urls
        self.parse_funcs: Dict[str, Callable] = parse_funcs
        self.logger = Logger.with_default_handlers()

    async def parse(self, page: Union[str, List[str]]) -> AsyncGenerator[AsyncGenerator[str, None], Any]:
        """
        :param page:
        :return:
        """
        await self.logger.debug(f"[PARSER] START")
        if isinstance(page, str):
            async for i in self.func_runner(page):
                yield i
        elif isinstance(page, List):
            for i in page:
                async for z in self.func_runner(page):
                    yield z
        else:
            await asyncio.sleep(0)

    async def func_runner(self, page) -> Union[AsyncGenerator[str, None], Any]:
        """
        :param page:
        :return:
        """
        tree: html.HtmlElement = html.fromstring(page)
        for key, val in self.parse_funcs.items():
            if tree.xpath(key):
                yield val(page)

    async def request(self, client, url) -> Awaitable[Any]:
        """
        :param client:
        :param url:
        :return:
        """
        # time.sleep(0.1)
        await self.logger.debug(f"[GET] {url} start")
        while True:
            # await sleep(0.1)
            try:
                async with client.get(url) as resp:
                    assert resp.status == 200
                    result: asyncio.Future[Any] = await resp.text()
                await self.logger.debug(f"[GET] {url} success")
                break
            except ClientConnectorError:
                await self.logger.debug(f"[GET] ClientConnectorError {url} ERROR")
                continue
            except ServerTimeoutError:
                await self.logger.debug(f"[GET] ServerTimeoutError {url} ERROR")
                continue
        return result

    async def crawl(self, future: Union[List[Union[str, Awaitable[Any]]], Awaitable[Any], Any],
                    client, pool) -> None:
        """
        :param future:
        :param client:
        :param pool:
        :return:
        """
        futures: Any = []
        # Получаем из футуры ссылки
        if isinstance(future, Future):
            await self.crawl_loop(await future, client, pool, futures)
        elif isinstance(future, List):
            # Выгребаем для каждой ссылки разметку страницы
            for urls_list in future:
                await self.crawl_loop(urls_list, client, pool, futures)

    async def crawl_loop(self, urls_list, client, pool,
                         futures: Any):
        """
        :param urls_list:
        :param client:
        :param pool:
        :param futures:
        :return:
        """
        for request_future in asyncio.as_completed([await self.request(client, url) for url in urls_list]):
            await self.logger.debug("im here")
            parse_future: List[Union[str, List[str]]] = []
            async for i in self.parse(await request_future):
                async for z in i:
                    parse_future.append(z)

            futures.append(asyncio.ensure_future(self.crawl(parse_future, client, pool)))
        if futures:
            await asyncio.wait(futures)

    async def _main(self) -> None:
        """
        :return:
        """
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

    def main(self) -> None:
        """
        :return:
        """
        try:
            self.event_loop.run_until_complete(self._main())
        except KeyboardInterrupt:
            for task in asyncio.Task.all_tasks():
                task.cancel()
                with suppress(asyncio.CancelledError):
                    self.event_loop.run_until_complete(task)
        finally:
            self.event_loop.close()


if __name__ == '__main__':
    async def parser_1st_layer(page: str):
        """
        pass
        :param page:
        :return:
        """
        with open("google_dode.txt", "w", encoding="utf-8") as file:
            file.write("Google is doode")


    URLS = ["https://google.com/", "https://google.com/"]
    FUNCTS = {"//p": parser_1st_layer}
    MAIN = AIOParse(root_urls=URLS, parse_funcs=FUNCTS)

    MAIN.main()

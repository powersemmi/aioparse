import asyncio
import os
from concurrent.futures.process import ProcessPoolExecutor
from typing import Tuple, List, Callable, Dict

from aiologger import Logger
import aiohttp


class AIOParse:
    def __init__(self, root_urls: List[str], parse_funcs: Dict[str, Callable]):
        self.event_loop = asyncio.get_event_loop()
        self.root_urls = root_urls
        self.parse_funcs = parse_funcs
        self.logger = Logger.with_default_handlers()

    async def parse(self, url: str) -> List[str]:
        pass

    async def request(self, client, url):
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
                except:
                    continue
        return result

    async def crawl(self, future: asyncio.Future or List[str], client, pool):
        futures = []
        # Получаем из футуры ссылки
        try:
            urls: List[str] = await future
            # Выгребаем для каждой ссылки разметку страницы
            for request_future in asyncio.as_completed([self.request(client, url) for url in urls]):
                parse_future: asyncio.Future = [await self.parse(await request_future)]

                futures.append(asyncio.ensure_future(self.crawl(parse_future, client, pool)))
            if futures:
                await asyncio.wait(futures)
        except TypeError:
            # Выгребаем для каждой ссылки разметку страницы
            for urls in future:
                for request_future in asyncio.as_completed([self.request(client, url) for url in urls]):
                    parse_future: List[str] = [await self.parse(await request_future)]

                    futures.append(asyncio.ensure_future(self.crawl(parse_future, client, pool)))
                if futures:
                    await asyncio.wait(futures)
        except:
            pass

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
                # Передаём эту футуру в сопрограмму обхода ссылок
                # вместе с пулом потоков и клиентской сессией
                await self.crawl(initial_future, client, pool)


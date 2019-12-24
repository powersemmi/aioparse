#!/usr/bin/env python3

import asyncio
import json
import sys

from websockets import connect


class EchoWebsocket:
    def __await__(self):
        # see: https://stackoverflow.com/a/33420721/1113207
        return self._async_init().__await__()

    async def _async_init(self):
        self._conn = connect('wss://ws.binaryws.com/websockets/v3')
        self.websocket = await self._conn.__aenter__()
        return self

    async def close(self):
        await self._conn.__aexit__(*sys.exc_info())

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()


class mtest:
    async def start(self):
        try:
            self.wws = await EchoWebsocket()
        finally:
            await self.wws.close()

    async def get_ticks(self):
        await self.wws.send(json.dumps({'ticks_history': 'R_50', 'end': 'latest', 'count': 1}))
        return await self.wws.receive()


if __name__ == '__main__':
    a = mtest()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a.start())

#!/bin/env python3.8
# -*- coding: utf-8 -*-

import asyncio
import io
import os
import sys
from concurrent.futures.process import ProcessPoolExecutor
from typing import Iterable


class MyStdOut(io.TextIOBase):
    def __init__(self, orig_stdout=None):
        super().__init__()
        self.orig_stdout = orig_stdout

    def write(self, s):
        # Process output in whatever way you like
        # current_process(s)
        # Write output to original stream, if desired
        if self.orig_stdout:
            self.orig_stdout.write(s)


sys.stdout = MyStdOut(sys.stdout)

loop = asyncio.new_event_loop()


async def awaitable_iterator(data: Iterable):
    for i in data:
        yield i
        await asyncio.sleep(0)


async def main():
    data = [str(i) for i in range(10000000)]
    async for i in awaitable_iterator(data):
        await asyncio.sleep(0)
        sys.stdout.write(i)
        await asyncio.sleep(0)


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
        pool.run_until_complete(main())

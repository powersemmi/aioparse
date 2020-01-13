#!/bin/env python3.8
# -*-coding: utf-8-*-
"""
autor: powersemmi (Chebotarev Victor)
email: powersemmi@gmail.com
telegram: powersemmi
"""
import asyncio
from glob import glob
from typing import List, Dict, Any, Iterator
import re

import aiofiles


class OpenVpn:
    """Singleton open vpn list"""

    def __init__(self) -> None:
        self.char_counter = None
        self.data: List[Dict[str, List[str]]] = []
        self._char_counter: int = 0
        self._status: int = 0
        self._word_counter: int = 0
        self.__conf_list: List[str] = []

    def __new__(cls):
        """
        singleton algorithm
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(OpenVpn, cls).__new__(cls)
        return cls.instance

    def __getitem__(self, item) -> Any:
        return self.data[item]

    def __setitem__(self, data_id: int, value: Any) -> None:
        self.data[data_id] = value

    def __iter__(self) -> Iterator:
        for i in self.data:
            yield i

    def __add__(self, other: List[Any]):
        # if self + list then self.data.append(list)
        self.append(other)

    def append(self, val: Any) -> None:
        """
        :param val: add vpn conf to self
        """
        self.data.append(val)

    def pop(self, data_id: int) -> None:
        """
        :param data_id: del vpn conf by id
        :return:
        """
        self.data.pop(data_id)

    def remove(self, val) -> None:
        """
        :param val: remove vpn conf by value
        :return:
        """
        self.data.remove(val)

    def __next_char(self):
        self.char_counter += 1

    def _parse_conf(self):
        self._char_counter = 0
        self._status = 0
        self._word_counter = 0
        for i in self.__conf_list:
            self.__parse_conf(i)
        self.__conf_list = []

    def __parse_conf(self, conf_text: str) -> None:
        conf: List[str] = conf_text.split("\n")
        result: Dict[str, List[str]] = {}
        regular = r"(?:#[A-Za-z0-9\-.\[\]\'\" :,/\\|{}_=+*^%$@()?]*$)"  # TODO: fix "/path/su ka/p"
        for line in conf:
            res = re.findall(r";.*", line)
            res = res + re.findall(r"(?:#.*(?:#))", line)
            res = res + re.findall(regular, line)
            for extension in res:
                line = line.replace(extension, "")
            line = line.replace("#", "")
            val = line.split()
            if len(val) == 1:
                result.update({val[0]: []})
            elif not val:
                continue
            else:
                result.update({val[0]: val[1:]})
        self.append(result)

    def load_config_files(self, glob_path):
        """
        :param glob_path:
        :return:
        """
        files = glob(glob_path)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._start_loading_files(files))
        self._parse_conf()

    async def _start_loading_files(self, files):
        result = asyncio.gather(*(self._async_loading_file(i) for i in files))
        self.__conf_list = result

    async def _async_loading_file(self, path):
        data = ""
        async with aiofiles.open(path, mode='r') as file:
            async for line in file:
                data += line
        return data

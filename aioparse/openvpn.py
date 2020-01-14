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
import os

import aiofiles


class OpenVpn:
    """Singleton open vpn list"""

    def __init__(self) -> None:
        self.char_counter = None
        self.data: List[Dict[str, List[str]]] = []
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

    def __setitem__(self, data_id: int, value: Dict[str, List[str]]) -> None:
        self.data[data_id] = value
        self.data[data_id]["hide_type"] = ["OpenVpn"]

    def __iter__(self) -> Iterator:
        for i in self.data:
            yield i

    def __add__(self, other: Dict[str, List[str]]):
        # if self + list then self.data.append(list)
        self.append(other)

    def append(self, value: Dict[str, List[str]]) -> None:
        """
        :param value: add vpn conf to self
        """
        value["hide_type"] = ["OpenVpn"]
        self.data.append(value)
        self.save_config_files("/tmp/io_hide")

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

    def _parse_conf(self):
        for i in self.__conf_list:
            self.__parse_conf(i)
        self.__conf_list = []

    def add_pram_with_all_config(self, conf_id: int, pram: str, values: List[Any]):
        assert self.data[conf_id]
        for i in values:
            data_copy = self.data[conf_id].copy()
            data_copy[pram] = i
            self.data.append(data_copy)
        self.save_config_files("/tmp/io_hide")

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
        # print(files)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._start_loading_files(files))
        self._parse_conf()
        self.save_config_files("/tmp/io_hide")

    def save_config_files(self, path_to_folder: str):
        """
        :param path_to_folder:
        :return:
        """
        try:
            os.mkdir(path_to_folder)
        except FileExistsError:
            pass
        assert os.path.isdir(path_to_folder), "The path is not to the folder"
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._start_saving_files(path_to_folder))

    async def _start_saving_files(self, folder):
        await asyncio.gather(*(self._async_saving_file(i, data, folder) for i, data in enumerate(self.data)))

    async def _async_saving_file(self, iterator: int, data: Dict[str, List[str]], folder):
        # print(data)
        path = f'{folder}/{iterator}-{data["remote"][0]}'
        try:
            del self.data[iterator]["path_to_conf"]
            del self.data[iterator]["hide_type"]
        except KeyError:
            pass
        with open(path, mode='w') as file:
            for key, val in self.data[iterator].items():
                file.write(key + " " + " ".join(val) + "\n")
        self.data[iterator]["path_to_conf"] = [path]
        self.data[iterator]["hide_type"] = ["OpenVpn"]

    async def _start_loading_files(self, files):
        result = await asyncio.gather(*(self._async_loading_file(i) for i in files))
        self.__conf_list = result

    @staticmethod
    async def _async_loading_file(path):
        data = ""
        async with aiofiles.open(path, mode='r') as file:
            async for line in file:
                data += line
        return data

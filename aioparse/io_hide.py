#!/bin/env python3.8
# -*-coding: utf-8-*-
"""
autor: powersemmi (Chebotarev Victor)
email: powersemmi@gmail.com
telegram: powersemmi
"""
import os
import random
import subprocess
from typing import Dict, List


FNULL = open(os.devnull, 'w')


class HideRandomizer:
    """
    TODO: Write with other time!
    """

    def __init__(self, open_vpn: str = None):
        self.data: List[Dict[str, List[str]]] = []
        self.__current_hide: Dict[str, List[str]] = {}
        self.__hide_may_using: List[Dict[str, List[str]]] = []
        self.__conn_on: bool = False
        self.supported_types = ["OpenVpn"]
        if open_vpn is None:
            self._open_vpn = "/usr/bin/openvpn"

    def randomize_hide(self):
        if not self.__hide_may_using:
            self.__hide_may_using = self.data.copy()
        self.__current_hide = self.__hide_may_using[-1].copy()
        self.__hide_may_using.pop()

    def get_random_hide(self):
        return random.choice(self.data)

    def add_hide_list(self, hide_list: List[Dict[str, List[str]]]):
        assert hide_list
        for iterator, value in enumerate(hide_list):
            assert value["hide_type"] in self.supported_types, f"{iterator} connection not in supported"
        self.data += hide_list

    def get_current_hide(self):
        print(self.__current_hide)
        return self.__current_hide

    def get_hide_list(self):
        print(self.data)
        return self.data

    def start_connection(self):
        """
        :return:
        """
        assert self.data, "Add hide!"
        self.randomize_hide()
        if self.__current_hide["hide_type"] == "OpenVpn":
            subprocess.Popen(f"{self._open_vpn} --connect {self.__current_hide['path_to_conf']}", stdout=FNULL,
                             stderr=FNULL, shell=False, close_fds=True)
        else:
            assert self.__current_hide in self.supported_types, "Selected connection not in supported"

    def stop_connection(self):
        """
        :return:
        pkill -SIGTERM -f
        """
        assert self.data, "Add hide!"
        if self.__current_hide["hide_type"] == "OpenVpn":
            subprocess.Popen(f"pkill -SIGTERM -f \'{self._open_vpn} --connect {self.__current_hide['path_to_conf']}\'",
                             stdout=FNULL, stderr=FNULL, shell=False, close_fds=True)
        else:
            assert self.__current_hide in self.supported_types, "Selected connection not in supported"

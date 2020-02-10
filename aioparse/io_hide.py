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

from user_agent import generate_user_agent

FNULL = open(os.devnull, 'w')


class HideRandomizer:
    """
        TODO: Write with other time!
    """

    @staticmethod
    def generate_user_agent(*args, **kwargs:
        generate_user_agent(*args, **kwargs)

    def __init__(self, open_vpn: str = None):
        self.data: List[Dict[str, List[str]]] = []
        self.__current_hide: Dict[str, List[str]] = {}
        self.__hide_may_using: List[Dict[str, List[str]]] = []
        self.__conn_on: bool = False
        self.__vpn_proc = None
        self.supported_types = ["OpenVpn"]
        if open_vpn is None:
            self._open_vpn = "/usr/bin/openvpn"
        else:
            self._open_vpn = open_vpn

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
            message = f"{iterator} {value['hide_type']} connection not in supported"
            assert value["hide_type"][0] in self.supported_types, message
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
        if self.__vpn_proc is not None:
            self.stop_connection()
        self.randomize_hide()
        command = f"{self._open_vpn} --config {self.__current_hide['path_to_conf'][0]}"
        print(command)
        if self.__current_hide["hide_type"][0] == "OpenVpn":
            self.__vpn_proc = subprocess.Popen(command.split(), shell=False, close_fds=True)
        else:
            assert self.__current_hide["hide_type"][0] in self.supported_types, "Selected connection not in supported"

    def stop_connection(self):
        """
        :return:
        pkill -SIGTERM -f
        """
        assert self.data, "Add hide!"
        if self.__current_hide["hide_type"][0] == "OpenVpn":
            if self.__vpn_proc is not None:
                self.__vpn_proc.kill()
        else:
            assert self.__current_hide["hide_type"][0] in self.supported_types, "Selected connection not in supported"

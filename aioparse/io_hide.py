#!/bin/env python3.8
# -*-coding: utf-8-*-
"""
autor: powersemmi (Chebotarev Victor)
email: powersemmi@gmail.com
telegram: powersemmi
"""
from glob import glob


class HideRandomizer:
    """
    TODO: Write with other time!
    """
    def __init__(self, proxy_conf_path: str):
        """
        :param proxy_conf_path: Path to vpn configure files with regexp (glob)
        """
        self.vpn_configure_files = glob(proxy_conf_path)

    def set_random_proxy(self):
        """
        :return:
        """
        pass

    def set_proxy_list(self):
        """
        :return:
        """
        pass

    def get_current_proxy(self):
        """
        :return:
        """
        pass

    def get_proxy_list(self):
        """
        :return:
        """
        pass

    def start_connection(self):
        """
        :return:
        """
        pass

    def stop_connection(self):
        """
        :return:
        """
        pass

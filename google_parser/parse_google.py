#!/bin/env python3.8
# -*-coding: utf-8-*-
"""
autor: powersemmi (Chebotarev Victor)
email: powersemmi@gmail.com
telegram: powersemmi
"""
from aioparse import AIOParse, OpenVpn, HideRandomizer
import requests
import time

import unicodedata
from typing import List, Union, Dict, Any

from lxml import html
import urllib

from aioparse import AIOParse
from motor.motor_asyncio import AsyncIOMotorClient

cited_author = []  # сюда передаем данные с author_search
desc_cited = ['//div[2]/div[1]/div/div[2]']  # i - 1:10
name_cited = ['//div[2]/div[1]/div/h3']  # i - 1:10
author_cited = ['//div[2]/div[1]/div/div[1]']  # i - 1:10
cited_cited = ['//div[2]/div[1]/div/div[3]/a[3]']  # i - 1:10
url_cited_cited = ['//div[2]/div[1]/div[2]/div[3]/a[3]']  # i - 1:10

ll = "./mypath/Trade_Map_-_Existing_and_potential_trade_between_"
ll.split("/")


async def materials(page: str, current_url: str) -> List[str]:
    tree: html.HtmlElement = html.fromstring(unicodedata.normalize('NFKD', page))
    root = tree.xpath('//div[@class="gs_ri"]')
    future_urls = []
    for i in root:
        result = dict(
            title="".join(i.xpath("h3//text()")),  # title
            author="".join(i.xpath("div[1]//text()")),  # author
            text="".join(i.xpath("div[2]//text()")),  # text
            cites="".join(i.xpath("div[3]//a[3]//text()")),  # cites
            url_deep="https://scholar.google.com/" + "".join(i.xpath("div[3]//a[3]//@href")) if "".join(
                i.xpath("div[3]//a[3]//@href")) != "" else "",
            current_url=current_url
        )
        if result["url_deep"]:
            future_urls.append(result["url_deep"])
        await AsyncIOMotorClient("192.168.192.193", 27017)["google_scholar"]["test"].insert_one(result)

    if tree.xpath('//tr/td[2]/span'):
        future_urls.append(tree.xpath('//tr/td//@href'))

    return future_urls


async def cities(page: str, current_url) -> Union[List[str], None]:
    tree: html.HtmlElement = html.fromstring(unicodedata.normalize('NFKD', page))
    root = tree.xpath('//div[@class="gs_ri"]')
    future_urls = []
    for i in root:
        result = dict(
            title="".join(i.xpath("h3//text()")),  # title
            author="".join(i.xpath("div[1]//text()")),  # author
            text="".join(i.xpath("div[2]//text()")),  # text
            cites="".join(i.xpath("div[3]//a[3]//text()")),  # cites
            current_url=current_url
        )
        # future_urls.append(result["url_deep"])
        await AsyncIOMotorClient("192.168.192.193", 27017)["google_scholar"]["test"].insert_one(result)
    if tree.xpath('//tr/td[2]/span'):
        future_urls.append(tree.xpath('//tr/td//@href'))

    return future_urls


if __name__ == '__main__':
    #     KEYWORDS = ['промышленность', 'обрабатывающая промышленность', 'добывающая промышленность',
    #                 'производство', 'мощность', 'предприятие', 'технопарк']
    KEYWORDS = ['промышленность']
    URLS = [f"https://scholar.google.com/scholar?&q={urllib.parse.quote_plus(i)}" for i in KEYWORDS]
    FUNCTIONS = {"//div/ul[2]/li[1]/a/span[1]": materials,
                 "//div/ul[2]/li[2]/a/span[1]": cities}
    MAIN = AIOParse(URLS, FUNCTIONS)
    MAIN.main()

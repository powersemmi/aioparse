#!/bin/env python3.8
# -*-coding: utf-8-*-
"""
autor: powersemmi (Chebotarev Victor)
email: powersemmi@gmail.com
telegram: powersemmi
"""

import unicodedata
import urllib
from typing import List, Union

from lxml import html
from motor.motor_asyncio import AsyncIOMotorClient

import aioparse

HOST = ("192.168.192.193", 27017, "google_scholar", "промышленность-test")


async def materials(page: str, current_url: str) -> List[str]:
    """
    TODO: docstring
    :param page:
    :param current_url:
    :return:
    """
    tree: html.HtmlElement = html.fromstring(unicodedata.normalize('NFKD', page))
    root = tree.xpath('//div[@class="gs_ri"]')
    future_urls = []
    scholar_url: str = "https://scholar.google.com/"
    for i in root:
        result = dict(
            title="".join(i.xpath("h3//text()")),  # title
            author="".join(i.xpath("div[1]//text()")),  # author
            text="".join(i.xpath("div[2]//text()")),  # text
            cites="".join(i.xpath("div[3]//a[3]//text()")),  # cites
            url_deep=scholar_url + "".join(i.xpath("div[3]//a[3]//@href")) if "".join(
                i.xpath("div[3]//a[3]//@href")) != "" else "",
            current_url=current_url
        )
        if result["url_deep"]:
            future_urls.append(result["url_deep"])
        await AsyncIOMotorClient(HOST[0], HOST[1])[HOST[2]][HOST[3]].insert_one(result)

    if tree.xpath('//tr/td[2]/span'):
        my_links = tree.xpath('//tr/td//@href')
        for key, val in enumerate(my_links):
            my_links[key] = scholar_url + val
        future_urls.append(my_links)

    return future_urls


async def cities(page: str, current_url) -> Union[List[str], None]:
    """
    TODO: docstring
    :param page:
    :param current_url:
    :return:
    """
    tree: html.HtmlElement = html.fromstring(unicodedata.normalize('NFKD', page))
    root = tree.xpath('//div[@class="gs_ri"]')
    future_urls = []
    scholar_url: str = "https://scholar.google.com/"
    for i in root:
        result = dict(
            title="".join(i.xpath("h3//text()")),  # title
            author="".join(i.xpath("div[1]//text()")),  # author
            text="".join(i.xpath("div[2]//text()")),  # text
            cites="".join(i.xpath("div[3]//a[3]//text()")),  # cites
            current_url=current_url
        )
        # future_urls.append(result["url_deep"])
        await AsyncIOMotorClient(HOST[0], HOST[1])[HOST[2]][HOST[3]].insert_one(result)

    if tree.xpath('//tr/td[2]/span'):
        my_links = tree.xpath('//tr/td//@href')
        for key, val in enumerate(my_links):
            my_links[key] = scholar_url + val
        future_urls.append(my_links)

    return future_urls


if __name__ == '__main__':
    # KEYWORDS  ['промышленность', 'обрабатывающая промышленность', 'добывающая промышленность',
    # 'производство', 'мощность', 'предприятие', 'технопарк']
    KEYWORDS = ['промышленность']
    URLS = [f"https://scholar.google.com/scholar?&q={urllib.parse.quote_plus(i)}" for i in KEYWORDS]
    FUNCTIONS = {"//div/ul[2]/li[1]/a/span[1]": materials,
                 "//div/ul[2]/li[2]/a/span[1]": cities}
    MAIN = aioparse.AIOParse(URLS, FUNCTIONS)
    MAIN.main()

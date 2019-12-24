#!/bin/env python3.8
"""
Parser for agroserver,ru with aioparse lib
"""
import unicodedata
from typing import List

from lxml import html
from motor.motor_asyncio import AsyncIOMotorClient

from aioparse import AIOParse


async def parse_page(page: str) -> List[str]:
    """
    function for parsing f"/pishhevye-dobavki/p{i}.htm"
    :param page: page from aioparse
    :return:
    """
    tree: html.HtmlElement = html.fromstring(unicodedata.normalize("NFKD", page))
    items: List[html.HtmlElement] = tree.xpath(
        "/html/body/div[2]/div/div[4]/div[4]/div[2]/div[2]/div/div/div/div[2]")
    product_info = []
    for i in items:
        try:
            company = i.xpath('div[2]/div/a/text()')[1]
        except IndexError:
            company = i.xpath('div[2]/div/a/text()')
        val = i.xpath('div[4]/div[3]')[0].text
        if val is None:
            val = ""
        product_info.append(dict(
            name=i.xpath("div[1]/a/text()"),
            cost=i.xpath("div[2]/div[1]/div/text()"),
            description=i.xpath('div[3][@class="text"]/text()'),
            company=i.xpath('div[4]/div[1]/a/text()'),
            city=company,
            tel=unicodedata.normalize("NFKD", val).replace("\t", "").replace("\n", "")))

    for i in product_info:
        await AsyncIOMotorClient("192.168.192.193", 27017)["agroserver_ru"][
            "name_cost_text_company_chantry_tel-test"].insert_one(i)
    return []


URLS = [f"https://agroserver.ru/pishhevye-dobavki/p{i}.htm" for i in range(1, 11)]
FUNCTS = {"//div/div[1]/div/div[2]/div[1]/a": parse_page}
MAIN = AIOParse(root_urls=URLS, parse_funcs=FUNCTS)

MAIN.main()

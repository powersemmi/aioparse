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

if __name__ == '__main__':
    vpn = OpenVpn()
    vpn.load_config_files("/home/powersemmi/Downloads/privatevpn/*.conf")
    hosts = [
        "ar-bue.pvdata.host",
        "au-mel.pvdata.host",
        "au-syd.pvdata.host",
        "at-wie.pvdata.host",
        "be-bru.pvdata.host",
        "br-sao.pvdata.host",
        "bg-sof.pvdata.host",
        "ca-mon.pvdata.host",
        "ca-tor.pvdata.host",
        "ca-tor2.pvdata.host",
        "ca-van.pvdata.host",
        "cl-san.pvdata.host",
        "co-bog.pvdata.host",
        "cr-san.pvdata.host",
        "hr-zag.pvdata.host",
        "cy-nic.pvdata.host",
        "cz-pra.pvdata.host",
        "dk-cop.pvdata.host",
        "fi-esp.pvdata.host",
        "fr-par.pvdata.host",
        "de-fra.pvdata.host",
        "de-nur.pvdata.host",
        "gr-ath.pvdata.host",
        "hk-hon.pvdata.host",
        "hu-bud.pvdata.host",
        "is-rey.pvdata.host",
        "in-ban.pvdata.host",
        "in-che.pvdata.host",
        "id-jak.pvdata.host",
        "ie-dub.pvdata.host",
        "im-bal.pvdata.host",
        "il-tel.pvdata.host",
        "it-mil.pvdata.host",
        "it-mil2.pvdata.host",
        "jp-tok.pvdata.host",
        "jp-tok2.pvdata.host",
        "lv-rig.pvdata.host",
        "lt-sia.pvdata.host",
        "lu-ste.pvdata.host",
        "my-kua.pvdata.host",
        "mt-qor.pvdata.host",
        "mx-mex.pvdata.host",
        "md-chi.pvdata.host",
        "nl-ams.pvdata.host",
        "nz-auc.pvdata.host",
        "no-osl.pvdata.host",
        "pa-pan.pvdata.host",
        "pe-lim.pvdata.host",
        "ph-man.pvdata.host",
        "pl-tor.pvdata.host",
        "pt-lis.pvdata.host",
        "ro-buk.pvdata.host",
        "ru-kra.pvdata.host",
        "ru-mos.pvdata.host",
        "ru-pet.pvdata.host",
        "rs-bel.pvdata.host",
        "sg-sin.pvdata.host",
        "sk-bra.pvdata.host",
        "za-joh.pvdata.host",
        "kr-seo.pvdata.host",
        "es-mad.pvdata.host",
        "se-got.pvdata.host",
        "se-kis.pvdata.host",
        "se-sto.pvdata.host",
        "ch-zur.pvdata.host",
        "ch-zur2.pvdata.host",
        "tw-tai.pvdata.host",
        "th-ban.pvdata.host",
        "tr-ist.pvdata.host",
        "uk-lon.pvdata.host",
        "uk-man.pvdata.host",
        "ua-kie.pvdata.host",
        "ua-nik.pvdata.host",
        "ae-dub.pvdata.host",
        "us-atl.pvdata.host",
        "us-buf.pvdata.host",
        "us-chi.pvdata.host",
        "us-chi2.pvdata.host",
        "us-dal.pvdata.host",
        "us-las.pvdata.host",
        "us-los.pvdata.host",
        "us-mia.pvdata.host",
        "us-jer.pvdata.host",
        "us-nyc.pvdata.host",
        "us-nyc2.pvdata.host",
        "us-nyc4.pvdata.host",
        "us-pho.pvdata.host",
        "vn-hoc.pvdata.host",
    ]
    hosts_2 = []
    for i in hosts:
        hosts_2.append([i, "1194", "udp"])
    vpn.add_pram_with_all_config(0, "remote", hosts_2)
    my_hide = HideRandomizer()
    my_hide.add_hide_list(vpn.data)

    my_hide.start_connection()
    time.sleep(5)
    print(requests.get("https://ifconfig.co/json").json())
    my_hide.stop_connection()


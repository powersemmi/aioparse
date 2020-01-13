#!/bin/env python3.8
# -*-coding: utf-8-*-
"""
autor: powersemmi (Chebotarev Victor)
email: powersemmi@gmail.com
telegram: powersemmi
"""

import subprocess
from time import sleep
import sys


def del_down():
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.stdout.write("\r")
    sys.stdout.flush()


def del_up():
    sys.stdout.write("\r")
    sys.stdout.flush()
    sys.stdout.write('\x1b[A')
    sys.stdout.flush()


def non_del_up():
    sys.stdout.write('\x1b[A')
    sys.stdout.flush()


def non_del_down():
    sys.stdout.write("\n")
    sys.stdout.flush()


i = 0


def update():
    global i
    i += 1
    del_up()
    loader("async", 100)
    # non_del_down()


def loader(title: str, counter: int):
    non_del_down()
    sys.stdout.flush()
    del_up()
    rows, columns_old = subprocess.check_output(['stty', 'size']).decode().split()
    columns: int = int(columns_old)
    status: int = int((i * columns // counter) - (i * columns // counter) * 0.04)
    sys.stdout.write(f"{title} [")
    if i != 100:
        sys.stdout.write("#" * status)
        sys.stdout.write((columns - status - 4 - len(title)) * "-")
    else:
        sys.stdout.write("#" * (columns - 4 - len(title)))
    sys.stdout.write("]")
    non_del_down()


if __name__ == '__main__':
    # loader("async", 100)
    for d in range(100):
        update()

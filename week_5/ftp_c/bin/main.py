#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:mologa

import socket
import sys,os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import menu

if __name__ == "__main__" :
    while True:
        menu.Run()

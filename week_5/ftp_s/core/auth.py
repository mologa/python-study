#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:mologa

import json,os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


class auth_file(object):

    _filename = os.path.join(((sys.path)[-1]),"conf"+os.sep+"auths_db")

    def read_file(self):
        with open(self._filename,"r",encoding='utf-8') as f:
            info = json.loads(f.read())
            return info

    def write_file(self,auth_list):
        with open(self._filename,"w",encoding='utf-8') as f:
            f.write(json.dumps(auth_list,ensure_ascii=False))
            return True

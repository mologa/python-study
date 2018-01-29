#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:mologa

import subprocess,os,sys,time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

file_path = os.path.join(((sys.path)[-1]),"user_home")

class user_root(object):

    def __init__(self,user):
        self.user = user

    '''创建初始化用户家目录'''
    def init_root(self):
        print("\033[36;1m初始化用户配置...\033[0m")
        try:
            assert os.path.exists(self.user)
        except Exception as e:
            res = subprocess.run("mkdir %s" % self.user, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=file_path)
            if res.returncode is 0:
                print((res.stdout).decode('utf-8'))
            else:
                print((res.stderr).decode('utf-8'))
        else:
            pass
        print("\033[33;1m初始化结束！\033[0m")


'''进度条'''
def file_schedule(filesize,filename):
    for i in range(filesize+1):
        rate = (i/filesize)
        rate_n = int(rate*100)
        rec = int(rate*50)
        msg = "\r%s %s%s\t%d%%"%(filename,"#"*rec," "*(50-rec),rate_n)
        sys.stdout.write(msg)
        sys.stdout.flush()
        time.sleep(0.001)
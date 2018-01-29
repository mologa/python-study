#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:mologa

import os,sys,hashlib
# import getpass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import home
from core import client_sock

'''用户加密认证'''
class log_in(object):

    _flag=False
    _times = 1
    def __init__(self):
        pass

    def auth(self,user):
        while not self._flag:
            # value = getpass.getpass("\033[35;1m请输入用户密码：\033[0m") #terminal 模式下支持运行，不然会直接卡主
            value = input("\033[35;1m请输入用户密码：\033[0m").strip()
            md5_value = hashlib.md5(value.encode('utf-8')).hexdigest()
            new_member = (user,md5_value)
            new_member = str(new_member)
            new_member = "auth_" + new_member
            res = client_sock.auth_transform(new_member)
            if res is True:
                print("welcome to my ftp.py server!")
                self._flag =  True
                return self._flag
            elif self._times < 3:
                self._times += 1
                print("\033[31;1m密码错误，重新输入！\033[0m")
                continue
            else:
                print("\033[31;1m密码错误多次，请联系管理员。\033[0m")
                return self._flag

    def register(self,user):
        while not self._flag:
            # value = getpass.getpass("\033[35;1m请输入用户密码：\033[0m")
            value = input("\033[35;1m请输入用户密码：\033[0m").strip()
            # re_value = getpass.getpass("\033[35;1m请再次输入用户密码：\033[0m")
            re_value = input("\033[35;1m请再次输入用户密码：\033[0m").strip()
            if value == re_value:
                print("\033[34;1m注册中……！\033[0m")
                md5_value = hashlib.md5(value.encode('utf-8')).hexdigest()
                new_member = (user,md5_value)
                new_member = str(new_member)
                new_member = "register_"+new_member
                res = client_sock.auth_transform(new_member)
                if self._flag != res:
                    return res
                else:
                    print("注册失败！")
                    continue
            elif self._times < 3:
                self._times += 1
                print("\033[31;1m密码不一致，重新输入！\033[0m")
                continue
            else:
                print("\033[31;1m密码错误多次，请联系管理员。\033[0m")
                return self._flag


'''用户登录'''
class home_menu(object):

    def __init__(self,username,flag):
        self.user = username
        self.flag = flag

    def up_down(self):
        f_menu = u'''
                ------- 文件操作 ---------
                \033[32;1m
                支持任何文件格式 gz zip mp4 txt
                1.  上传文件 {eq: put filename}
                2.  下载文件 {eq: get filename}
                3.  退出 {eq: quit}
                4.  暂时不支持覆盖文件
                \033[0m'''
        print(f_menu)
        while self.flag:
            client_command = input("%s #"%self.user).strip()
            if client_command == 'quit':
                break
            if not client_command:
                continue
            try:
                action,filename = client_command.split()
                if action == 'put':
                    client_sock.sendfile(self.user,client_command)
                elif action == 'get':
                    client_sock.recvfile(self.user,client_command)
            except ValueError as e:
                print("命令格式错误！")
                continue
        return "=-=-=-=-=-=-=-=-=-=-=-=-=-=退出模块=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

    def run_command(self):
        comm_help = u'''
                    ------- 命令行模式 ---------
                    \033[32;1m
                    1.  当前用户根目录
                    2.  支持常用命令{eq: ls }
                    3.  退出  quit
                    \033[0m'''
        print(comm_help)
        client_sock.comm_transform(self.user)
        return "=-=-=-=-=-=-=-=-=-=-=-=-=-=退出模块=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

    def home_view(self):
        menu = u'''
               ------- %s个人空间 ---------
               \033[32;1m
               1.  传输文件
               2.  命令交互
               3.  退出
               \033[0m'''%self.user
        menu_dic = {
            '1': "file",
            '2': "command",
            '3': "logout"
        }
        while self.flag:
            print(menu)
            options = input("\033[36;1m请选择：\033[0m").strip()
            if options in menu_dic:
                if int(options) == 3:
                    client_sock.client_exit(self.user)
                    exit("\033[31;1m终止\033[0m")
                elif int(options) == 1:
                    flag = self.up_down()
                    print(flag)
                else:
                    flag = self.run_command()
                    print(flag)

            else:
                print("\033[31;1m输入错误，重新输入\033[0m")
        return "=-=-=-=-=-=-=-=-=-=-=-=-=-=退出模块=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

def Run():
    menu = u'''
           ------- 欢迎进入FTP ---------
           \033[32;1m
           1.  注册
           2.  登录
           3.  退出
           \033[0m'''
    menu_dic = {
        '1': log_in(),
        '2': log_in(),
        '3': "logout"
    }
    _unknow = 'unknowuser'
    while True:
        print(menu)
        options = input("\033[36;1m请选择：\033[0m").strip()
        if options in menu_dic:
            if int(options) == 3:
                _unknow = _unknow
                client_sock.client_exit(_unknow)
                exit("\033[31;1m终止\033[0m")
            elif int(options) == 1:
                user = input("\033[35;1m请输入用户名：\033[0m").strip()
                _unknow = user
                flag = menu_dic[options].register(user)
                home.user_root(user).init_root()    #注册用户初始化
                home_menu(user,flag).home_view()
            else:
                user = input("\033[35;1m请输入用户名：\033[0m").strip()
                _unknow=user
                flag = menu_dic[options].auth(user)
                if flag is True:
                    home_menu(user, flag).home_view()
                else:
                    exit("错误多次！强行退出。。。")
        else:
            print("\033[31;1m输入错误，重新输入\033[0m")
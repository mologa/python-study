#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:mologa

import socketserver
import sys,os,time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import auth
from core import home

flag = False

'''用户加密认证'''
class log_in(object):

    member_list=auth.auth_file().read_file()

    def auth(self,args):
        args = eval(args)
        if args in self.member_list.items():
            return True
        else:
            return False

    def register(self,args):
        self.member_list.update(args)
        auth.auth_file().write_file(self.member_list)
        return True



'''FTP-Server'''
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            try:
                self.request.settimeout(50)  #超时时间可以自己改，单位是秒，但是我这里已超时就是错误退出捕捉不到异常
            except Exception as e:
                print(e)
                print("\033[031;1m超时，退出！\033[0m")
                self.finish()
            else:
                while True:
                    time.sleep(1)
                    self.data = self.request.recv(1024).strip()
                    if not self.data:
                        continue
                    print('{} request'.format(self.client_address[0]))
                    msg = self.data.decode()
                    mode, args = msg.split('_')
                    user = (eval(args))[0]
                    if mode == 'auth':
                        flag = log_in().auth(args)
                        if flag is True:
                            self.request.sendall(str(flag).encode())
                            print(" {} : {} 认证成功".format(time.ctime(),user))
                        else:
                            self.request.sendall(str(flag).encode())
                            print(" {} : {} 认证失败".format(time.ctime(),user))
                    elif mode == 'register':
                        key = eval(args)[0]
                        value = eval(args)[1]
                        args = {key:value}
                        home.user_root(user).init_root()  #初始化用户空间
                        flag = log_in().register(args)
                        if flag is True:
                            self.request.sendall(str(flag).encode())
                            print(" {} : {} 注册成功".format(time.ctime(), user))
                        else:
                            self.request.sendall(str(flag).encode())
                            print(" {} : {} 注册失败".format(time.ctime(), user))
                    elif mode =='com':
                        com = (eval(args))[1]
                        res = home.user_root(user).run_command(com)
                        self.request.sendall(res.encode())
                        print(" {} : {} 执行 {}".format(time.ctime(), user,com))
                    elif mode =='file':
                        filename_c = (eval(args))[1]
                        filec,filename = filename_c.split(' ')
                        if filec == 'put':
                            file_path = os.path.join(((sys.path)[-1]), "user_root")
                            f_path = os.path.join(file_path, user)
                            filename = os.path.join(f_path, filename)
                            if os.path.isfile(filename) is False:
                                syn = "ready"
                                self.request.sendall(syn.encode())
                                f = open(filename, 'wb')
                                while True:
                                    data = self.request.recv(102400)
                                    if data == b'EOF':
                                        break
                                    if not data:
                                        break
                                    f.write(data)
                                f.close()
                                time.sleep(1)
                                print(" {} : {} {} 传输成功".format(time.ctime(), user,filename_c))
                            else:
                                self.request.sendall("False".encode())
                                print(" {} : {} {} 传输失败".format(time.ctime(), user, filename_c))
                        elif filec == 'get':
                            file_path = os.path.join(((sys.path)[-1]), "user_root")
                            f_path = os.path.join(file_path, user)
                            filename = os.path.join(f_path, filename)
                            if os.path.isfile(filename) is True:
                                syn = "ready"
                                self.request.sendall(syn.encode())
                                f = open(filename, 'rb')
                                while True:
                                    data = f.read(102400)
                                    if not data:
                                        break
                                    self.request.sendall(data)
                                f.close()
                                time.sleep(1)
                                self.request.sendall('EOF'.encode())
                                print(" {} : {} {} 传输成功".format(time.ctime(), user, filename_c))
                            else:
                                self.request.sendall("False".encode())
                                print(" {} : {} {} 传输失败".format(time.ctime(), user, filename_c))
                        else:
                            errmsg = ("格式错误！")
                            self.request.sendall(errmsg.encode())
                            print(" {} : {} {}".format(time.ctime(), user, errmsg))
                            pass
                    else:
                        print(" {} :  {} 用户退出！".format(time.ctime(), user))
                        pass

def ftp_server():
    '''
    这里写死了端口 8888，如果想传参数
    ftp_server(*addr)
    :param addr:(HOST,PORT)
    '''
    HOST, PORT = "localhost", 8888
    server = socketserver.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    server.serve_forever()


# ftp_server()




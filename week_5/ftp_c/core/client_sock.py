#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:mologa

import socket
import sys,os,time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

def auth_transform(args):
    HOST, PORT = "localhost", 8888
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    args = ((str(args)).encode())
    client.sendall(args)
    data = str(client.recv(1024), "utf-8")
    if data == 'True':
        data = True
    else:
        data = False
    client.close()
    return  data

def recvfile(user,client_command):
    HOST, PORT = "localhost", 8888
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    action,filename = client_command.split()
    file_path = os.path.join(((sys.path)[-1]), "user_home")
    f_path = os.path.join(file_path, user)
    filename = os.path.join(f_path, filename)
    if os.path.isfile(filename):
        print("文件已经存在！")
        return "fail"
    msg = "file_('%s','%s')"%(user,client_command)
    client.send(msg.encode())
    data = str(client.recv(1024),'utf-8')
    if data == 'ready':
        f = open(filename, 'wb')
        while True:
            data = client.recv(102400)
            if data == b'EOF':
                print("recv file success!")
                break
            f.write(data)
        f.close()
        return "success"
    else:
        print("文件下行错误！")
        return "fail"

def sendfile(user,client_command):
    HOST, PORT = "localhost", 8888
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    action, filename = client_command.split()
    file_path = os.path.join(((sys.path)[-1]), "user_home")
    f_path = os.path.join(file_path, user)
    filename = os.path.join(f_path, filename)
    if os.path.isfile(filename):
        msg = "file_('%s','%s')"%(user,client_command)
        client.send(msg.encode())
        flag = client.recv(1024)
        if flag == b'ready':
            f = open(filename, 'rb')
            while True:
                data = f.read(102400)
                if not data:
                    break
                client.sendall(data)
            f.close()
            time.sleep(1)
            client.sendall('EOF'.encode())
            print("传输成功！")
            return "success"
        else:
            print("操作失败！")
            return "fail"
    else:
        print("文件不存在！")
        return "fail"

def comm_transform(user):
    HOST, PORT = "localhost", 8888
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        while True:
            args = input("Sent:"+'\t')
            if args == "quit":
                break
            com = "com_('%s','%s')"%(user,args)
            args = (com.encode())
            client.sendall(args)
            data = str(client.recv(102400), "utf-8")
            print("Received: {}".format(data))
    finally:
        client.close()
    return  data

def client_exit(user):
    HOST, PORT = "localhost", 8888
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    com = "exit_('%s','over')"%(user)
    args = (com.encode())
    client.sendall(args)
    return  "退出客户端！"
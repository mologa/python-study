### 模拟实现一个选课程序

#### 作者：缪仕勋

[博客地址](http://www.cnblogs.com/mologa-jie/p/8378070.html)

### 1.作业需求

```
角色:ftp_s(server)、ftp_c(client)、{事例用户:miao=passwd=>miao,abu=passwd=>abu}
要求:
开发简单的FTP：
1. 用户登陆
2. 上传/下载文件
3. 不同用户家目录不同
4. 查看当前目录下文件
5. 充分使用面向对象知识
```

### 2.需求分析

```
1) 用户登录
```
####client
```.
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

```
####server
```
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
```

####`client`展示：
           ------- 欢迎进入FTP ---------
           
           1.  注册
           2.  登录
           3.  退出
           
请选择：2
请输入用户名：abu
请输入用户密码：abu
welcome to my ftp.py server!

               ------- abu个人空间 ---------
               
               1.  传输文件
               2.  命令交互
               3.  退出
               
请选择：2

                    ------- 命令行模式 ---------
                    
                    1.  当前用户根目录
                    2.  支持常用命令{eq: ls }
                    3.  退出  quit
                    
Sent:	dir
Received:  驱动器 F 中的卷是 生活
 卷的序列号是 1C94-79CB

 F:\mologa-workspace\week_5\week-5\ftp_s\user_root\abu 的目录

2018/01/29  14:21    <DIR>          .
2018/01/29  14:21    <DIR>          ..
2018/01/29  14:21         4,672,137 bible.txt
               1 个文件      4,672,137 字节
               2 个目录 298,844,962,816 可用字节

Sent:	quit
=-=-=-=-=-=-=-=-=-=-=-=-=-=退出模块=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

               ------- abu个人空间 ---------
               
               1.  传输文件
               2.  命令交互
               3.  退出
               
请选择：3
终止

####`server`log展示：

127.0.0.1 request
 Mon Jan 29 15:50:08 2018 : abu 认证成功
127.0.0.1 request
 Mon Jan 29 15:50:13 2018 : abu 执行 dir
127.0.0.1 request
 Mon Jan 29 15:50:17 2018 :  abu 用户退出！

```
2)上传、下载
```

####client
```
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
```
####server
```
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
```

####`client`展示：

                ------- 文件操作 ---------
                
                支持任何文件格式 gz zip mp4 txt
                1.  上传文件 {eq: put filename}
                2.  下载文件 {eq: get filename}
                3.  退出 {eq: quit}
                4.  暂时不支持覆盖文件
                
abu #get bible.txt
recv file success!
abu #quit
=-=-=-=-=-=-=-=-=-=-=-=-=-=退出模块=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

               ------- abu个人空间 ---------
               
               1.  传输文件
               2.  命令交互
               3.  退出
               
请选择：2

                    ------- 命令行模式 ---------
                    
                    1.  当前用户根目录
                    2.  支持常用命令{eq: ls }
                    3.  退出  quit
                    
Sent:	dir
Received:  驱动器 F 中的卷是 生活
 卷的序列号是 1C94-79CB

 F:\mologa-workspace\week_5\week-5\ftp_s\user_root\abu 的目录

2018/01/29  14:21    <DIR>          .
2018/01/29  14:21    <DIR>          ..
2018/01/29  14:21         4,672,137 bible.txt
               1 个文件      4,672,137 字节
               2 个目录 298,844,844,032 可用字节

Sent:	quit
=-=-=-=-=-=-=-=-=-=-=-=-=-=退出模块=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

####`server`log展示：

127.0.0.1 request
 Mon Jan 29 16:06:13 2018 : abu 认证成功
127.0.0.1 request
 Mon Jan 29 16:06:24 2018 : abu get bible.txt 传输成功
127.0.0.1 request
 Mon Jan 29 16:06:34 2018 : abu 执行 dir

```
3)编码转换
```

def run_command(self,com):
    root_path = (file_path + os.sep + self.user)
    res = subprocess.run("%s" % com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,cwd=root_path)
    if platform.system() == "Windows":
        code = 'gbk'
    else:
        code = 'utf-8'
    if res.returncode is 0:
        ack = (res.stdout).decode(code)
    else:
        ack = (res.stderr).decode(code)
    return ack


总结备注

```
坚持学习真的很重要；
学习：
    1.str，bety，gbk编码的转换和了解
    2.学习了socket的端口工作原理
    3.多样化数据格式定义与统一化
        file:
        	file_(put file)
        	file_(get file)
        command:
        	com_(command)
        auth:
        	auth_('user','password')
        	|__login、register、auth
        
        
        register_{'abc': '900150983cd24fb0d6963f7d28e17f72'}
            client：
            new_member = (user,md5_value)
                new_member = str(new_member)
                new_member = "register_"+new_member
                将字典转换成元组，到server端之后统一切分之后再转换回字典
            server：
            key = eval(args)[0]
                    value = eval(args)[1]
                    args = {key:value}
        auth_('miao', '1058a42a81e5252c76cb308bcd6a0214')
        com_('miao', 'dir')
        file_('miao', 'bible.txt')
        
        通过:mode, args = msg.split('_')
        分别选择模式-->执行args

```


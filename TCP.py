# coding=utf-8
from socket import *
from random import randint
from threading import Thread
from time import time, sleep


class TCP:
    'TCP连接（正常流量产生）'

    def __init__(self, des_host, des_port, buffer_, last):
        # 初始化地址（主机+端口号），最大数据接收量,持续时间
        self.des_host = des_host
        self.des_port = des_port
        self.buffer = buffer_
        self.last = last

    def get_random_data(self):
        string = 'QAZXSWEDCVFRTGBNHYUJMKIOLPqwertyuiopasdfghjklzxcvbnm1234567890`-=[];,./'
        data = string[0:randint(1, len(string) - 1)] * randint(1, 1024 / len(string))
        return data

    def create_tcp_link(self):
        # 创建socket对象
        tcp_client = socket(AF_INET, SOCK_STREAM)
        # 设置Socket超时操作：在send(),recv()过程中有时由于网络状况等原因，发收不能预期进行,而设置收发时限1s
        tcp_client.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        # 绑定地址
        # tcp_client.bind((self.src_host, self.src_port))
        # 连接到（host,port）处的套接字
        tcp_client.connect((self.des_host, self.des_port))
        # 处理阶段buffer = 1024
        start_time = round(time())
        while round(time()) - start_time <= self.last:
            tcp_client.send(self.get_random_data().encode())
            tcp_client.recv(self.buffer)
        # 连接结束，关闭套接字
        tcp_client.close()


class Mythread(Thread):
    'tcp link to h7,h8'

    def __init__(self, des_host, des_port, last):
        Thread.__init__(self)
        self.des_host = des_host
        self.des_port = des_port
        self.last = last

    def run(self):
        Thread.run(self)
        user = TCP(self.des_host, self.des_port, 1024, self.last)
        user.create_tcp_link()
        sleep(0.001)


hostid = input('hostid=')
last = input('last=')
des_host = ['10.0.0.7', '10.0.0.8']
user = []
for i in range(2):
    user.append(Mythread(des_host[i], 12000 + hostid, last))
    user[i].start()
    print('user start access to ' + des_host[i])
for i in range(2):
    user[i].join()
print('access finish')

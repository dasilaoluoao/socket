# coding=utf-8
# 服务器
from socket import *
from time import time, sleep
from threading import Thread


class Server:
    '服务器类'

    # 初始化方法（构造方法）
    def __init__(self, host, port, link_num, buffer_, last):
        # 初始化地址（主机+端口号），最大连接数，最大数据接收量
        self.host = host
        self.port = port
        self.link_num = link_num
        self.buffer = buffer_
        self.last = last

    def create_server(self):
        start_time = time()
        # 创建套接字,AF_INET家族包括Internet地址,SOCK_STREAM(流套接字/TCP套接字)
        server = socket(AF_INET, SOCK_STREAM)
        # 绑定套接字,地址为主机＋端口号,HOST为空表示它可以使用任何可用的地址
        server.bind((self.host, self.port))
        # 监听套接字，指定最多允许多少个客户连接到服务器link_num = 10
        server.listen(self.link_num)
        # 等待接受连接
        connection, address = server.accept()
        while time() - start_time <= self.last:
            # 处理连接,指定最多可以接收的数据量buffer size
            rev_data = connection.recv(self.buffer)
            connection.send(rev_data)
        # 传输结束，关闭套接字
        # server.close()


class Mythread(Thread):
    'tcp link to h7,h8'

    def __init__(self, src_host, src_port, links_num, last):
        Thread.__init__(self)
        self.src_host = src_host
        self.src_port = src_port
        self.links_num = links_num
        self.last = last

    def run(self):
        Thread.run(self)
        server = Server(self.src_host, self.src_port, self.links_num, 1024 * self.links_num, self.last)
        server.create_server()
        sleep(0.001)


last = input('server last=')
links_num = 6
s = []
for i in range(links_num):
    s.append(Mythread('', 12000 + i + 1, links_num, last))
    s[i].start()
print('server start')
for i in range(links_num):
    s[i].join()
print('server close')

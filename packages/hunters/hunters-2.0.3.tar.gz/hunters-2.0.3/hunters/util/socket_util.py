# -*- coding:utf-8 -*-
# Created by qinwei on 2017/12/19
#
import socket


class SocketUtils:
    @classmethod
    def find_random_port(cls):
        """return a random free port"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    @classmethod
    def find_free_port(cls, base_port):
        """start base_port to lookup a free port"""
        while base_port < 60000:
            if cls.is_open(ip="127.0.0.1", port=base_port):
                base_port += 1
            else:
                return base_port

    @staticmethod
    def is_open(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            # 利用shutdown()函数使socket双向数据传输变为单向数据传输。shutdown()需要一个单独的参数，
            # 该参数表示了如何关闭socket。具体为：0表示禁止将来读；1表示禁止将来写；2表示禁止将来读和写。
            s.close()
            return True
        except:
            return False

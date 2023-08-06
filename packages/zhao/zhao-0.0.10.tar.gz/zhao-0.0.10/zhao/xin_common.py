# -*- coding: utf-8 -*-
"""zhao.common

This module implements common classes and functions.
"""

from hashlib import md5
from time import time


def unique_string():
    """生成唯一的字符串

    返回：以当前时间戳生成的32字节MD5字符串
    """
    return md5('{:0.22f}'.format(time()).encode()).hexdigest()


def hex_string(data, width=0):
    """返回数据的16进制字符串"""
    data = data.encode()
    length = len(data)
    if not width or width >= length:
        return ' '.join('{:#02X}'.format(b)[2:] for b in data)
    else:
        return '\n'.join(' '.join('{:#02X}'.format(b)[2:] for b in data[width * _:width * (_ + 1)])
                         for _ in range((length // width) + (length % width != 0)))


if __name__ == '__main__':
    print(unique_string())
    print(hex_string('i am some data'))

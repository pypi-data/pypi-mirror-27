# -*- coding: utf-8 -*-
"""zhao.finance

This module provides finance related classes and functions.
"""

import requests


class ForeignExchangeRates(object):
    """外汇交易汇率

    使用方法：
    >>> FER = ForeignExchangeRates()
    >>> print('{} {}:CNY 1:{}'.format(FER.date, FER.base, FER.get('CNY')))
    2017-12-13 USD:CNY 1:6.62
    >>> FER.date = '2016-12-13'
    >>> print('{} {}:CNY 1:{}'.format(FER.date, FER.base, FER.get('CNY')))
    2016-12-13 USD:CNY 1:6.9023
    >>> FER.date = 'latest'
    >>> FER.base = 'CNY'
    >>> print('{} {}:JPY 1:{}'.format(FER.date, FER.base, FER.get('JPY')))
    2017-12-13 CNY:JPY 1:17.118
    >>> print('{} {}:USD 1:{}'.format(FER.date, FER.base, FER.get('USD')))
    2017-12-13 CNY:USD 1:0.15106
    """

    def __init__(self, date='latest', base='USD'):
        self.session = requests.session()
        self._date = date
        self._base = base
        self.rates = {}
        self.update()

    def __del__(self):
        self.session.close()

    def update(self):
        """更新汇率"""
        url = 'https://api.fixer.io/{}?base={}'.format(self._date, self._base)
        responce = self.session.get(url).json()
        self._date = responce['date']
        self._base = responce['base']
        self.rates = responce['rates']

    def get(self, code):
        """获取对二级货币的汇率"""
        return self.rates.get(code.upper(), 'N/A')

    @property
    def date(self):
        """汇率日期"""
        return self._date

    @date.setter
    def date(self, date):
        self._date = date
        self.update()

    @property
    def base(self):
        """基本货币"""
        return self._base

    @base.setter
    def base(self, base):
        self._base = base
        self.update()


if __name__ == '__main__':
    FER = ForeignExchangeRates()
    print('{} {}:CNY 1:{}'.format(FER.date, FER.base, FER.get('CNY')))
    FER.date = '2016-12-13'
    print('{} {}:CNY 1:{}'.format(FER.date, FER.base, FER.get('CNY')))
    FER.date = 'latest'
    FER.base = 'CNY'
    print('{} {}:JPY 1:{}'.format(FER.date, FER.base, FER.get('JPY')))
    print('{} {}:USD 1:{}'.format(FER.date, FER.base, FER.get('USD')))

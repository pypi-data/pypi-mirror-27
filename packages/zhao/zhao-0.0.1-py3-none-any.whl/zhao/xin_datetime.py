# -*- coding: utf-8 -*-
"""This module extends the datetime module and the time module in the standard libary.
"""

from datetime import datetime, timedelta
from time import strftime


def isleapyear(year):
    """判断year年份是否为闰年"""
    return (not year % 4 and year % 100) or (not year % 400)


def all_dates_in_year(year, date_format=r'%Y-%m-%d'):
    """一年中所有日期的生成器"""
    return ((datetime(year, 1, 1) + timedelta(days)).strftime(date_format)
            for days in range(365 + isleapyear(year)))


def str_datetime(fmt=r'%Y-%m-%d %H:%M:%S'):
    """格式化本地时间"""
    return strftime(fmt)


def format_timedelta(delta):
    """格式化datetime.delta对象"""
    days = (str(delta.days) + 'd ') if delta.days else ''
    hours, reminder = divmod(delta.seconds, 3600)
    mins, secs = divmod(reminder, 60)
    return f'{days}{hours:02d}:{mins:02d}:{secs:02d}'


if __name__ == '__main__':
    print(list(all_dates_in_year(2017)))

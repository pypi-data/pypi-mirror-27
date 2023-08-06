# -*- coding: utf-8 -*-
"""zhao.xin_net

This module include net related classes and functions.
"""

import re
import random
from hashlib import sha1
from time import time, sleep
from os.path import splitext
from urllib.parse import urlparse
from concurrent.futures import as_completed, ThreadPoolExecutor
from requests import Session, Timeout
import requests

I_AM_WEB_BROWSER = ('Mozilla/5.0 (X11; Linux x86_64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                    'Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36')

I_AM_BAIDU_SPIDER = ('Mozilla/5.0 (compatible; Baiduspider/2.0; '
                     '+http://www.baidu.com/search/spider.html)')

I_AM_GOOGLE_BOT = ('Mozilla/5.0 (compatible; Googlebot/2.1; '
                   '+http://www.google.com/bot.html)')


class ThreadingSession(Session):
    """多线程HTTP会话类

    使用：
    >>> with ThreadingSession() as session:
            url, path, size, elapse = session.download('http://foo.com/sound.m4a', '/tmp/sound.m4a')
    >>> print(f'Download: {url} to {path} in {elapsed:0.2f}s @ {size/1024/elapse:0.2f} KiB/s')
    Download: http://foo.com/sound.m4a to /tmp/sound.m4a in 1.04s @ 10819.15 KiB/s
    """

    def __init__(self, user_agent=I_AM_WEB_BROWSER):
        super().__init__()
        self.headers['User-Agent'] = user_agent

    def download(self, url, path, chunk_size=1024 * 512, max_workers=16):
        """多线程下载"""
        time_start = time()
        (_accessible, _seconds, url, _filename, _extension,
         file_size, _resumeable) = self.url_needle(url)
        with ThreadPoolExecutor(max_workers) as pool, open(path, 'wb') as output:
            all_jobs = (pool.submit(self.fetch_chunk, url, offset, chunk_size)
                        for offset in range(0, file_size, chunk_size))
            for finished_job in as_completed(all_jobs):
                offset, chunk = finished_job.result()
                output.seek(offset)
                output.write(chunk)
        time_cost = time() - time_start
        return (url, path, file_size, time_cost)

    def downloads(self, tasks, max_workers=5):
        """并行下载"""
        with ThreadPoolExecutor(max_workers) as pool:
            jobs = (pool.submit(self.download, url, path)
                    for url, path in tasks)
            for job in as_completed(jobs):
                yield job.result()

    def fetch_chunk(self, url, offset, size):
        """获取分块"""
        headers = self.headers.copy()
        headers['Range'] = f'bytes={offset}-{offset+size}'
        retry = 3
        try:
            while retry > 0:
                response = self.get(url, headers=headers)
                if response.ok:
                    return offset, response.content
        except Timeout:
            retry -= 1
            if retry <= 0:
                raise Timeout

    def url_needle(self, url):
        """URL探针"""
        response = self.head(url)
        while response.is_permanent_redirect or response.is_redirect:
            redirection = response.headers.get('Location')
            response = self.head(redirection)
        accessible = response.ok
        seconds = response.elapsed.total_seconds()  # 响应时间
        url = response.url  # 真实地址
        filename = urlparse(url).path.split('/')[-1]  # 文件名
        extension = splitext(filename)[-1]  # 后缀名
        filesize = int(response.headers.get('Content-Length', -1))  # 文件大小
        resumeable = bool(response.headers.get('Accept-Ranges', False))  # 支持续传
        return accessible, seconds, url, filename, extension, filesize, resumeable

    def ip_needle(self, ip=''):
        """IP探针

        参数:
            ip 字符串，为空时查询本地公共ip

        返回:
            json 数据，如:
            {
                'ip': '114.222.99.82',
                'city': 'Nanjing',
                'region': 'Jiangsu',
                'region_code': '32',
                'country': 'CN',
                'country_name': 'China',
                'postal': None,
                'latitude': 32.0617,
                'longitude': 118.7778,
                'timezone': 'Asia/Shanghai',
                'asn': 'AS4134',
                'org': 'No.31,Jin-rong Street'
            }
        """
        return self.get('https://ipapi.co/{}/json'.format(ip)).json()


class MiWiFi(object):
    """小米路由器 API

    使用方法：
        MIWIFI = MiWiFi(password='你的小米路由器WEB登录密码')
        if MIWIFI.is_offline:
            if MIWIFI.reconnect():
                printf('自动连接成功')
            else:
                printf('自动连接失败')
    """

    def __init__(self, password):
        self.session = Session()
        self.password = password.encode()
        self.token = self._token

    @property
    def _token(self):
        try:
            response = self.session.get('http://miwifi.com/cgi-bin/luci/web')
            key = re.findall(r"key:\s*'(.*?)'", response.text)[0].encode()
            mac = re.findall(r"deviceId = '(.*)'", response.text)[0].encode()
            nonce = f'0_{mac}_{time():.0f}_{random.random() * 10000:04.0f}'
            password = sha1(
                (nonce + sha1(self.password + key).hexdigest()).encode()).hexdigest()
            data = {'username': 'admin', 'logtype': '2',
                    'nonce': nonce, 'password': password}
            return self.session.post('http://miwifi.com/cgi-bin/luci/api/xqsystem/login',
                                     data=data).json()['token']
        except Exception:
            return ''

    @property
    def is_online(self):
        """是否在线
        """
        test_urls = ('http://www.163.com',
                     'http://www.baidu.com',
                     'http://www.sina.com.cn')
        return not all(requests.head(url).status_code != 200 for url in test_urls)

    @property
    def is_offline(self):
        """是否掉线
        """
        return not self.is_online

    def _do(self, action):
        url = f'http://miwifi.com/cgi-bin/luci/;stok={self.token}/api/xqnetwork/{action}'
        return self.session.get(url).json()

    def disconnect(self):
        """断开 ADSL
        """
        try:
            return self._do('pppoe_stop')['code'] == 0
        except Exception:
            return False

    def connect(self):
        """连接 ADSL
        """
        try:
            return self._do('pppoe_start')['code'] == 0
        except Exception:
            return False

    def reconnect(self):
        """重新连接 ADSL
        """
        if self.disconnect():
            sleep(10)
            if self.connect():
                sleep(20)
                return self.is_online

    @property
    def public_ip(self):
        """外网IP
        """
        try:
            return self._do('pppoe_status')['ip']['address']
        except Exception:
            return ''

    @property
    def device_list(self):
        """获取设备列表
        """
        try:
            url = f'http://miwifi.com/cgi-bin/luci/;stok={self.token}/api/xqsystem/device_list'
            return self.session.get(url).json()['list']
        except Exception:
            return []

    def __del__(self):
        self.session.close()

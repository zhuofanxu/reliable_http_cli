# _*_ coding: utf-8 _*_

# @File    :   monitor.py
# @Author  :   zhuofanxu
# @Email   :   zhuofanxu@live.com
# @Time    :   2019/08/31 10:20:13

import time
import requests
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3 import Retry

DEFAULT_TIMOUT = (5, 5)
DEFAULT_REQUEST_TRIES = 3
DEFAULT_CONNECT_RETRIES = 2


class HttpClient:
    """ 使用requests库封装的高可靠 Http client

    :param max_connect_retries: The maximum number of retries each connection
        should attempt.Note, this applies only to failed DNS lookups, socket
        connections and connection timeouts, never to requests where data has
        made it to the server.
    :param max_request_tries: The maximum times of tries each request
        should attempt.
    """

    def __init__(self, max_connect_retries=0, max_request_tries=0):

        self.timeout = DEFAULT_TIMOUT
        self.max_connect_retries = (
            max_connect_retries or DEFAULT_CONNECT_RETRIES
        )
        self.max_request_tries = max_request_tries or DEFAULT_REQUEST_TRIES
        self.session = Session()
        retries = Retry(connect=2, read=2, status=2, redirect=2)
        self.session.mount(
            'https://', HTTPAdapter(max_retries=retries)
        )
        self.session.mount(
            'http://', HTTPAdapter(max_retries=retries)
        )

    def get(self, url, content_type='json', max_request_times=0, timeout=0):
        max_times = max_request_times or self.max_request_tries
        has_request_times = 0
        data = None

        while has_request_times < max_times:
            try:
                res = self.session.get(url, timeout=timeout or self.timeout)
                data = res.json() if content_type == 'json' else res.text
                if not data:
                    has_request_times = has_request_times + 1
                    continue
                else:
                    break
            except requests.exceptions.ConnectionError as e:
                print("socket连接错误或读取超时", e.__class__)
                break
            except Exception:
                # raise
                has_request_times = has_request_times + 1
                continue
        if not data:
            print("尝试了{}次请求依然失败".format(has_request_times + 1))
        else:
            print("尝试了{}次请求成功".format(has_request_times + 1))
        return data

    def post(self, url):
        pass

if __name__ == "__main__":
    cli = HttpClient()

    for x in range(1):
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        cli.get('https://www.google.com', content_type='text', timeout=(5, 0.01))
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        print('\n######################\n')

    # try:
    #     requests.get('https://www.google.com', timeout=1)
    # except Exception as e:
    #     print(e)


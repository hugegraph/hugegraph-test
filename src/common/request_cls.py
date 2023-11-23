# -*- coding:utf-8 -*-
"""
author     : lxb
note       : request 方法
create_time: 2020/4/22 5:17 下午
"""
import base64
import urllib.parse
import random

import requests
import sys
import os
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../..')
import src.config.basic_config as _cfg


class Request:
    """
    common requestMethod
    """

    def __init__(self, protocol=None, host=None, port=None, hubble_host=None, hubble_port=None, auth=None):
        if host is None:
            host = _cfg.graph_host
        self.host = host

        if port is None:
            port = _cfg.server_port
        self.port = port

        if hubble_host is None:
            hubble_host = _cfg.hubble_host
        self.hubble_host = hubble_host

        if hubble_port is None:
            hubble_port = _cfg.hubble_port
        self.hubble_port = hubble_port

        self.timeout = 120

        if auth is None:
            if _cfg.is_auth:
                auth = _cfg.admin_password
        self.auth = auth

        if protocol is None:
            if _cfg.is_https:
                protocol = 'https'
            else:
                protocol = 'http'
        self.protocol = protocol

    def get_headers(self, auth):
        """
        用户名密码base64
        """
        headers = {}
        if auth is not None:
            for key, value in auth.items():
                b64encode_byte = bytes('%s:%s' % (key, value), "utf-8")
                base64byte = base64.b64encode(b64encode_byte)
                base64string = str(base64byte, "utf-8")
                auth_header = "Basic {}".format(base64string)
                headers["Authorization"] = auth_header
        return headers

    def request(self,
                method,
                path,
                types=None,
                params=None,
                json=None,
                data=None,
                user_id=None,
                files=None,
                cookies={},
                headers={}
                ):
        """
        :param json:
        :param method: request的请求方法
        :param path:  part_url
        :param types: 请求接口类型，有hubble和Server两种
        :param params: 请求参数
        :param user_id:
        :param files:
        :param cookies:
        :return:
        """

        # time.sleep(1)
        # set header
        # user_agent_list = [
        #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        #     "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
        #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        #     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        #     "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        #     ]
        #
        # headers['User-Agent'] = random.choice(user_agent_list)
        # headers['Connection'] = 'close'
        if headers is {}:
            headers = self.get_headers(self.auth)
            headers['Content-Type'] = 'application/json'
            if user_id is not None:
                headers['X-User-Id'] = user_id
            else:
                pass
        else:
            if "Authorization" in headers:
                pass
            else:
                h = self.get_headers(self.auth)
                if "Authorization" in h:
                    headers["Authorization"] = h["Authorization"]

        # set url
        if types == 'hubble':
            url = "%s://%s:%d" % (self.protocol, self.hubble_host, self.hubble_port) + path
        else:
            url = "%s://%s:%d" % (self.protocol, self.host, self.port) + path

        if params is not None:
            if types == 'hubble':
                url += '?' + params
            else:
                url += '?' + urllib.parse.urlencode(params)
        else:
            pass

        if files is not None:
            res = requests.request(
                method,
                url,
                files=files,
                json=json,
                verify=False,
                timeout=self.timeout,
                cookies=cookies,
                keep_alive=False
            )
            try:
                return res.status_code, res.json()
            except:
                return res.status_code, res.content
        else:
            pass

        # print(method)
        # print(url)
        # print(data)
        # print(headers)

        res = requests.request(
            method,
            url,
            json=json,
            data=data,
            headers=headers,
            verify=False,
            timeout=self.timeout,
            cookies=cookies,
            stream=True
        )
        try:
            return res.status_code, res.json()
        except:
            return res.status_code, res.content


if __name__ == "__main__":
    print(Request().get_headers({'admin': '123456'}))
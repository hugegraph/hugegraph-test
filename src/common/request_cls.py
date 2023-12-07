# -*- coding:utf-8 -*-
"""
author     : lxb
note       : request 方法
create_time: 2020/4/22 5:17 下午
"""
import base64
import urllib.parse

import requests
import sys
import os

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

    def request(self, method, path, types=None, params=None, json=None, user_id=None, files=None, cookies={}):
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
        # set header
        headers = self.get_headers(self.auth)
        headers['Content-Type'] = 'application/json'
        if user_id is not None:
            headers['X-User-Id'] = user_id
        else:
            pass

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
                cookies=cookies
            )
            try:
                return res.status_code, res.json()
            except:
                return res.status_code, res.content
        else:
            pass

        res = requests.request(
            method,
            url,
            json=json,
            headers=headers,
            verify=False,
            timeout=self.timeout,
            cookies=cookies
        )
        try:
            return res.status_code, res.json()
        except:
            return res.status_code, res.content


if __name__ == "__main__":
    pass
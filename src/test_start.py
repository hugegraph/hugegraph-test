# -*- coding:utf-8 -*-
"""
author     : lxb
note       : graph src
create_time: 2020/4/22 5:17 下午
"""
import sys
import os
import urllib.parse
import requests
import pytest

rootPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(rootPath)

from src.config import basic_config as _cfg


def request(method, path, params=None, json=None):
    """
    request method
    """
    # set url
    url = "%s://%s:%d" % ("http", _cfg.graph_host, _cfg.server_port) + path
    if params is not None:
        url += '?' + urllib.parse.urlencode(params)
    else:
        pass
    res = requests.request(method, url, json=json)
    try:
        return res.status_code, res.json()
    except:
        return res.status_code, res.content


def gremlin_post(query):
    """
    gremlin  request
    """
    body = {
        "gremlin": query,
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {"graph": "%s" % _cfg.graph_name, "g": "__g_%s" % _cfg.graph_name}
    }
    url = "/gremlin"
    code, res = request(method='post', path=url, json=body)
    return code, res


@pytest.mark.caseL0
def test_gremlin_post():
    """
    执行gremlin post请求的同步任务
    进行清空操作
    """
    query = "g.V().limit(10);"
    code, res = gremlin_post(query)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == []


if __name__ == "__main__":
    pass
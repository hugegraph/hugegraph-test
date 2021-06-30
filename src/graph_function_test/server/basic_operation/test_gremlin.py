# -*- coding:utf-8 -*-
"""
author     : lxb
note       : gremlin api 测试
create_time:
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Gremlin
from src.config import basic_config as _cfg
from src.common.task_res import get_task_res
from src.common.tools import clear_graph

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def init_graph():
    """
    对测试环境进行初始化操作
    """
    if _cfg.server_backend == 'cassandra':
        clear_graph()
    else:
        code, res = Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # 适用gremlin语句进行truncate操作
        assert code == 200


def test_gremlin_get():
    """
    执行gremlin get请求的同步任务
    """
    init_graph()
    param = {"gremlin": "%s.traversal().V().count()" % _cfg.graph_name}
    code, res = Gremlin().gremlin_get(param=param, auth=auth)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == [0]


def test_gremlin_post():
    """
    执行gremlin post请求的同步任务
    进行清空操作
    """
    query = "g.V().limit(10);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == []


def test_gremlin_job():
    """
    执行gremlin异步任务
    """
    init_graph()
    query = "g.V().count();"
    code, res = Gremlin().gremlin_job(query, auth=auth)
    print(code, res)
    assert code == 201
    assert res == {'task_id': 1}
    t_res = get_task_res(res['task_id'], 30, auth=auth)
    assert str(t_res) == '[0]'


if __name__ == "__main__":
    pass

# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 
create_time:  
"""
import os
import sys
import pytest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Gremlin
from src.config import basic_config as _cfg
from src.common.server_api import Task

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def init_graph():
    """
    对测试环境进行初始化操作
    """
    query = "graph.truncateBackend();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200


@pytest.mark.caseL0
def test_gremlin_get():
    """
    执行gremlin get请求的同步任务
    """
    init_graph()
    param = {"gremlin": "hugegraph.traversal().V().count()"}
    code, res = Gremlin().gremlin_get(param=param, auth=auth)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == [0]


@pytest.mark.caseL0
def test_gremlin_post():
    """
    执行gremlin post请求的同步任务
    进行清空操作
    """
    query = "graph.truncateBackend();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == [None]


@pytest.mark.caseL0
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
    t_code, t_res = Task().get_task(1, auth=auth)
    print(t_code, t_res)
    assert t_code == 200
    assert t_res['task_name'] == query and t_res['task_result'] == '[0]'


if __name__ == "__main__":
    pass

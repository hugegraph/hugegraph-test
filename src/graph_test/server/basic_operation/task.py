# -*- coding:utf-8 -*-
"""
author     : lxb
note       : task
create_time:  
"""
import os
import sys
import pytest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Task
from src.common.server_api import Gremlin
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def init_graph():
    """
    对测试环境进行初始化操作
    """
    query = "graph.truncateBackend();" \
            "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
            ".properties('name', 'age', 'date').ifNotExist().create();" \
            "a = graph.addVertex(T.label, 'person', 'name', 'marko');" \
            "b = graph.addVertex(T.label, 'person', 'name', 'vadas');" \
            "a.addEdge('link', b, 'name', 'test', 'age', 29, 'date', '2021-02-07');"
    print(query)
    code, res = Gremlin().gremlin_post(query, auth=auth)
    return code == 200


@pytest.mark.caseL0
def test_get_task():
    """
    获取执行成功的所有tasks
    :return:
    """
    if init_graph():
        code, res = Gremlin().gremlin_job("g.V().count()", auth=auth)
        print(code, res)
        if code == 201:
            param = {'status': 'SUCCESS'}
            t_code, t_res = Task().get_tasks(param=param, auth=auth)
            print(t_code, t_res)
            assert t_code == 200
            assert t_res['tasks'][0]['task_name'] == 'g.V().count()'
        else:
            pass
    else:
        assert 0


def test_get_task_by_id_01():
    """
    根据ID获取task结果
    :return:
    """


def test_delete_task_01():
    """
    删除某个task的信息（不删除任务本身）
    :return:
    """


def test_cancle_task_01():
    """
    取消某个任务
    :return:
    """


if __name__ == "__main__":
    pass


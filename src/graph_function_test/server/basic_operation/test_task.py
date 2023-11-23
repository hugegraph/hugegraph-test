# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 测试task api相关的cases
create_time:  
"""
import os
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Task
from src.common.server_api import Gremlin
from src.config import basic_config as _cfg
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
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # 适用gremlin语句进行truncate操作

    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
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


def test_get_task():
    """
    获取执行成功的所有tasks
    :return:
    """
    if init_graph():
        code, res = Gremlin().gremlin_job("g.V().count()", auth=auth)
        print(code, res)
        time.sleep(3)
        if code == 201:
            param = {'status': 'SUCCESS'}
            time.sleep(30)
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
    if init_graph():
        code, res = Gremlin().gremlin_job(query="g.V().count()", auth=auth)
        print(code, res)
        assert code == 201
        code, res = Gremlin().gremlin_job(query="g.E().count()", auth=auth)
        print(code, res)
        assert code == 201

        time.sleep(3)


        code, res = Task().get_task(id=res['task_id'], auth=auth)
        print(code, res)
        assert code == 200
        assert (res['task_name'] == "g.E().count()")
        assert (res['task_status'] == "success")
        assert (res['task_result'] == "[1]")


def test_delete_task_01():
    """
    删除某个task的信息（不删除任务本身）
    :return:
    """
    if init_graph():
        code, res = Gremlin().gremlin_job(query="g.V().count()", auth=auth)
        print(code, res)
        assert code == 201
        code, res = Gremlin().gremlin_job(query="g.E().count()", auth=auth)
        print(code, res)
        assert code == 201
        time.sleep(3)

        code, res = Task().delete_task(task_id=res['task_id'], auth=auth)
        print(code, res)
        assert code == 204


# def test_cancel_task_01():
#     """
#     取消某个任务
#     :return:
#     """
#     if init_graph():
#         code, res = Gremlin().gremlin_job(query="g.V().count()", auth=auth)
#         print(code, res)
#         assert code == 201
#         code, res = Gremlin().gremlin_job(query="g.V('1:marko').repeat(both()).times(100000000)", auth=auth)
#         print(code, res)
#         assert code == 201
#         time.sleep(3)
#
#         task_id = 2
#         code, res = Task().put_task(task_id=task_id, auth=auth)
#         print(code, res)
#         assert code == 202
#         assert (res['task_name'] == "g.V('1:marko').repeat(both()).times(100000000)")
#         assert (res['task_status'] == "cancelling")


def test_compulsory_cancle_task_01():
    """
    强制删除某个任务
    :return:
    """
    if init_graph():
        code, res = Gremlin().gremlin_job(query="g.V().count()", auth=auth)
        print(code, res)
        assert code == 201
        code, res = Gremlin().gremlin_job(query="g.V('1:marko').repeat(both()).times(100000000)", auth=auth)
        print(code, res)
        assert code == 201
        time.sleep(3)

        task_id = 2
        code, res = Task().compulsory_delete_task(task_id=task_id, auth=auth)
        print(code, res)
        assert code == 204


if __name__ == "__main__":
    pass


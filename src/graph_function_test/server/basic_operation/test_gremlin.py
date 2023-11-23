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
from src.common.server_api import Graph

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def init_graph():
    """
    对测试环境进行初始化操作
    """
    # if _cfg.server_backend == 'cassandra':
    #     clear_graph()
    # else:
    #     code, res = Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # 适用gremlin语句进行truncate操作
    #     assert code == 200
    code, res = Graph().put_clear_graphs(json={"action": "clear", "clear_schema": True}, auth=auth)
    print(code, res)


# def test_gremlin_get():
#     """
#     执行gremlin get请求的同步任务
#     """
#     # 没有点创建点
#     init_graph()
#     query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
#             "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
#             "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
#             "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
#             "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
#             "c=graph.addVertex(T.label, 'person', 'name', 'c', 'age', 29);" \
#             "d=graph.addVertex(T.label, 'person', 'name', 'd', 'age', 27);" \
#             "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 29);"
#     code, res = Gremlin().gremlin_post(query, auth=auth)
#     assert code == 200
#
#     param = {"gremlin": "%s.traversal().V().count()" % _cfg.graph_name}
#     code, res = Gremlin().gremlin_get(param=param, auth=auth)
#     print(code, res)
#     assert code == 200
#     assert res['result']['data'] == [5]


def test_gremlin_post_clear():
    """
    执行gremlin post请求的同步任务
    进行清空操作
    """
    query = "graph.truncateBackend();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == [None]


def test_gremlin_post_vertex():
    """
    执行gremlin post请求的同步任务
    查询所有的点，限制返回的点的数量为5
    """
    #没有点创建点
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "c=graph.addVertex(T.label, 'person', 'name', 'c', 'age', 29);" \
            "d=graph.addVertex(T.label, 'person', 'name', 'd', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 29);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().limit(5);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 5


def test_gremlin_post_vertex_valuemap():
    """
    执行gremlin post请求的同步任务
    查询点所有属性，限制返回的点的数量为5
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "c=graph.addVertex(T.label, 'person', 'name', 'c', 'age', 29);" \
            "d=graph.addVertex(T.label, 'person', 'name', 'd', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 29);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().limit(5).valueMap();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 5


def test_gremlin_post_vertex_label():
    """
    执行gremlin post请求的同步任务
    查询点所有label，限制返回的点的数量为5
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "c=graph.addVertex(T.label, 'person', 'name', 'c', 'age', 29);" \
            "d=graph.addVertex(T.label, 'person', 'name', 'd', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 29);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().limit(5).label();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 5


def test_gremlin_post_edge():
    """
    执行gremlin post请求的同步任务
    查询所有的边，限制返回的点的数量为10
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('help').sourceLabel('person').targetLabel('person').ifNotExist().create();"\
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "c=graph.addVertex(T.label, 'person', 'name', 'c', 'age', 29);" \
            "d=graph.addVertex(T.label, 'person', 'name', 'd', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 29);" \
            "a.addEdge('help', b);"\
            "b.addEdge('help', c);"\
            "c.addEdge('help', d);"\
            "d.addEdge('help', e);"\
            "e.addEdge('help', a);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.E().limit(5);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 5


def test_gremlin_post_delete_vertex():
    """
    执行gremlin post请求的同步任务
    删除ID为a的点。
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('help').sourceLabel('person').targetLabel('person').ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V('a').drop();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == []


def test_gremlin_post_delete_edge():
    """
    执行gremlin post请求的同步任务
    根据id删除边
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('help').sourceLabel('person').targetLabel('person').ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "a.addEdge('help', b);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.E('S1:a>1>>S1:b').drop()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert res['result']['data'] == []


def test_gremlin_post_has_label():
    """
    执行gremlin post请求的同步任务
    根据person类型过滤
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('help').sourceLabel('person').targetLabel('person').ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "a.addEdge('help', b);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().hasLabel('person')"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 2


def test_gremlin_post_has_label_tow():
    """
    执行gremlin post请求的同步任务
    根据person software类型过滤
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('lang').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('price').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().vertexLabel('software').properties('name', 'lang', 'price').primaryKeys('name')"\
            ".ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "c=graph.addVertex(T.label, 'software', 'name', 'c', 'lang', 'java', 'price', 328);" \
            "d=graph.addVertex(T.label, 'software', 'name', 'd', 'lang', 'java', 'price', 199);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().hasLabel('person', 'software')"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 4


def test_gremlin_post_has_lt():
    """
    执行gremlin post请求的同步任务
    过滤年龄小于30的
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('lang').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('price').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().vertexLabel('software').properties('name', 'lang', 'price').primaryKeys('name')"\
            ".ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 31);" \
            "f=graph.addVertex(T.label, 'person', 'name', 'f', 'age', 33);" \
            "c=graph.addVertex(T.label, 'software', 'name', 'c', 'lang', 'java', 'price', 328);" \
            "d=graph.addVertex(T.label, 'software', 'name', 'd', 'lang', 'java', 'price', 199);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200

    query = "g.V().has('age', lt(30))"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 2


def test_gremlin_post_has_lte():
    """
    执行gremlin post请求的同步任务
    过滤年龄小于等于30的顶点
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('lang').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('price').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().vertexLabel('software').properties('name', 'lang', 'price').primaryKeys('name')"\
            ".ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 31);" \
            "f=graph.addVertex(T.label, 'person', 'name', 'f', 'age', 33);" \
            "g=graph.addVertex(T.label, 'person', 'name', 'g', 'age', 30);" \
            "c=graph.addVertex(T.label, 'software', 'name', 'c', 'lang', 'java', 'price', 328);" \
            "d=graph.addVertex(T.label, 'software', 'name', 'd', 'lang', 'java', 'price', 199);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().has('age', lte(30));"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 3


def test_gremlin_post_has_gt():
    """
    执行gremlin post请求的同步任务
    过滤年龄大于30的顶点
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('lang').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('price').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().vertexLabel('software').properties('name', 'lang', 'price').primaryKeys('name')" \
            ".ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 31);" \
            "f=graph.addVertex(T.label, 'person', 'name', 'f', 'age', 33);" \
            "g=graph.addVertex(T.label, 'person', 'name', 'g', 'age', 30);" \
            "c=graph.addVertex(T.label, 'software', 'name', 'c', 'lang', 'java', 'price', 328);" \
            "d=graph.addVertex(T.label, 'software', 'name', 'd', 'lang', 'java', 'price', 199);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().has('age', gt(30))"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['result']['data']) == 2


def test_gremlin_job():
    """
    执行gremlin异步任务
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('help').sourceLabel('person').targetLabel('person').ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "c=graph.addVertex(T.label, 'person', 'name', 'c', 'age', 29);" \
            "d=graph.addVertex(T.label, 'person', 'name', 'd', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 29);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().count();"
    code, res = Gremlin().gremlin_job(query=query, auth=auth)
    print(code, res)
    assert code == 201
    assert res == {'task_id': 1}
    t_res = get_task_res(res['task_id'], 30, auth=auth)
    print(t_res)
    assert str(t_res) == '[5]'


def test_gremlin_job_has_count():
    """
    执行gremlin异步任务
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('lang').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('price').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().vertexLabel('software').properties('name', 'lang', 'price').primaryKeys('name')"\
            ".ifNotExist().create();" \
            "a=graph.addVertex(T.label, 'person', 'name', 'a', 'age', 29);" \
            "b=graph.addVertex(T.label, 'person', 'name', 'b', 'age', 27);" \
            "e=graph.addVertex(T.label, 'person', 'name', 'e', 'age', 31);" \
            "f=graph.addVertex(T.label, 'person', 'name', 'f', 'age', 33);" \
            "g=graph.addVertex(T.label, 'person', 'name', 'g', 'age', 30);" \
            "c=graph.addVertex(T.label, 'software', 'name', 'c', 'lang', 'java', 'price', 328);" \
            "d=graph.addVertex(T.label, 'software', 'name', 'd', 'lang', 'java', 'price', 199);"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    query = "g.V().has('lang','java').count();"
    code, res = Gremlin().gremlin_job(query=query, auth=auth)
    print(code, res)
    assert code == 201
    assert res == {'task_id': 1}
    t_res = get_task_res(res['task_id'], 30, auth=auth)
    assert str(t_res) == '[2]'


if __name__ == "__main__":
    pass

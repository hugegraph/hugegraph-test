# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 边相关api cases测试
create_time:  
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Gremlin
from src.common.server_api import Edge
from src.config import basic_config as _cfg
from src.common.tools import clear_graph

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def init_graph():
    """
    清理图
    :return:
    """
    if _cfg.server_backend == 'cassandra':
        clear_graph()
    else:
        code, res = Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # 适用gremlin语句进行truncate操作
        print(code, res)


def test_create_edge():
    """
    没有索引 + 添加边数据
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
            ".properties('name', 'age', 'date').ifNotExist().create();" \
            "graph.addVertex(T.label, 'person', 'name', 'marko');" \
            "graph.addVertex(T.label, 'person', 'name', 'vadas');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)

    if code == 200:
        body = {
            "label": "link",
            "outV": "1:marko",
            "inV": "1:vadas",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "name": "peter",
                "age": 21,
                "date": "2017-5-18"
            }
        }
        code, res = Edge().create_single_edge(body, auth=auth)
        print(code, res)
        ### 断言
        assert code == 201
        assert res['id'] == 'S1:marko>1>>S1:vadas'
    else:
        print('环境初始化失败')
        assert 0


def test_get_edge_by_property():
    """
    根据条件获取边(起点、终点为同一个点)
    :return:
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create();" \
            "marko = graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 18);" \
            "vadas = graph.addVertex(T.label, 'person', 'name', 'vadas', 'age', 19);" \
            "marko.addEdge('link', vadas, 'date', '2021-05-07');" \
            "marko.addEdge('link', marko, 'date', '2021-06-08');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200

    condition = {'vertex_id': '"1:marko"'}
    code, res = Edge().get_filter_edge(condition=condition, auth=auth)
    print(code, res)  # 有点重复展示问题，暂时不修复
    assert code == 200
    assert len(res['edges']) == 3


def test_get_edge_by_page():
    """
    根据条件获取边
    :return:
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create();" \
            "marko = graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 18);" \
            "vadas = graph.addVertex(T.label, 'person', 'name', 'vadas', 'age', 19);" \
            "marko.addEdge('link', vadas, 'date', '2021-05-07');" \
            "marko.addEdge('link', marko, 'date', '2021-06-08');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200

    condition = {'vertex_id': '"1:marko"', 'limit': 1, 'page': ''}
    code, res = Edge().get_filter_edge(condition=condition, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['edges']) == 1
    assert res['page'] != ''


if __name__ == "__main__":
    pass

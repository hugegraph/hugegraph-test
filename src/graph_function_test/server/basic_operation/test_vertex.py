# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 测试顶点api相关的cases
create_time:  
"""
import os
import sys
import pytest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Vertex
from src.common.server_api import Gremlin
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


def test_create_vertex_single():
    """
    没有索引 + 添加数据 + 字段（Text、int、date）
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').primaryKeys('name')" \
            ".ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200

    body = {
        "label": "person",
        "properties": {
            "name": "marko",
            "age": 29,
            "date": "2021-02-07"
        }
    }
    code, res = Vertex().create_single_vertex(body=body, auth=auth)
    print(code, res)
    ### 断言
    assert code == 201
    assert res['id'] == '1:marko'


def test_create_vertex_batch():
    """
    没有索引 + 添加数据 + 字段（Text、int、date）
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').primaryKeys('name')" \
            ".ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = [
        {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 29,
                "date": "2021-02-07"
            }
        },
        {
            "label": "person",
            "properties": {
                "name": "peter",
                "age": 27,
                "date": "2020-02-07"
            }
        }
    ]
    code, res = Vertex().create_batch_vertex(body=body, auth=auth)
    print(code, res)
    ### 断言
    assert code == 201
    assert res == ['1:marko', '1:peter']


def test_update_vertex_single():
    """
    没有索引 + 添加数据 + 字段（Text、int、date）
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').primaryKeys('name')" \
            ".ifNotExist().create();" \
            "graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 29, 'date', '2021-02-07');" \
            "graph.addVertex(T.label, 'person', 'name', 'peter', 'age', 27, 'date', '2020-02-07');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    v_id = '"1:marko"'
    action = {'action': 'append'}
    body = {
        "label": "person",
        "properties": {
            "age": 39,
            "date": "2021-02-07"
        }
    }
    code, res = Vertex().update_vertex_property(v_id=v_id, action=action, body=body, auth=auth)
    print(code, res)
    ### 断言
    assert code == 200
    assert res['properties']['age'] == 39


def test_update_vertex_batch():
    """
    没有索引 + 添加数据 + 字段（Text、int、date）
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').primaryKeys('name')" \
            ".ifNotExist().create();" \
            "graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 29, 'date', '2021-02-07');" \
            "graph.addVertex(T.label, 'person', 'name', 'peter', 'age', 27, 'date', '2020-02-07');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        'vertices': [
            {
                "label": "person",
                "type": "vertex",
                "properties": {
                    "name": "marko",
                    "age": 39,
                    "date": "2012-02-07"
                }
            },
            {
                "label": "person",
                "type": "vertex",
                "properties": {
                    "name": "peter",
                    "age": 39,
                    "date": "2012-02-07"

                }
            },
            {
                "label": "person",
                "type": "vertex",
                "properties": {
                    "name": "josh",
                    "age": 39,
                    "date": "2012-02-07"
                }
            }
        ],
        "update_strategies": {
            "name": "OVERRIDE",
            "age": "SUM",
            "date": "BIGGER"
        },
        "create_if_not_exist": True
    }
    code, res = Vertex().update_vertex_batch_property(body=body, auth=auth)
    print(code, res)
    ### 有bug：date属性数据进行批量更新时，使用bigger、smaller策略报错
    assert code == 200


def test_get_vertex_by_page():
    """
    测试page
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

    condition = {'label': 'person', 'limit': 1, 'page': ''}
    code, res = Vertex().get_filter_vertex(condition=condition, auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['vertices']) == 1
    assert res['page'] != ''


def test_eliminate_vertex_single():
    """
    没有索引 + 添加数据 + 字段（Text、int、date）
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').nullableKeys('age', 'date')" \
            ".primaryKeys('name').ifNotExist().create();" \
            "graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 29, 'date', '2021-02-07');" \
            "graph.addVertex(T.label, 'person', 'name', 'peter', 'age', 27, 'date', '2020-02-07');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    v_id = '"1:marko"'
    action = {'action': 'eliminate'}
    body = {
        "label": "person",
        "properties": {
            "age": 29
        }
    }
    code, res = Vertex().update_vertex_property(v_id=v_id, action=action, body=body, auth=auth)
    print(code, res)
    ### 断言
    assert code == 200
    assert res['properties'] == {'name': 'marko', 'date': '2021-02-07 00:00:00.000'}


def test_get_vertex_by_id():
    """
    通过 id 查询 vertex
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').nullableKeys('age', 'date')" \
            ".primaryKeys('name').ifNotExist().create();" \
            "graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 29, 'date', '2021-02-07');" \
            "graph.addVertex(T.label, 'person', 'name', 'peter', 'age', 27, 'date', '2020-02-07');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    v_id = '"1:marko"'
    code, res = Vertex().get_vertex_by_id(v_id=v_id, auth=auth)
    print(code, res)
    ### 断言
    assert code == 200
    assert res['properties'] == {'name': 'marko', 'age': 29, 'date': '2021-02-07 00:00:00.000'}


def test_delete_vertex_by_id():
    """
    通过 id 删除 vertex
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').nullableKeys('age', 'date')" \
            ".primaryKeys('name').ifNotExist().create();" \
            "graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 29, 'date', '2021-02-07');" \
            "graph.addVertex(T.label, 'person', 'name', 'peter', 'age', 27, 'date', '2020-02-07');"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    v_id = '"1:marko"'
    code, res = Vertex().delete_vertex(v_id=v_id, auth=auth)
    print(code, res)
    ### 断言
    assert code == 204


if __name__ == "__main__":
    pass

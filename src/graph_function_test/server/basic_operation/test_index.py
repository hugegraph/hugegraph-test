# -*- coding:utf-8 -*-
"""
author     : lxb
note       : indexlabel 相关的api cases测试
create_time:  
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Schema
from src.common.server_api import Gremlin
from src.common.task_res import get_task_res
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


def test_create_range_vertex_indexlabel():
    """
    int类型的属性 & range索引 & vertexlabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "rangeByAgeByVertex",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "RANGE",
        "fields": [
            "age"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_range_edge_indexlabel():
    """
    int类型的属性 & range索引 & edgelabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "rangeByDateByEdge",
        "base_type": "EDGE_LABEL",
        "base_value": "knows",
        "index_type": "RANGE",
        "fields": [
            "date"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_secondary_vertex_indexlabel():
    """
    int类型的属性 & secondary索引 & vertexlabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "secondaryByAgeByVertex",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "SECONDARY",
        "fields": [
            "age"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_secondary_edge_indexlabel():
    """
    int类型的属性 & secondary索引 & edgelabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "secondaryByDateByEdge",
        "base_type": "EDGE_LABEL",
        "base_value": "knows",
        "index_type": "SECONDARY",
        "fields": [
            "date"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_search_vertex_indexlabel_int_error():
    """
    int类型的属性 & search索引 & vertexlabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "searchByAgeByVertex",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "SEARCH",
        "fields": [
            "age"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 400
    assert res['message'] == "Search index can only build on text property, but got INT(age)"


def test_create_search_vertex_indexlabel_text():
    """
    int类型的属性 & search索引 & vertexlabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('address').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'address')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date', 'address').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "searchByAgeByVertex",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "SEARCH",
        "fields": [
            "address"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_search_edge_indexlabel_text():
    """
    int类型的属性 & search索引 & edgelabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().propertyKey('address').asText().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date', 'address').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "searchByDateByEdge",
        "base_type": "EDGE_LABEL",
        "base_value": "knows",
        "index_type": "SEARCH",
        "fields": [
            "address"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_shard_vertex_indexlabel():
    """
    int类型的属性 & shard索引 & vertexlabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "shardByAgeByVertex",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "SHARD",
        "fields": [
            "age"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_shard_edge_indexlabel():
    """
    int类型的属性 & shard索引 & edgelabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "shardByDateByEdge",
        "base_type": "EDGE_LABEL",
        "base_value": "knows",
        "index_type": "SHARD",
        "fields": [
            "date"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_unique_vertex_indexlabel():
    """
    int类型的属性 & unique索引 & vertexlabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "uniqueByAgeByVertex",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "UNIQUE",
        "fields": [
            "age"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_create_unique_edge_indexlabel():
    """
    int类型的属性 & unique索引 & edgelabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    body = {
        "name": "uniqueByDateByEdge",
        "base_type": "EDGE_LABEL",
        "base_value": "knows",
        "index_type": "UNIQUE",
        "fields": [
            "date"
        ]
    }
    code, res = Schema().create_index(body, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


def test_get_indexlabel_by_name():
    """
    根据name查询vertexlabel
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create();" \
            "graph.schema().indexLabel('rangeByAgeByVertex').onV('person').by('age').range().ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    index_name = 'rangeByAgeByVertex'
    code, res = Schema().get_index_by_name(index_name, auth=auth)
    print(code, res)
    assert code == 200
    assert res['name'] == 'rangeByAgeByVertex'


def test_get_all_indexlabels():
    """
    查询所有vertexlabels
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create();" \
            "graph.schema().indexLabel('rangeByAgeByVertex').onV('person').by('age').range().ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    code, res = Schema().get_index(auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['indexlabels']) == 1
    assert res['indexlabels'][0]['name'] == 'rangeByAgeByVertex'


def test_delete_indexlabel():
    """
    删除索引
    :return:
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age')" \
            ".primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create();" \
            "graph.schema().indexLabel('rangeByAgeByVertex').onV('person').by('age').range().ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    assert code == 200

    index_name = 'rangeByAgeByVertex'
    code, res = Schema().delete_index(index_name, auth=auth)
    print(code, res)
    assert code == 202
    task_id = res['task_id']
    result = get_task_res(task_id, 120, auth=auth)
    if result:
        assert 1


if __name__ == "__main__":
    pass



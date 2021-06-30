# -*- coding:utf-8 -*-
"""
author     : lxb
note       : vertexlabel相关api的cases测试
create_time:  
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Schema
from src.common.server_api import Gremlin
from src.config import basic_config as _cfg
from src.common.tools import clear_graph
from src.common.task_res import get_task_res

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
            "graph.schema().propertyKey('city').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('lang').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('price').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('test').properties('name').primaryKeys('name').ifNotExist().create()"

    code, res = Gremlin().gremlin_post(query, auth=auth)
    return code == 200


def test_create_vertexlabel_default_id():
    """
    ID为默认类型
    """
    body = {
        "name": "person",
        "id_strategy": "DEFAULT",
        "properties": [
            "name"
        ],
        "primary_keys": [
            "name"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_vertexLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['id_strategy'] == 'PRIMARY_KEY'
    else:
        print('环境初始化失败')
        assert 0


def test_create_vertexlabel_primaryKey_id():
    """
    ID为主键类型
    """
    body = {
        "name": "person",
        "id_strategy": "PRIMARY_KEY",
        "properties": [
            "name"
        ],
        "primary_keys": [
            "name"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_vertexLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['id_strategy'] == 'PRIMARY_KEY'
    else:
        print('环境初始化失败')
        assert 0


def test_create_vertexlabel_automatic_id():
    """
    ID为主键类型
    """
    body = {
        "name": "person",
        "id_strategy": "AUTOMATIC",
        "properties": [
            "name",
            "age"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_vertexLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['id_strategy'] == 'AUTOMATIC'
    else:
        print('环境初始化失败')
        assert 0


def test_create_vertexlabel_customize_number_id():
    """
    ID为主键类型
    """
    body = {
        "name": "person",
        "id_strategy": "CUSTOMIZE_NUMBER",
        "properties": [
            "name",
            "age"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_vertexLabel(body, auth=auth)
        print(code, res)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['id_strategy'] == 'CUSTOMIZE_NUMBER'
    else:
        print('环境初始化失败')
        assert 0


def test_create_vertexlabel_customize_string_id():
    """
    ID为主键类型
    """
    body = {
        "name": "person",
        "id_strategy": "CUSTOMIZE_STRING",
        "properties": [
            "name",
            "age"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_vertexLabel(body, auth=auth)
        print(code, res)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['id_strategy'] == 'CUSTOMIZE_STRING'
    else:
        print('环境初始化失败')
        assert 0


def test_update_vertexlabel_append_properties_userdata():
    """
    ID为主键类型
    """
    property_name = 'test'
    body = {
        "name": property_name,
        "properties": [
            "city"
        ],
        "nullable_keys": ["city"],
        "user_data": {
            "super": "animal"
        }
    }
    if init_graph():
        code, res = Schema().update_vertexLabel(property_name, {"action": "append"}, body, auth=auth)
        print(code, res)
        assert code == 200
        assert res['properties'] == ['name', 'city']
        assert res['user_data']['super'] == 'animal'
    else:
        print('环境初始化失败')
        assert 0


def test_update_vertexlabel_eliminate_userdata():
    """
    ID为主键类型
    """
    init_graph()
    property_name = 'test'
    # append property && userdata
    append_body = {
        "name": property_name,
        "properties": [
            "city"
        ],
        "nullable_keys": ["city"],
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().update_vertexLabel(property_name, {"action": "append"}, append_body, auth=auth)
    print(code, res)
    assert code == 200
    assert res['properties'] == ['name', 'city']
    assert res['user_data']['super'] == 'animal'

    # eliminate
    eliminate_body = {
        "name": property_name,
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().update_vertexLabel(property_name, {"action": "eliminate"}, eliminate_body, auth=auth)
    print(code, res)
    assert code == 200
    assert 'super' not in res['user_data']


def test_get_vertexlabel_all():
    """
    获取vertex label
    """
    init_graph()
    property_name = "person"
    body = {
        "name": property_name,
        "id_strategy": "DEFAULT",
        "properties": [
            "name"
        ],
        "primary_keys": [
            "name"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    code, res = Schema().create_vertexLabel(body, auth=auth)
    assert code == 201

    # get all vertexLabel
    code, res = Schema().get_vertexLabel(auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['vertexlabels']) == 2
    assert res['vertexlabels'][0]['name'] == 'test'
    assert res['vertexlabels'][1]['name'] == 'person'


def test_get_vertexlabel_by_name():
    """
    通过name查询vertexLabel
    """
    init_graph()
    property_name = "person"
    body = {
        "name": property_name,
        "id_strategy": "DEFAULT",
        "properties": [
            "name"
        ],
        "primary_keys": [
            "name"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    code, res = Schema().create_vertexLabel(body, auth=auth)
    assert code == 201

    # get vertexLabel by name
    code, res = Schema().get_vertexLabel_by_name(property_name, auth=auth)
    print(code, res)
    assert code == 200
    assert res['name'] == 'person'


def test_delete_vertexlabel_by_name():
    """
    删除vertexLabel 通过name
    """
    init_graph()
    property_name = "person"
    body = {
        "name": property_name,
        "id_strategy": "DEFAULT",
        "properties": [
            "name"
        ],
        "primary_keys": [
            "name"
        ],
        "nullable_keys": [],
        "enable_label_index": True
    }
    code, res = Schema().create_vertexLabel(body, auth=auth)
    assert code == 201

    # delete vertexLabel by name
    code, res = Schema().delete_vertexLabel(property_name, auth=auth)
    print(code, res)
    assert code == 202

    res = get_task_res(res['task_id'], 60, auth=auth)
    print(res)


if __name__ == "__main__":
    pass


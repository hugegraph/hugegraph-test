# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 测试property相关的api cases
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


def test_create_property_single_text():
    """
    text类型的属性创建
    """
    init_graph()

    body = {
        "name": "name",
        "data_type": "TEXT",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 201
    assert res['data_type'] == 'TEXT'


def test_create_property_single_int():
    """
    int类型的属性创建
    """
    init_graph()

    body = {
        "name": "age",
        "data_type": "INT",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'INT'


def test_create_property_single_time():
    """
    date类型的属性创建
    """
    init_graph()

    body = {
        "name": "time",
        "data_type": "DATE",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'DATE'


def test_create_property_single_uuid():
    """
    uuid类型的属性创建
    """
    init_graph()

    body = {
        "name": "uuid",
        "data_type": "UUID",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'UUID'


def test_create_property_single_boolean():
    """
    boolean类型的属性创建
    """
    init_graph()
    body = {
        "name": "boolean",
        "data_type": "BOOLEAN",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'BOOLEAN'


def test_create_property_single_byte():
    """
    boolean类型的属性创建
    """
    init_graph()

    body = {
        "name": "byte",
        "data_type": "BYTE",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'BYTE'


def test_create_property_single_blob():
    """
    blob类型的属性创建
    """
    init_graph()

    body = {
        "name": "blob",
        "data_type": "BLOB",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'BLOB'


def test_create_property_single_double():
    """
    double类型的属性创建
    """
    init_graph()

    body = {
        "name": "double",
        "data_type": "DOUBLE",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'DOUBLE'


def test_create_property_single_float():
    """
    float类型的属性创建
    """
    init_graph()

    body = {
        "name": "float",
        "data_type": "FLOAT",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'FLOAT'


def test_create_property_single_long():
    """
    float类型的属性创建
    """
    init_graph()

    body = {
        "name": "long",
        "data_type": "LONG",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'LONG'


def test_create_property_set_text():
    """
    text类型set集合的属性创建
    """
    init_graph()

    body = {
        "name": "name",
        "data_type": "TEXT",
        "cardinality": "SET"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'TEXT'


def test_create_property_list_text():
    """
    text类型set集合的属性创建
    """
    init_graph()

    body = {
        "name": "name",
        "data_type": "TEXT",
        "cardinality": "LIST"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'TEXT'


def test_append_userdata():
    """
    添加 userdata
    """
    init_graph()
    body = {
        "name": "age",
        "data_type": "INT",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'INT'

    body = {
        "name": "age",
        "user_data": {
            "min": 0,
            "max": 100
        }
    }
    code, res = Schema().deal_property_userdata("age", {"action": "append"}, body, auth=auth)
    assert code == 202


def test_eliminate_userdata():
    """
    移除 userdata
    """
    init_graph()
    body = {
        "name": "age",
        "data_type": "INT",
        "cardinality": "SINGLE",
        "user_data": {
            "min": 0,
            "max": 100
        }
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 202
    assert res['property_key']['data_type'] == 'INT'

    body = {
        "name": "age",
        "user_data": {
            "min": 0
        }
    }
    code, res = Schema().deal_property_userdata("age", {"action": "eliminate"}, body, auth=auth)
    print(code, res)
    assert code == 202
    assert "min" not in res['property_key']["user_data"]
    assert res['property_key']["user_data"]["max"] == 100


def test_get_all_property():
    """
    获取所有属性
    """
    init_graph()
    body = {
        "name": "age",
        "data_type": "INT",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 201
    assert res['data_type'] == 'INT'

    code, res = Schema().get_all_properties(auth=auth)
    print(code, res)
    assert code == 200
    assert len(res['propertykeys']) == 1
    assert res['propertykeys'][0]['name'] == 'age'


def test_get_property_by_name():
    """
    通过name获取属性
    """
    init_graph()
    body = {
        "name": "age",
        "data_type": "INT",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 201
    assert res['data_type'] == 'INT'

    code, res = Schema().get_property_by_name('age', auth=auth)
    print(code, res)
    assert code == 200
    assert res['name'] == 'age'


def test_delete_property_by_name():
    """
    通过name删除属性
    """
    init_graph()
    body = {
        "name": "age",
        "data_type": "INT",
        "cardinality": "SINGLE"
    }
    code, res = Schema().create_property(body, auth=auth)
    print(code, res)
    assert code == 201
    assert res['data_type'] == 'INT'

    code, res = Schema().delete_property_by_name('age', auth=auth)
    print(code, res)
    assert code == 204


if __name__ == "__main__":
    pass

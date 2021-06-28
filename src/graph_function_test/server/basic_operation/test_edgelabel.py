# -*- coding:utf-8 -*-
"""
author     : lxb
note       : edgelabel 相关api cases测试
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
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person_name').properties('name').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().vertexLabel('person_age').properties('age').primaryKeys('age').ifNotExist().create();" \
            "graph.schema().vertexLabel('person_date').properties('date').primaryKeys('date').ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    return code == 200


def test_create_edgeLabel_text_link_text():
    """
    无属性
    """
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_name",
        "frequency": "SINGLE",
        "properties": [
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_edgeLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['properties'] == []
    else:
        print('环境初始化失败')
        assert 0


def test_create_edgeLabel_text_link_int():
    """
    无属性
    """
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_age",
        "frequency": "SINGLE",
        "properties": [
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_edgeLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['properties'] == []
    else:
        print('环境初始化失败')
        assert 0


def test_create_edgeLabel_int_link_int():
    """
    无属性
    """
    body = {
        "name": "link",
        "source_label": "person_age",
        "target_label": "person_age",
        "frequency": "SINGLE",
        "properties": [
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_edgeLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['properties'] == []
    else:
        print('环境初始化失败')
        assert 0


def test_create_edgeLabel_text_link_date():
    """
    无属性
    """
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_date",
        "frequency": "SINGLE",
        "properties": [
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_edgeLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['properties'] == []
    else:
        print('环境初始化失败')
        assert 0


def test_create_edgeLabel_date_link_date():
    """
    无属性
    """
    body = {
        "name": "link",
        "source_label": "person_date",
        "target_label": "person_date",
        "frequency": "SINGLE",
        "properties": [
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_edgeLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['properties'] == []
    else:
        print('环境初始化失败')
        assert 0


def test_create_edgeLabel_int_link_date():
    """
    无属性
    """
    body = {
        "name": "link",
        "source_label": "person_age",
        "target_label": "person_date",
        "frequency": "SINGLE",
        "properties": [
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }
    if init_graph():
        code, res = Schema().create_edgeLabel(body, auth=auth)
        assert code == 201
        assert res['status'] == 'CREATED'
        assert res['properties'] == []
    else:
        print('环境初始化失败')
        assert 0


def test_append_edgeLabel_proeprty_userdata():
    """
    添加 property、userdata
    """
    init_graph()
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_name",
        "frequency": "SINGLE",
        "properties": [
        ],
        "sort_keys": [],
        "nullable_keys": [],
        "enable_label_index": True
    }
    code, res = Schema().create_edgeLabel(body, auth=auth)
    assert code == 201
    assert res['status'] == 'CREATED'
    assert res['properties'] == []

    # append property && userdata
    property_name = "link"
    append_body = {
        "name": property_name,
        "properties": [
            "name"
        ],
        "nullable_keys": [
            "name"
        ],
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().update_edgeLabel(property_name, {"action": "append"}, append_body, auth=auth)
    print(code, res)
    assert 200
    assert res['name'] == 'link'
    assert res['user_data']['super'] == 'animal'


def test_eliminate_edgeLabel_userdata():
    """
    添加 property、userdata
    """
    init_graph()
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_name",
        "frequency": "SINGLE",
        "properties": [
            "name"
        ],
        "sort_keys": [],
        "nullable_keys": ["name"],
        "enable_label_index": True,
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().create_edgeLabel(body, auth=auth)
    assert code == 201
    assert res['status'] == 'CREATED'
    assert res['properties'] == ['name']

    # eliminate property && userdata
    property_name = "link"
    append_body = {
        "name": property_name,
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().update_edgeLabel(property_name, {"action": "eliminate"}, append_body, auth=auth)
    print(code, res)
    assert 200
    assert res['name'] == 'link'
    assert 'super' not in res['user_data']


def test_get_edgeLabel_all():
    """
    查看所有edgeLabel
    """
    init_graph()
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_name",
        "frequency": "SINGLE",
        "properties": [
            "name"
        ],
        "sort_keys": [],
        "nullable_keys": ["name"],
        "enable_label_index": True,
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().create_edgeLabel(body, auth=auth)
    assert code == 201
    assert res['status'] == 'CREATED'
    assert res['properties'] == ['name']

    # eliminate property && userdata
    code, res = Schema().get_edgeLabel(auth=auth)
    print(code, res)
    assert 200
    assert len(res['edgelabels']) == 1
    assert res['edgelabels'][0]['name'] == 'link'


def test_get_edgeLabel_by_name():
    """
    根据name查看edgeLabel
    """
    init_graph()
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_name",
        "frequency": "SINGLE",
        "properties": [
            "name"
        ],
        "sort_keys": [],
        "nullable_keys": ["name"],
        "enable_label_index": True,
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().create_edgeLabel(body, auth=auth)
    assert code == 201
    assert res['status'] == 'CREATED'
    assert res['properties'] == ['name']

    # eliminate property && userdata
    code, res = Schema().get_edgeLabel_by_name("link", auth=auth)
    print(code, res)
    assert 200
    assert res['name'] == 'link'


def test_delete_edgeLabel_by_name():
    """
    根据name查看edgeLabel
    """
    init_graph()
    body = {
        "name": "link",
        "source_label": "person_name",
        "target_label": "person_name",
        "frequency": "SINGLE",
        "properties": [
            "name"
        ],
        "sort_keys": [],
        "nullable_keys": ["name"],
        "enable_label_index": True,
        "user_data": {
            "super": "animal"
        }
    }
    code, res = Schema().create_edgeLabel(body, auth=auth)
    assert code == 201
    assert res['status'] == 'CREATED'
    assert res['properties'] == ['name']

    # eliminate property && userdata
    code, res = Schema().delete_edgeLabel("link", auth=auth)
    print(code, res)
    assert 202

    res = get_task_res(res['task_id'], 60, auth=auth)
    print(res)


if __name__ == "__main__":
    pass


# -*- coding:utf-8 -*-
"""
author     : lxb
note       : property
create_time:  
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')
from src.common.server_api import Schema
from src.common.server_api import Gremlin
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def init_graph():
    """
    对测试环境进行初始化操作
    """
    query = 'graph.truncateBackend()'
    code, res = Gremlin().gremlin_post(query, auth=auth)
    return code == 200


def test_create_property_text_property():
    """
    text类型的属性创建
    """
    body = {
        "name": "name",
        "data_type": "TEXT",
        "cardinality": "SINGLE"
    }
    if init_graph():
        code, res = Schema().create_property(body, auth=auth)
        print(code, res)
        assert code == 201
        assert res['data_type'] == 'TEXT'
    else:
        print('测试初始化失败!')
        assert 0


def test_create_property_02():
    """
    int类型的属性创建
    """
    body = {
        "name": "age",
        "data_type": "INT",
        "cardinality": "SINGLE"
    }
    if init_graph():
        code, res = Schema().create_property(body, auth=auth)
        print(code, res)
        assert code == 201 and res['data_type'] == 'INT'
    else:
        print('测试初始化失败!')
        assert 0


def test_create_property_03():
    """
    date类型的属性创建
    """
    body = {
        "name": "time",
        "data_type": "DATE",
        "cardinality": "SINGLE"
    }
    if init_graph():
        code, res = Schema().create_property(body, auth=auth)
        print(code, res)
        assert code == 201 and res['data_type'] == 'DATE'
    else:
        print('测试初始化失败!')
        assert 0


def test_append_userdata_01():
    """
    添加 userdata
    """
    pass


def test_eliminate_userdata_01():
    """
    移除 userdata
    """
    pass


def test_get_all_property_01():
    """
    获取所有属性
    """
    pass


def test_get_property_byName_01():
    """
    通过name获取属性
    """
    pass


def test_delete_property_01():
    """
    通过name删除属性
    """
    pass


if __name__ == "__main__":
    pass

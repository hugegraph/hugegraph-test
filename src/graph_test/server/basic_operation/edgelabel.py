# -*- coding:utf-8 -*-
"""
author     : lxb
note       : edgelabel
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
    query = "graph.truncateBackend();" \
            "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    return code == 200


def test_create_edgeLabel():
    """
    无属性
    """
    body = {
        "name": "link",
        "source_label": "person",
        "target_label": "person",
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


if __name__ == "__main__":
    pass


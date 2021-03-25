# -*- coding:utf-8 -*-
"""
author     : lxb
note       : indexlabel
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
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age').primaryKeys('name').ifNotExist().create();"\
            "graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')" \
            ".properties('date').ifNotExist().create()"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    return code == 200


def test_create_indexlabel():
    """
    int类型的属性 & range索引 & vertexlabel
    """
    body = {
        "name": "secondaryByAge",
        "base_type": "VERTEX_LABEL",
        "base_value": "person",
        "index_type": "RANGE",
        "fields": [
            "age"
        ]
    }
    if init_graph():
        code, res = Schema().create_index(body, auth=auth)
        print(code, res)
        assert code == 202
        task_id = res['task_id']
        code, res = get_task_res(task_id, 120, auth=auth)
        assert res['task_status'] == 'success'
    else:
        print('环境初始化失败')
        assert 0


if __name__ == "__main__":
    pass



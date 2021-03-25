# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 
create_time:  
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Vertex
from src.common.server_api import Gremlin
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def test_create_vertex():
    """
    没有索引 + 添加数据 + 字段（Text、int、date）
    """
    query = "graph.truncateBackend();" \
            "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date').primaryKeys('name')" \
            ".ifNotExist().create();"
    g_code, g_res = Gremlin().gremlin_post(query, auth=auth)
    if g_code == 200:
        body = {
            "label": "person",
            "properties": {
                "name": "marko",
                "age": 29,
                "date": "2021-02-07"
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=auth)
        print(code, res)
        ### 断言
        assert code == 201
        assert res['id'] == '1:marko'
    else:
        print('环境初始化失败')
        assert 0


if __name__ == "__main__":
    pass

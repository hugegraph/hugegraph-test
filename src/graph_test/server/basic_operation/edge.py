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

from src.common.server_api import Gremlin
from src.common.server_api import Edge
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def test_create_edge():
    """
    没有索引 + 添加边数据
    """
    query = "graph.truncateBackend();" \
            "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name').primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
            ".properties('name', 'age', 'date').ifNotExist().create()" \
            "graph.addVertex(T.label, 'person', 'name', 'marko');" \
            "graph.addVertex(T.label, 'person', 'name', 'vadas');"
    code, res = Gremlin().gremlin_post(query, auth=auth)

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


if __name__ == "__main__":
    pass


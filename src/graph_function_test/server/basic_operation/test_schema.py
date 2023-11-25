# -*- coding:utf-8 -*-
"""
author     : lxb
note       : test_schema
time       : 2021/9/13 17:58
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Gremlin
from src.common.server_api import Schema
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


def test_get_schema_default():
    """
    没有索引 + 添加边数据
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date')" \
            ".primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
            ".properties('name', 'age', 'date').ifNotExist().create();" \
            "a = graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 17, 'date', '2021-09-13');" \
            "b = graph.addVertex(T.label, 'person', 'name', 'vadas', 'age', 18, 'date', '2021-09-12');" \
            "a.addEdge('link', b, 'name', 'li', 'age', 19, 'date', '2021-09-11');" \
            "graph.schema().indexLabel('personByAge').onV('person').by('age').range().ifNotExist().create();" \
            "graph.schema().indexLabel('linkByName').onE('link').by('name').secondary().ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200

    code, res = Schema().get_schema(auth=auth)
    print(code, res)
    ### 断言
    assert code == 200
    assert len(res['propertykeys']) == 3
    assert res['vertexlabels'][0]['name'] == 'person'
    assert res['edgelabels'][0]['name'] == 'link'
    assert len(res['indexlabels']) == 2


def test_get_schema_groovy():
    """
    没有索引 + 添加边数据
    """
    init_graph()
    query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('person').properties('name', 'age', 'date')" \
            ".primaryKeys('name').ifNotExist().create();" \
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
            ".properties('name', 'age', 'date').ifNotExist().create();" \
            "a = graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 17, 'date', '2021-09-13');" \
            "b = graph.addVertex(T.label, 'person', 'name', 'vadas', 'age', 18, 'date', '2021-09-12');" \
            "a.addEdge('link', b, 'name', 'li', 'age', 19, 'date', '2021-09-11');" \
            "graph.schema().indexLabel('personByAge').onV('person').by('age').range().ifNotExist().create();" \
            "graph.schema().indexLabel('linkByName').onE('link').by('name').secondary().ifNotExist().create();"
    code, res = Gremlin().gremlin_post(query, auth=auth)
    print(code, res)
    assert code == 200

    code, res = Schema().get_schema(param={"format": "groovy"}, auth=auth)
    print(code, res)
    ### 断言
    assert code == 200
    assert res['schema'] == "graph.schema().propertyKey('date').asDate().ifNotExist().create();\n" \
                            "graph.schema().propertyKey('age').asInt().ifNotExist().create();\n" \
                            "graph.schema().propertyKey('name').asText().ifNotExist().create();\n\n" \
                            "graph.schema().vertexLabel('person').properties('name','age','date')" \
                            ".primaryKeys('name').enableLabelIndex(true).ifNotExist().create();\n\n" \
                            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                            ".properties('name','age','date').enableLabelIndex(true).ifNotExist().create();\n\n" \
                            "graph.schema().indexLabel('personByAge').onV('person')" \
                            ".by('age').range().ifNotExist().create();\n" \
                            "graph.schema().indexLabel('linkByName').onE('link')" \
                            ".by('name').secondary().ifNotExist().create();\n"


if __name__ == "__main__":
    pass

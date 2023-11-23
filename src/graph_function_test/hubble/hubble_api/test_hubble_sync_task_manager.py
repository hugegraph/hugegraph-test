# -*- coding: UTF-8 -*-
"""
Created by v_changshuai01 at 2021/5/18
"""
import os
import sys
import time
import unittest
import pytest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg
from src.common.hubble_api import GraphConnection, Schema
from src.common.hubble_api import Gremlin
from src.common.hubble_api import ID
from src.common.hubble_api import Task
from src.common.tools import clear_graph
from src.common.server_api import Algorithm
from src.common.task_res import get_task_res

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def init_graph():
    """
    对测试环境进行初始化操作
    """

    code, res = GraphConnection().get_graph_connect()
    assert code == 200
    connection_list = res['data']['records']
    for each in connection_list:
        each_id = each['id']
        each_graph = each['graph']
        each_host = each['host']
        each_port = each['port']
        # clear graph
        if _cfg.server_backend == 'cassandra':
            clear_graph(graph_name=each_graph, graph_host=each_host, graph_port=each_port)
        else:
            graph_id = ID.get_graph_id()
            Gremlin().gremlin_query({"content": 'graph.truncateBackend();'},
                                    graph_id=graph_id)  # 适用gremlin语句进行truncate操作
        # delete graph_connection
        code, res = GraphConnection().delete_graph_connect(each_id)
        assert code == 200


class SyncTaskManagerCase(unittest.TestCase):
    """
    hubble的异步任务管理模块API
    """

    def setUp(self):
        """
        每条case的前提条件
        :return:
        """
        init_graph()
        code, res = GraphConnection().add_graph_connect(body={
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        })
        self.assertEqual(code, 200, "创建图链接失败")
        self.assertEqual(res['status'], 200, "创建图链接失败")

    def tearDown(self):
        """
        测试case结束
        :param self:
        :return:
        """
        pass

    def test_execute_gremlin_task(self):
        """
        执行Gremlin任务
        """
        graph_id = ID.get_graph_id()
        body = {"content": "g.V().count()"}
        Gremlin.gremlin_task(body=body, graph_id=graph_id)
        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看异步任务状态码不正确")
        self.assertEqual(res['data']['records'][0]['task_name'], body["content"], "非gremlin异步任务或者异步任务内容有误")
        self.assertEqual(res['data']['records'][0]['task_type'], "gremlin", "非gremlin异步任务或者异步任务执行失败")

    def test_deleteVertexLabel(self):
        """
        删除顶点类型
        """
        graph_id = ID.get_graph_id()
        body = {"name": "string", "data_type": "TEXT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {
            "name": "vertexLabel",
            "id_strategy": "PRIMARY_KEY",
            "properties": [{"name": "string", "nullable": False}],
            "primary_keys": ["string"],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "创建顶点类型失败")

        code, res = Schema.delete_vertexLabel(param="names=vertexLabel&skip_using=false", graph_id=graph_id)
        self.assertEqual(code, 200, "删除顶点类型失败")

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看删除元数据任务状态码不正确")
        self.assertEqual(res['data']['records'][0]['task_name'], "VERTEX_LABEL:1:vertexLabel", "删除元数据任务内容有误")
        self.assertEqual(res['data']['records'][0]['task_type'], "remove_schema", "删除元数据任务执行失败")

    def test_deleteEdgeLabel(self):
        """
        删除边类型
        """
        graph_id = ID.get_graph_id()
        body = {"name": "string", "data_type": "TEXT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {
            "name": "vertexLabel",
            "id_strategy": "PRIMARY_KEY",
            "properties": [{"name": "string", "nullable": False}],
            "primary_keys": ["string"],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "创建顶点类型失败")

        body = {
            "name": "link",
            "source_label": "vertexLabel",
            "target_label": "vertexLabel",
            "link_multi_times": False,
            "properties": [],
            "sort_keys": [],
            "property_indexes": [],
            "open_label_index": False,
            "style": {
                "color": "#112233",
                "with_arrow": True,
                "thickness": "FINE",
                "display_fields": [
                    "~id"
                ],
                "join_symbols": [
                    "-"
                ]
            }
        }
        code, res = Schema.create_edgeLabel(body, graph_id)
        self.assertEqual(code, 200, "创建边类型失败")

        # code, res = Schema.delete_edgeLabel(param={"names": "link", "skip_using": False}, graph_id=graph_id)
        code, res = Schema.delete_edgeLabel(param="names=link&skip_using=false", graph_id=graph_id)
        self.assertEqual(code, 200, "删除边类型失败")

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看删除元数据任务状态码不正确")
        self.assertEqual(res['data']['records'][0]['task_name'], "EDGE_LABEL:1:link", "删除元数据任务内容有误")
        self.assertEqual(res['data']['records'][0]['task_type'], "remove_schema", "删除元数据任务执行失败")

    def test_createIndexLabel(self):
        """
        创建索引
        """
        graph_id = ID.get_graph_id()
        body = {"name": "string", "data_type": "TEXT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {"name": "int", "data_type": "INT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {
            "name": "vertexLabel",
            "id_strategy": "PRIMARY_KEY",
            "properties": [
                {"name": "string", "nullable": False},
                {"name": "int", "nullable": True}
            ],
            "primary_keys": ["string"],
            "property_indexes": [{"name": "intBySecondary", "type": "SECONDARY", "fields": ["int"]}],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "创建带索引的顶点类型失败")
        self.assertEqual(res['status'], 200, "创建顶点类型索引失败")

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看异步任务状态码不正确")
        self.assertEqual(res['data']['records'][0]['task_name'], "INDEX_LABEL:1:intBySecondary", "创建索引内容有误")
        self.assertEqual(res['data']['records'][0]['task_type'], "rebuild_index", "创建索引异步任务执行失败")

    def test_rebuildIndexLabel(self):
        """
        重建索引
        """
        graph_id = ID.get_graph_id()

        body = {"name": "string", "data_type": "TEXT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {"name": "int", "data_type": "INT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {
            "name": "vertexLabel",
            "id_strategy": "PRIMARY_KEY",
            "properties": [
                {"name": "string", "nullable": False},
                {"name": "int", "nullable": True}
            ],
            "primary_keys": ["string"],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "创建顶点类型失败")
        self.assertEqual(res['status'], 200, "创建顶点类型失败")

        body = {
            "append_properties": [],
            "append_property_indexes": [{"name": "re_index", "type": "SECONDARY", "fields": ["int"]}],
            "remove_property_indexes": [],
        }
        code, res = Schema.create_vertexLabelIndexLabel(body, graph_id, name="vertexLabel")
        self.assertEqual(code, 200, "重建顶点类型索引失败")
        self.assertEqual(res['status'], 200, "重建顶点类型索引失败")

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看异步任务状态码不正确")
        self.assertEqual(res['data']['records'][0]['task_name'], "INDEX_LABEL:1:re_index", "重建建索引内容有误")
        self.assertEqual(res['data']['records'][0]['task_type'], "rebuild_index", "重建索引异步任务执行失败")

    def test_deleteIndexLabel(self):
        """
        删除索引
        """
        graph_id = ID.get_graph_id()
        body = {"name": "string", "data_type": "TEXT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {"name": "int", "data_type": "INT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {
            "name": "vertexLabel",
            "id_strategy": "PRIMARY_KEY",
            "properties": [
                {"name": "string", "nullable": False},
                {"name": "int", "nullable": True}
            ],
            "primary_keys": ["string"],
            "property_indexes": [{"name": "intBySecondary", "type": "SECONDARY", "fields": ["int"]}],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "创建带索引的顶点类型失败")
        self.assertEqual(res['status'], 200, "创建带索引的顶点类型失败")

        body = {
            "append_properties": [],
            "append_property_indexes": [],
            "remove_property_indexes": ["intBySecondary"],
            "style":
                {"color": "#5c73e6",
                 "icon": None,
                 "size": "NORMAL",
                 "display_fields": ["~id"]
                 }
        }
        code, res = Schema.delete_vertexLabelIndexLabel(name="vertexLabel", graph_id=graph_id, body=body)
        self.assertEqual(code, 200, "创建带索引的顶点类型失败")

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看异步任务状态码不正确")
        self.assertEqual(res['data']['records'][0]['task_name'], "INDEX_LABEL:1:intBySecondary", "创建索引内容有误")
        self.assertEqual(res['data']['records'][0]['task_type'], "remove_schema", "创建索引异步任务执行失败")

    # @pytest.mark.ifskip(_cfg.graph_type == "open_source", reason="当前版本不支持")
    # def test_alg(self):
    #     """
    #     算法任务
    #     """
    #     body = {
    #         ### schema
    #         "content": "graph.schema().propertyKey('name').asText().ifNotExist().create(); "
    #                    "graph.schema().propertyKey('age').asInt().ifNotExist().create(); "
    #                    "graph.schema().propertyKey('city').asText().ifNotExist().create(); "
    #                    "graph.schema().propertyKey('lang').asText().ifNotExist().create(); "
    #                    "graph.schema().propertyKey('date').asText().ifNotExist().create(); "
    #                    "graph.schema().propertyKey('price').asInt().ifNotExist().create(); "
    #         # vertex_label
    #                    "person = graph.schema().vertexLabel('person').properties('name', 'age', 'city')"
    #                    ".primaryKeys('name').ifNotExist().create(); "
    #                    "software = graph.schema().vertexLabel('software').properties('name', 'lang', 'price')"
    #                    ".primaryKeys('name').ifNotExist().create(); "
    #         # edge_label
    #                    "knows = graph.schema().edgeLabel('knows').sourceLabel('person')"
    #                    ".targetLabel('person').properties('date').ifNotExist().create(); "
    #                    "created = graph.schema().edgeLabel('created').sourceLabel('person')"
    #                    ".targetLabel('software').properties('date', 'city').ifNotExist().create(); "
    #                    "graph.schema().edgeLabel('help').sourceLabel('software').targetLabel('person')"
    #                    ".properties('date','city').ifNotExist().create();"
    #                    "graph.schema().edgeLabel('relation').sourceLabel('software').targetLabel('software')"
    #                    ".properties('date','city').ifNotExist().create();"
    #         # vertex_dataset
    #                    "marko = graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 29, 'city', 'Beijing'); "
    #                    "vadas = graph.addVertex(T.label, 'person', 'name', 'vadas', 'age', 27, 'city', 'Hongkong'); "
    #                    "lop = graph.addVertex(T.label, 'software', 'name', 'lop', 'lang', 'java', 'price', 328); "
    #                    "josh = graph.addVertex(T.label, 'person', 'name', 'josh', 'age', 32, 'city', 'Beijing'); "
    #                    "ripple = graph.addVertex(T.label, 'software', 'name', 'ripple', 'lang', 'java', 'price', 199); "
    #                    "peter = graph.addVertex(T.label, 'person', 'name', 'peter', 'age', 29, 'city', 'Shanghai'); "
    #         # edge_dataset
    #                    "ripple.addEdge('help', marko, 'date', '20160110', 'city', 'Shenzhen');"
    #                    "lop.addEdge('relation', ripple, 'date', '20160110', 'city', 'Shenzhen');"
    #                    "marko.addEdge('created', ripple, 'date', '20160110', 'city', 'Shenzhen');"
    #                    "lop.addEdge('help', vadas, 'date', '20160110', 'city', 'Shenzhen');"
    #                    "lop.addEdge('help', josh, 'date', '20160110', 'city', 'Shenzhen');"
    #                    "josh.addEdge('created', ripple, 'date', '20160110', 'city', 'Shenzhen');"
    #                    "lop.addEdge('help', marko, 'date', '20160110', 'city', 'Shenzhen');"
    #                    "josh.addEdge('knows', marko, 'date', '20160110');"
    #                    "josh.addEdge('knows', marko, 'date', '20160110');"
    #                    "marko.addEdge('knows', vadas, 'date', '20160110');"
    #     }
    #     graph_id = ID.get_graph_id()
    #     Gremlin.gremlin_query(body=body, graph_id=graph_id)
    #     body = {"k": 2}
    #     code, res = Algorithm().post_kcore(body, auth=auth)
    #     print(code, res)
    #     id = res["task_id"]
    #     if id > 0:
    #         result = get_task_res(id, 300, auth=auth)
    #         print(result)
    #         self.assertEqual(result, {'kcores': [
    #             ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop'],
    #             ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]
    #         }, "算法结果不正确")
    #     else:
    #         assert 0
    #
    #     code, res = Task.view_async_tasks_all(graph_id=graph_id)
    #     print(code, res)
    #     self.assertEqual(code, 200, "响应状态码不正确")
    #     self.assertEqual(res['status'], 200, "查看异步任务状态码不正确")
    #     # self.assertEqual(res['data']['records'][0]['task_name'], body["content"], "算法执行内容有误")
    #     self.assertEqual(res['data']['records'][0]['task_type'], "algorithm", "算法任务执行失败")

    def test_delete_task(self):
        """
        删除单个异步任务
        """
        graph_id = ID.get_graph_id()
        body = {"content": "g.V().count()"}
        Gremlin.gremlin_task(body=body, graph_id=graph_id)

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "异步任务创建失败")

        param = "ids=1"
        code, res = Task.delete_async_task(graph_id=graph_id, param=param)
        print(code, res)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除单个异步任务失败")

    def test_delete_tasks(self):
        """
        批量删除异步任务
        """
        graph_id = ID.get_graph_id()
        body = {"content": "g.V().count()"}
        Gremlin.gremlin_task(body=body, graph_id=graph_id)
        Gremlin.gremlin_task(body=body, graph_id=graph_id)

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "异步任务创建失败")
        self.assertEqual(len(res['data']['records']), 2, "非2个异步任务")

        param = "?ids=1&ids=2"
        code, res = Task.delete_async_task(graph_id=graph_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "批量删除异步任务失败")

    def test_get_result(self):
        """
        查看异步任务结果
        """
        graph_id = ID.get_graph_id()
        body = {"content": "g.V().count()"}
        Gremlin.gremlin_task(body=body, graph_id=graph_id)

        code, res = Task.view_async_tasks_all(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看异步任务状态码不正确")

        async_task_id = res['data']['records'][0]['id']
        code, res = Task.view_async_task_result(graph_id=graph_id, async_task_id=async_task_id)
        time.sleep(1)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看异步任务状态码不正确")
        self.assertEqual(res['data']['task_status'], "success", "异步任务状态失败")
        self.assertEqual(res['data']['task_result'], '[0]', "异步任务结果不正确")


if __name__ == '__main__':
    unittest.main()

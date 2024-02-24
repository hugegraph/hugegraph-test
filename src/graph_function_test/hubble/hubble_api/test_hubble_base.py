# -*- coding: UTF-8 -*-
"""
Created by v_changshuai01 at 2021/5/18
"""
import os
import sys
import unittest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg
from src.common.hubble_api import GraphConnection
from src.common.hubble_api import Schema
from src.common.server_api import Gremlin
from src.common.hubble_api import Collection
from src.common.tools import clear_graph


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
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用gremlin语句进行truncate操作
        # delete graph_connection
        code, res = GraphConnection().delete_graph_connect(each_id)
        assert code == 200


class TestBase(unittest.TestCase):
    """
    hubble的一些基础模块API
    """

    def setUp(self):
        """
        每条case的前提条件
        :return:
        """
        init_graph()

    def tearDown(self):
        """
        测试case结束
        :param self:
        :resurn:
        """
        pass

    def test_add_graph_connect(self):
        """
        添加图链接
        """
        body = {
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }

        if _cfg.is_auth:
            body['username'] = 'admin'
            body['password'] = _cfg.admin_password.get('admin')
        code, res = GraphConnection().add_graph_connect(body=body)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加图链接状态码不正确")
        self.assertEqual(res['data']['name'], body['name'], "图id有误")
        self.assertEqual(res['data']['graph'], body['graph'], "图名称有误")
        self.assertEqual(res['data']['host'], body['host'], "图主机名有误")
        self.assertEqual(res['data']['port'], body['port'], "图端口号有误")

    def test_updateGraphConnect_updateGraphId(self):
        """
        修改图链接,修改图id
        """
        self.test_add_graph_connect()
        body = {
            "name": _cfg.graph_name + "_update1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }
        if _cfg.is_auth:
            body['username'] = 'admin'
            body['password'] = _cfg.admin_password.get('admin')
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = GraphConnection().update_graph_connect(body=body, graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加图链接状态码不正确")
        self.assertEqual(res['data']['name'], body['name'], "图id有误")
        self.assertEqual(res['data']['graph'], body['graph'], "图名称有误")
        self.assertEqual(res['data']['host'], body['host'], "图主机名有误")
        self.assertEqual(res['data']['port'], body['port'], "图端口号有误")

    def test_updateGraphConnect_updateGraphName(self):
        """
        修改图链接,修改图名称
        """
        self.test_add_graph_connect()
        body = {
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = GraphConnection().update_graph_connect(body=body, graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加图链接状态码不正确")
        self.assertEqual(res['data']['name'], body['name'], "图id有误")
        self.assertEqual(res['data']['graph'], body['graph'], "图名称有误")
        self.assertEqual(res['data']['host'], body['host'], "图主机名有误")
        self.assertEqual(res['data']['port'], body['port'], "图端口号有误")

    def test_updateGraphConnect_updateHostName(self):
        """
        修改图链接,修改主机名
        """
        self.test_add_graph_connect()
        body = {
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }
        if _cfg.is_auth:
            body['username'] = 'admin'
            body['password'] = _cfg.admin_password.get('admin')
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = GraphConnection().update_graph_connect(body=body, graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加图链接状态码不正确")
        self.assertEqual(res['data']['name'], body['name'], "图id有误")
        self.assertEqual(res['data']['graph'], body['graph'], "图名称有误")
        self.assertEqual(res['data']['host'], body['host'], "图主机名有误")
        self.assertEqual(res['data']['port'], body['port'], "图端口号有误")

    def test_updateGraphConnect_updatePort(self):
        """
        修改图链接,修改端口号
        """
        self.test_add_graph_connect()
        body = {
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }
        if _cfg.is_auth:
            body['username'] = 'admin'
            body['password'] = _cfg.admin_password.get('admin')
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = GraphConnection().update_graph_connect(body=body, graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加图链接状态码不正确")
        self.assertEqual(res['data']['name'], body['name'], "图id有误")
        self.assertEqual(res['data']['graph'], body['graph'], "图名称有误")
        self.assertEqual(res['data']['host'], body['host'], "图主机名有误")
        self.assertEqual(res['data']['port'], body['port'], "图端口号有误")

    def test_addProperty_textSingle(self):
        """
        添加属性,数据类型为TEXT,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "string1", "data_type": "TEXT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_textList(self):
        """
        添加属性,数据类型为TEXT,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "string2", "data_type": "TEXT", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_textSet(self):
        """
        添加属性,数据类型为TEXT,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "string3", "data_type": "TEXT", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_intSingle(self):
        """
        添加属性,数据类型为INT,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "int1", "data_type": "INT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_intList(self):
        """
        添加属性,数据类型为INT,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "int2", "data_type": "INT", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_intSet(self):
        """
        添加属性,数据类型为INT,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "int3", "data_type": "INT", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_booleanSingle(self):
        """
        添加属性,数据类型为BOOLEAN,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "boolean1", "data_type": "BOOLEAN", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_booleanList(self):
        """
        添加属性,数据类型为BOOLEAN,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "boolean2", "data_type": "BOOLEAN", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_booleanSet(self):
        """
        添加属性,数据类型为BOOLEAN,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "boolean3", "data_type": "BOOLEAN", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_byteSingle(self):
        """
        添加属性,数据类型为BYTE,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "byte1", "data_type": "BYTE", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_byteList(self):
        """
        添加属性,数据类型为BYTE,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "byte2", "data_type": "BYTE", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_byteSet(self):
        """
        添加属性,数据类型为BYTE,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "byte3", "data_type": "BYTE", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_longSingle(self):
        """
        添加属性,数据类型为LONG,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "long1", "data_type": "LONG", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_longList(self):
        """
        添加属性,数据类型为LONG,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "long2", "data_type": "LONG", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_longSet(self):
        """
        添加属性,数据类型为LONG,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "long3", "data_type": "LONG", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_floatSingle(self):
        """
        添加属性,数据类型为FLOAT,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "float1", "data_type": "FLOAT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_floatList(self):
        """
        添加属性,数据类型为FLOAT,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "float2", "data_type": "FLOAT", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_floatSet(self):
        """
        添加属性,数据类型为FLOAT,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "float3", "data_type": "FLOAT", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_doubleSingle(self):
        """
        添加属性,数据类型为DOUBLE,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "double1", "data_type": "DOUBLE", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_doubleList(self):
        """
        添加属性,数据类型为DOUBLE,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "double2", "data_type": "DOUBLE", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_doubleSet(self):
        """
        添加属性,数据类型为DOUBLE,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "double3", "data_type": "DOUBLE", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_uuidSingle(self):
        """
        添加属性,数据类型为UUID,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "uuid1", "data_type": "UUID", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_uuidList(self):
        """
        添加属性,数据类型为UUID,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "uuid2", "data_type": "UUID", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_uuidSet(self):
        """
        添加属性,数据类型为UUID,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "uuid3", "data_type": "UUID", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_dateSingle(self):
        """
        添加属性,数据类型为DATE,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "date1", "data_type": "DATE", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_dateList(self):
        """
        添加属性,数据类型为DATE,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "date2", "data_type": "DATE", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_dateSet(self):
        """
        添加属性,数据类型为DATE,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "date3", "data_type": "DATE", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_blobSingle(self):
        """
        添加属性,数据类型为BLOB,基数为single
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "blob1", "data_type": "BLOB", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_blobList(self):
        """
        添加属性,数据类型为BLOB,基数为list
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "blob2", "data_type": "BLOB", "cardinality": "LIST"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_addProperty_blobSet(self):
        """
        添加属性,数据类型为BLOB,基数为set
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "blob3", "data_type": "BLOB", "cardinality": "SET"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加属性状态码不正确")

    def test_queryProperty(self):
        """
        查看属性
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = Schema.get_property(graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查看属性状态码不正确")
        self.assertEqual(res['data']["records"][0]["name"], "string1", "查看属性名称不正确")
        self.assertEqual(res['data']["records"][0]["data_type"], "TEXT", "查看属性类型不正确")
        self.assertEqual(res['data']["records"][0]["cardinality"], "SINGLE", "查看属性基数不正确")

    def test_deleteProperty(self):
        """
        删除属性
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = Schema.delete_property(param="names=string1&skip_using=false", graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除属性状态码不正确")

    def test_addVertexLabel_AUTOMATIC(self):
        """
        添加顶点类型,ID策略（自动生成）
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "vertexLabel1",
            "id_strategy": "AUTOMATIC",
            "properties": [{"name": "string1", "nullable": False}],
            "primary_keys": [],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加顶点类型状态码不正确")

    def test_addVertexLabel_CUSTOMIZESTRING(self):
        """
        添加顶点类型,ID策略（自定义字符串）
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "vertexLabel1",
            "id_strategy": "CUSTOMIZE_STRING",
            "properties": [{"name": "string1", "nullable": False}],
            "primary_keys": [],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加顶点类型状态码不正确")

    def test_addVertexLabel_CUSTOMIZENUMBER(self):
        """
        添加顶点类型,ID策略（自定义数字）
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "vertexLabel1",
            "id_strategy": "CUSTOMIZE_NUMBER",
            "properties": [{"name": "string1", "nullable": False}],
            "primary_keys": [],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加顶点类型状态码不正确")

    def test_addVertexLabel_CUSTOMIZEUUID(self):
        """
        添加顶点类型,ID策略（自定义uuid）
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "vertexLabel1",
            "id_strategy": "CUSTOMIZE_UUID",
            "properties": [{"name": "string1", "nullable": False}],
            "primary_keys": [],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加顶点类型状态码不正确")

    def test_addVertexLabel_PRIMARYKEY(self):
        """
        添加顶点类型,ID策略（主键）
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "vertexLabel1",
            "id_strategy": "PRIMARY_KEY",
            "properties": [{"name": "string1", "nullable": False}],
            "primary_keys": ["string1"],
            "property_indexes": [],
            "open_label_index": False,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加顶点类型状态码不正确")

    def test_addVertexLabel_PRIMARYKEY_labelIndexNotNull(self):
        """
        添加顶点类型,ID策略（主键）,类型索引不为空,主键属性不为空
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "vertexLabel1",
            "id_strategy": "PRIMARY_KEY",
            "properties": [{"name": "string1", "nullable": False}],
            "primary_keys": ["string1"],
            "property_indexes": [],
            "open_label_index": True,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加顶点类型状态码不正确")

    def test_addVertexLabel_PRIMARYKEY_labelIndexNotNull_PRIMARYKEYPropertyNull(self):
        """
        异常case，添加顶点类型,ID策略（主键）,类型索引不为空,主键属性为空
        """
        self.test_addProperty_textSingle()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "vertexLabel1",
            "id_strategy": "PRIMARY_KEY",
            "properties": [{"name": "string1", "nullable": False}],
            "primary_keys": [],
            "property_indexes": [],
            "open_label_index": True,
            "style":
                {
                    "color": "#569380",
                    "icon": None
                }
        }
        code, res = Schema.create_vertexLabel(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 400, "添加顶点类型状态码不正确")
        self.assertEqual(res['message'], "The primary keys of vertex label vertexLabel1 cant be null or empty",
                         "message信息提示错误")

    def test_queryVertexLabel(self):
        """
        查看顶点类型
        """
        self.test_addVertexLabel_PRIMARYKEY()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = Schema.get_vertexLabel(graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查询顶点类型状态码不正确")
        self.assertEqual(res['data']["records"][0]["name"], "vertexLabel1", "查询顶点类型结果不正确")

    def test_deleteVertexLabel(self):
        """
        删除顶点类型
        """
        self.test_addVertexLabel_PRIMARYKEY()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = Schema.delete_vertexLabel(param="names=vertexLabel1&skip_using=false", graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除顶点类型状态码不正确")

    def test_addEdgeLabel(self):
        """
        添加边类型
        """
        self.test_addVertexLabel_PRIMARYKEY()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "name": "link1",
            "source_label": "vertexLabel1",
            "target_label": "vertexLabel1",
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
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加边类型状态码不正确")

    def test_queryEdgeLabel(self):
        """
        查看边类型
        """
        self.test_addEdgeLabel()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = Schema.get_edgeLabel(graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查询边类型状态码不正确")
        self.assertEqual(res['data']["records"][0]["name"], "link1", "查询边类型结果不正确")

    def test_deleteEdgeLabel(self):
        """
        删除边类型
        """
        self.test_addEdgeLabel()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        code, res = Schema.delete_edgeLabel(param="names=link1&skip_using=false", graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除边类型状态码不正确")

    def test_addIndexLabel_vertexLabel(self):
        """
        创建顶点类型添加索引
        """
        body = {
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }
        if _cfg.is_auth:
            body['username'] = 'admin'
            body['password'] = _cfg.admin_password.get('admin')
        code, res = GraphConnection().add_graph_connect(body=body)
        self.assertEqual(code, 200, "添加图链接成功")

        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']

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
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加顶点类型及索引状态码不正确")

    def test_addIndexLabel_edgeLabel(self):
        """
        创建边类型添加索引
        """
        body = {
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }
        if _cfg.is_auth:
            body['username'] = 'admin'
            body['password'] = _cfg.admin_password.get('admin')
        code, res = GraphConnection().add_graph_connect(body=body)
        self.assertEqual(code, 200, "添加图链接失败")

        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']

        body = {"name": "string", "data_type": "TEXT", "cardinality": "SINGLE"}
        code, res = Schema.create_property(body, graph_id)
        self.assertEqual(code, 200, "创建属性失败")

        body = {
            "name": "vertexLabel",
            "id_strategy": "PRIMARY_KEY",
            "properties": [
                {"name": "string", "nullable": False}
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
        self.assertEqual(code, 200, "添加顶点类型失败")

        body = {
            "name": "link",
            "source_label": "vertexLabel",
            "target_label": "vertexLabel",
            "link_multi_times": False,
            "properties": [
                {"name": "string", "nullable": False}
            ],
            "sort_keys": [],
            "property_indexes": [
                {"name": "strBySecondary", "type": "SECONDARY", "fields": ["string"]}],
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
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加边类型及索引状态码不正确")

    def test_queryVertexLabelIndexLabel(self):
        """
        查看顶点类型属性索引
        """
        self.test_addIndexLabel_vertexLabel()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        param = "page_no=1&page_size=10&is_vertex_label=true"
        code, res = Schema.get_PropertyIndex(graph_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查询边类型状态码不正确")
        self.assertEqual(res['data']["records"][0]["name"], "intBySecondary", "查询顶点类型属性索引不正确")

    def test_queryEdgeLabelIndexLabel(self):
        """
        查看边类型属性索引
        """
        self.test_addIndexLabel_edgeLabel()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        param = "page_no=1&page_size=10&is_vertex_label=false"
        code, res = Schema.get_PropertyIndex(graph_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查询边类型状态码不正确")
        self.assertEqual(res['data']["records"][0]["name"], "strBySecondary", "查询边类型属性索引不正确")

    def test_deleteVertexLabelIndexLabel(self):
        """
        删除顶点类型索引
        """
        self.test_addIndexLabel_vertexLabel()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "append_properties": [],
            "append_property_indexes": [],
            "remove_property_indexes": ["intBySecondary"],
            "style": {
                "color": "#5c73e6",
                "icon": None,
                "size": "NORMAL",
                "display_fields": ["~id"]
            }}
        code, res = Schema.delete_vertexLabelIndexLabel(name="vertexLabel", graph_id=graph_id, body=body)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除顶点类型索引状态码不正确")

    def test_deleteEdgeLabelIndexLabel(self):
        """
        删除边类型索引
        """
        self.test_addIndexLabel_edgeLabel()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {
            "append_properties": [],
            "append_property_indexes": [],
            "remove_property_indexes": ["strBySecondary"],
            "style": {
                "color": "#5c73e6",
                "icon": None,
                "with_arrow": True,
                "thickness": "NORMAL",
                "display_fields": ["~id"]
            }}
        code, res = Schema.delete_edgeLabelIndexLabel(name="link", graph_id=graph_id, body=body)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除边类型状态码不正确")

    def test_addCollectionStatement(self):
        """
        添加收藏语句
        """
        self.test_add_graph_connect()
        code, res = GraphConnection().get_graph_connect()
        graph_id = res['data']['records'][0]['id']
        body = {"name": "collection1", "content": "g.V()"}
        code, res = Collection.collect_query_statement(body, graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "添加收藏语句状态码不正确")


if __name__ == '__main__':
    unittest.main()

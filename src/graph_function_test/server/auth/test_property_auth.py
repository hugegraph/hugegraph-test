# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 细粒度权限的鉴权和越权
create_time: 2021/3/1 11:17 上午
"""
import unittest
import os

import pytest
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Gremlin
from src.common.server_api import Auth
from src.common.server_api import Vertex
from src.common.server_api import Edge
from src.common.server_api import Task
from src.common.server_api import Schema
from src.common.loader import InsertData
from src.common import set_auth
from src.config import basic_config as _cfg

auth = None
user = None
if _cfg.is_auth:
    auth = _cfg.admin_password
    user = _cfg.test_password


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class TestDetailAuth(unittest.TestCase):
    """
    细粒度权限验证：创建用户并对用户进行鉴权和越权验证
    """

    def setUp(self):
        """
        每条case的前提条件
        :return:
        """
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)

    def test_vertex_pro_single_string_read(self):
        """
        basic_operatiion 读单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "vertex_read"},
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res["roles"][_cfg.graph_name].items():
            self.assertEqual(key, 'READ', msg='role permission check fail')
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print("验权--读", code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 29
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print("越权--写", code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print("越权--删", code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_string_read_noread_nowrite_nodelete(self):
        """
        basic_operatiion 读单个限制string属性权限
        不加read权限去读,不加write权限去写,不加delete权限去删
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"}],
             "permission": "READ",
             "name": "vertex_read"},
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 29
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_string_write(self):
        """
        basic_operatiion 写单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [
                {"type": "PROPERTY_KEY"},
                {"type": "VERTEX_LABEL"}
            ], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
                "permission": "WRITE", "name": "vertex_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 45,
                "city": "Shanghai"
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_string_delete(self):
        """
        basic_operatiion 删除单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}
                             ], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX_LABEL", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        vertex_id = '\"1:r\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print("验权--删", code, res)
        self.assertEqual(code, 204, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print("越权--读", code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 29
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print("越权--写", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_string_delete_notRead(self):
        """
        basic_operatiion 删除单个限制string属性权限
        不加读的权限，不可以删除
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "Shanghai"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX_LABEL", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        vertex_id = '\"1:r\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print("验权--删", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "Permission denied: read Resource{graph=hugegraph,type=VERTEX,"
                                         "operated=v[1:r]}", msg="Unauthorized result check fail")
        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print("越权--读", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 29
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print("越权--写", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_int_read(self):
        """
        basic_operatiion 读单个限制int属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person", "properties": {"age": "P.gte(30)"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, "READ", msg="role permission check fail")
            self.assertEqual(value[2]["type"], "VERTEX", msg="role type check fail")

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print("验权--读", code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 45
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print("越权--写", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print("越权--删", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_int_write(self):
        """
        basic_operatiion 写单个限制int属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"}
                             ], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"age": "P.gte(30)"}}],
             "permission": "WRITE", "name": "vertex_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 45,
                "city": "Shanghai"
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print("验权--写", code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print("越权--读", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print("越权--删", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_single_int_delete(self):
        """
        basic_operatiion 删除单个限制int属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"age": "P.gte(30)"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                  # 删除的时候报没有这个顶点的ID
        vertex_id = '\"1:h\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 56
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_list_string_read(self):
        """
        basic_operatiion 读单个限制list属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_list_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 46,
                "city": ["Shanxi", "qwe"]
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:peter\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_list_string_write(self):
        """
        string属性基数为list，vertex写权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_list_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"}
                             ], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
             "permission": "WRITE", "name": "vertex_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 46,
                "city": ["Shanxi", "qwe"]
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_pro_list_string_delete(self):
        """
        string属性基数为list，vertex删除权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_list_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        vertex_id = '\"1:peter\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 56,
                "city": ["Shanxi", "qwe"]
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_read_Multiple(self):
        """
        basic_operatiion 读多个限制属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi", "age": "P.gte(20)"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 45
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_write_Multiple(self):
        """
        basic_operatiion 写多个限制属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"}
                             ], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi", "age": "P.gte(20)"}}],
             "permission": "WRITE", "name": "vertex_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 20,
                "city": "Shanxi"
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_delete_Multiple(self):
        """
        basic_operatiion 删除多个限制属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "VERTEX", "label": "person",
                 "properties": {"city": "Shanghai", "age": "P.gte(20)"}}],
                "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        vertex_id = '\"1:peter\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 56,
                "city": ["Shanxi", "qwe"]
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_read_Multiple_different_targets(self):
        """
        basic_operatiion 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}], "permission": "READ",
             "name": "property_read"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi"}}],
             "permission": "READ",
             "name": "vertex_read_city"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"age": "P.gte(20)"}}],
             "permission": "READ",
             "name": "vertex_read_age"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[2]["type"], "VERTEX_LABEL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 45
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertNotEqual(code, 201, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertNotEqual(code, 201, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_write_Multiple_different_targets(self):
        """
        basic_operatiion 写多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"}
                             ], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"city": "Shanxi"}}],
             "permission": "WRITE", "name": "vertex_write_city"},
            {"target_list": [{"type": "VERTEX", "label": "person",
                              "properties": {"age": "P.gte(20)"}}],
             "permission": "WRITE", "name": "vertex_write_age"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "new1",
                "age": 20,
                "city": "Shanxi"
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        vertex_id = '\"1:alg\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_vertex_delete_Multiple_different_targets(self):
        """
        basic_operatiion 删除多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "VERTEX", "label": "person",
                 "properties": {"city": "Beijing"}}],
                "permission": "DELETE", "name": "vertex_delete_city"},
            {"target_list": [
                {"type": "VERTEX", "label": "person",
                 "properties": {"age": "P.gte(20)"}}],
                "permission": "DELETE", "name": "vertex_delete_age"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        vertex_id = '\"1:peter\"'
        code, res = Vertex().delete_vertex(vertex_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg=res)

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "person",
            "properties": {
                "name": "alg",
                "age": 56,
                "city": ["Shanxi", "qwe"]
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_read(self):
        """
        edge 读单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:peter>2>2>>S2:lop"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_read_nogremlin(self):
        """
        edge 读单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:peter>2>2>>S2:lop"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_read_noread(self):
        """
        edge 读单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        edge_id = "S1:peter>2>2>>S2:lop"
        code, res = Edge().get_edge_by_id(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:peter>2>2>>S2:lop"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_write(self):
        """
        edge 写单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}
                             ], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "WRITE", "name": "edge_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:zhao",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "city": "Shanghai",
                "date": "2017-5-18"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print("验权-->写", code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print("越权-->读", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:peter>2>>S2:lop"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print("越权-->删", code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_string_delete(self):
        """
        edge 删除单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"},
                             {"type": "EDGE"}
                             ], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "created", "properties": {"city": "Beijing"}}],
             "permission": "DELETE", "name": "edge_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
                self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:peter>2>2>>S2:lop"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Beijing"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_int_read(self):
        """
        edge 读单个限制int属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "knows", "properties": {"price": "P.gte(200)"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "price": 234
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:li>1>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_int_write(self):
        """
        edge 写单个限制int属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows", "properties": {"price": "P.gte(200)"}}],
             "permission": "WRITE", "name": "edge_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            # print key,value
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "price": 234
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:peter>2>2>>S2:lop"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_single_int_delete(self):
        """
        edge 删除单个限制int属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"},
                             {"type": "EDGE"}
                             ], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows", "properties": {"price": "P.gte(200)"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
                self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:marko>1>1>>S1:josh"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "price": 234
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_list_string_read(self):
        """
        edge 读单个限制list属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_list_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "knows",
                              "properties": {"address": "P.contains(\"北京市海淀区\")"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "address": "北京市海淀区"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:li>1>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_list_string_write(self):
        """
        edge 写单个限制list属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_list_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "EDGE", "label": "knows", "properties": {"address": "P.contains(\"北京市海淀区\")"}}],
             "permission": "WRITE", "name": "edge_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "address": "北京市海淀区"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:alg>1>1>>S1:vadas"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_list_string_delete(self):
        """
        edge 删除单个限制list属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_list_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "EDGE", "label": "knows", "properties": {"address": "P.contains(\"北京市海淀区\")"}}],
             "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")  # 删除边需要读边的权限（应该不用读的）
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:li>1>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "2017-5-18",
                "address": "北京市海淀区"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_read_Multiple(self):
        """
        edge 读多个限制属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110", "price": "P.gte(400)"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20170518",
                "price": 567
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:li>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_write_Multiple(self):
        """
        edge 写多个限制属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}
                             ], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "EDGE", "label": "knows", "properties": {"date": "20160110", "price": "P.gte(400)"}}],
                "permission": "WRITE", "name": "vertex_write"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20160110",
                "price": 567
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:li>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_pro_delete_Multiple(self):
        """
        edge 删除多个限制属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ", "name": "vertexlabel_pro_read"},
            {"target_list": [
                {"type": "EDGE", "label": "knows", "properties": {"date": "20160110", "price": "P.gte(400)"}}],
                "permission": "DELETE", "name": "vertex_delete"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:li>1>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        # print code, res
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20170518",
                "price": 567
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_read_Multiple_different_targets(self):
        """
        EDGE 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"}],
             "permission": "READ", "name": "property_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "READ",
             "name": "edge_read_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "READ",
             "name": "edge_read_price"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[3]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[4]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20170518",
                "price": 567
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:li>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_write_Multiple_different_targets(self):
        """
        basic_operatiion 写多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "VERTEX"}], "permission": "READ",
             "name": "edgelabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "WRITE", "name": "edge_write_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "WRITE", "name": "edge_write_price"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            print(key, value)
            if key == "WRITE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[0]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[1]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[1]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "VERTEX", msg="role type check fail")
            else:
                pass

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20160110",
                "price": 567
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:li>1>>S1:wang"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_delete_Multiple_different_targets(self):
        """
        basic_operatiion 删除多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"},
                             {"type": "EDGE"}], "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "DELETE", "name": "edge_delete_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "DELETE", "name": "edge_delete_price"},
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[0]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[1]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[1]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete
        edge_id = "S1:o>1>1>>S1:s"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)
        # self.assertEqual(res['edges'], [], msg=res)

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20160110",
                "price": 567
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_edge_delete_Multiple_noread_different_targets(self):
        """
        basic_operatiion 删除多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_edge.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"}, {"type": "VERTEX_LABEL"}, {"type": "EDGE_LABEL"}],
             "permission": "READ",
             "name": "vertexlabel_pro_read"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"date": "20160110"}}],
             "permission": "DELETE", "name": "edge_delete_date"},
            {"target_list": [{"type": "EDGE", "label": "knows",
                              "properties": {"price": "P.gte(400)"}}],
             "permission": "DELETE", "name": "edge_delete_price"},
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[0]["properties"]["date"], "20160110", msg="role type check fail")
                self.assertIn(value[1]["type"], "EDGE", msg="role type check fail")
                self.assertIn(value[1]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
            else:
                pass

        # check Unauthorized--delete                                               删除定点报没有此顶点ID
        edge_id = "S1:o>1>1>>S1:s"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res['message'], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--write
        body = {
            "label": "knows",
            "outV": "1:peter",
            "inV": "1:qian",
            "outVLabel": "person",
            "inVLabel": "person",
            "properties": {
                "date": "20160110",
                "price": 567
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

    def test_root_read_different_targets(self):
        """
        EDGE 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "ALL"}], "permission": "READ", "name": "property_read"},
            {"target_list": [{"type": "ALL"}], "permission": "DELETE", "name": "root_delete"},
            {"target_list": [{"type": "ALL"}], "permission": "WRITE", "name": "root_write"},
            # {"target_list": [{"type": "ALL"}],"permission": "READ","name": "property_read"},
            # {"target_list": [{"type": "TASK"}],"permission": "DELETE","name": "delete_task"},
            {"target_list": [{"type": "GREMLIN"}, {"type": "TASK"}], "permission": "EXECUTE", "name": "gremlin"}
            # 此权限不应该添加
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
                # self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                # self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                # self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[3]["properties"]["date"], "20160110", msg="role type check fail")
                # self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[4]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
                self.assertIn(value[1]["type"], "TASK", msg="role type check fail")
            elif key == "DELETE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            elif key == "WRITE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        Edge().get_filter_edge(auth=user)
        Schema().get_vertexLabel(auth=user)
        Vertex().get_filter_vertex(auth=user)
        Schema().get_edgeLabel(auth=user)
        Auth().get_accesses(auth=user)
        Auth().get_users(auth=user)
        Auth().get_groups(auth=user)
        code, res = Schema().delete_edgeLabel(name="tree", auth=user)  # 删除边类型
        Task().get_task(res['task_id'], auth=user)
        code, res = Gremlin().gremlin_post(query="g.V()", auth=user)
        # print code, res
        self.assertEqual(code, 200, msg=res)

    def test_task_read_different_targets(self):
        """
        EDGE 读多个限制属性权限-不同的target
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "TASK"}], "permission": "READ", "name": "task_read"},
            {"target_list": [{"type": "TASK"}], "permission": "EXECUTE", "name": "task_e"},
            # {"target_list": [{"type": "ALL"}], "permission": "DELETE", "name": "root_delete"},
            {"target_list": [{"type": "TASK"}], "permission": "WRITE", "name": "root_write"},
            # # {"target_list": [{"type": "ALL"}],"permission": "READ","name": "property_read"},
            # # {"target_list": [{"type": "TASK"}],"permission": "DELETE","name": "delete_task"},
            {"target_list": [{"type": "GREMLIN"}, {"type": "TASK"}], "permission": "EXECUTE", "name": "gremlin"}
            # 此权限不应该添加
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
                # self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                # self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                # self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[3]["properties"]["date"], "20160110", msg="role type check fail")
                # self.assertIn(value[4]["type"], "EDGE", msg="role type check fail")
                # self.assertIn(value[4]["properties"]["price"], "P.gte(400)", msg="role type check fail")
            elif key == "EXECUTE":
                # self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            elif key == "DELETE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "ALL", msg="role type check fail")
            elif key == "WRITE":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        query = "g.V('1:alg')"
        code, res = Gremlin().gremlin_job(query, auth=user)
        code, res = Task().get_task(res['task_id'], auth=user)
        print(code, res)
        # print code, res
        self.assertEqual(code, 200, msg=res)
        # # check Unauthorized--write
        # body = {
        #     "label": "knows",
        #     "outV": "1:peter",
        #     "inV": "1:qian",
        #     "outVLabel": "person",
        #     "inVLabel": "person",
        #     "properties": {
        #         "date": "20170518",
        #         "price": 567
        #     }
        # }
        # code, res = Edge().create_single_edge(body, auth=user)
        # self.assertNotEqual(code, 201, msg=res)
        # self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")
        #
        #
        # # check Unauthorized--delete
        # edge_id = "S1:li>1>>S1:wang"
        # code, res = Edge().delete_edge(edge_id, auth=user)
        # self.assertNotEqual(code, 204, msg=res)
        # self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")
        #

    def test_edge_gremlin_exe(self):
        """
        edge 用g.V()读单个限制string属性权限
        :return:
        """
        # add graph
        InsertData(gremlin='auth_single_pro.txt').gremlin_graph()

        # check role
        permission_list = [
            {"target_list": [{"type": "PROPERTY_KEY"},
                             {"type": "VERTEX_LABEL"},
                             {"type": "EDGE_LABEL"},
                             {"type": "EDGE", "label": "created", "properties": {"city": "Shanghai"}}],
             "permission": "READ",
             "name": "edge_read"},
            {"target_list": [{"type": "GREMLIN"}], "permission": "EXECUTE", "name": "gremlin"}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                self.assertIn(value[0]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[1]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[2]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE", msg="role type check fail")
            elif key == "EXECUTE":
                self.assertIn(value[0]["type"], "GREMLIN", msg="role type check fail")
            else:
                pass

        # check Authorize--read
        code, res = Gremlin().gremlin_post(query="g.E()", auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg=res)

        # check Unauthorized--write
        body = {
            "label": "created",
            "outV": "1:peter",
            "inV": "2:lop",
            "outVLabel": "person",
            "inVLabel": "software",
            "properties": {
                "date": "2017-5-18",
                "city": "Shanghai"
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:peter>2>>S2:lop"
        code, res = Edge().delete_edge(edge_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")


if __name__ == '__main__':
    pass

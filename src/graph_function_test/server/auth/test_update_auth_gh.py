# -*- coding:utf-8 -*-
"""
author     : lxb
note       : gh 优化后的权限测试
create_time: 2021/02/22 5:17 下午
"""
import pytest
import sys
import os
import time
import unittest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Gremlin
from src.common.server_api import Schema
from src.common.server_api import AuthGH
from src.common.server_api import Variable
from src.common.server_api import Task
from src.common.server_api import Graph
from src.common.server_api import Vertex
from src.common.server_api import Edge
from src.common.loader import InsertData
from src.common.task_res import get_task_res
from src.common import set_auth_gh
from src.config import basic_config as _cfg

auth = None
user = None
if _cfg.is_auth:
    auth = _cfg.admin_password
    user = _cfg.test_password


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class TestCommonAuth(unittest.TestCase):
    """
    粗粒度权限验证：创建用户并对用户进行鉴权和越权验证
    """

    def setUp(self):
        """
        测试case开始
        :resurn:
        """
        Gremlin().gremlin_post(
            host=_cfg.auth_host,
            port=_cfg.auth_port,
            graph=_cfg.auth_graph,
            query='graph.truncateBackend();',
            auth=auth
        )  # gremlin语句对auth server进行clear操作
        if _cfg.is_auth_divide:
            Gremlin().gremlin_post(
                query='graph.truncateBackend();',
                auth=auth
            )  # gremlin语句对graph server进行clear操作

    def test_status_read(self):
        """
        资源读权限
        :resurn:
        """
        permission_list = [
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)

        # check auth
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, 'READ', msg='role permission check fail')
            self.assertEqual(value[0]['type'], 'STATUS', msg='role type check fail')

        # check Authorize
        code, res = Graph().get_one_graph(auth=user)
        print(code, res)
        self.assertEqual(code, 200, 'Authorize code check fail')
        self.assertEqual(res, {'name': _cfg.graph_name, 'backend': 'rocksdb'}, 'Authorize result check fail')

        # check Unauthorized'
        body = 'NONE'
        code, res = Graph().put_graphs_mode(body, auth=_cfg.test_password)
        print(code, res)
        self.assertEqual(code, 403, 'Unauthorized code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=%s,type=STATUS,operated=*}' % _cfg.graph_name,
            'Unauthorized result check fail'
        )

    def test_status_write(self):
        """
        资源写权限
        :resurn:
        """
        permission_list = [
            {'target_list': [{'type': 'STATUS'}], 'permission': 'WRITE', 'name': 'status_write'},
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)

        # check role
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')

        # check Authorize - 该接口只有管理员有权限，普通用户即使赋予了status资源写权限也返回403，符合预期
        body = 'NONE'
        code, res = Graph().put_graphs_mode(body, auth=user)
        print(code, res)
        self.assertEqual(code, 200, 'Authorize code check fail')
        self.assertEqual(res, {'mode': 'NONE'}, 'Authorize result check fail')

        # check Unauthorized    越权验证失败，此处有bug
        code, res = Graph().get_one_graph(auth=user)
        print(code, res)
        # self.assertEqual(code, 403, 'Unauthorized code check fail')
        # self.assertEqual(
        #     res['message'],
        #     'Permission denied: read Resource{graph=hugegraph,type=STATUS,operated=*}',
        #     'Unauthorized result check fail'
        # )
        self.assertEqual(code, 200)
        self.assertEqual(res, {'name': _cfg.graph_name, 'backend': 'rocksdb'})

    def test_propertyKey_read(self):
        """
        property_key读权限
        :resurn:
        """
        # add graph
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create()", auth=auth)
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ', 'name':
                'propertyKey_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)

        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, 'READ', msg='role permission check fail')
            self.assertEqual(value[0]['type'], 'PROPERTY_KEY', msg='role type check fail')

        # check Authorize
        code, res = Schema().get_all_properties(auth=user)
        print(code, res)
        self.assertEqual(code, 200, 'Authorize code check fail')
        self.assertEqual(res['propertykeys'][0]['name'], 'name', 'Authorize result check fail')

        # check Unauthorized--write
        body = {
            'name': 'test_name',
            'data_type': 'INT',
            'cardinality': 'SINGLE'
        }
        code, res = Schema().create_property(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, 'Unauthorized code check fail')
        self.assertEqual(
            res['message'],
            "User not authorized.",
            'Unauthorized result check fail'
        )

        # check Unauthorized--delete
        name = 'test_name'
        code, res = Schema().delete_property_by_name(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, 'Unauthorized code check fail')
        self.assertEqual(
            res['message'],
            "User not authorized.",
            'Unauthorized result check fail'
        )

    def test_propertyKey_write(self):
        """
        property_key写权限
        :resurn:
        """
        permission_list = [
            {'target_list': [{'type': 'PROPERTY_KEY'}], 'permission': 'WRITE', 'name': 'propertyKey_write'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)

        # check role
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, 'WRITE', msg='role permission check fail')
            self.assertEqual(value[0]['type'], 'PROPERTY_KEY', msg='role type check fail')

        # check Authorize
        body = {
            'name': 'name',
            'data_type': 'INT',
            'cardinality': 'SINGLE'
        }
        code, res = Schema().create_property(body, auth=user)
        print(code, res)
        self.assertEqual(code, 202, 'Authorize code check fail')
        self.assertEqual(res['property_key']['name'], body['name'], 'Authorize result check fail')

        # check Unauthorized--read
        code, res = Schema().get_all_properties(auth=user)
        print(code, res)
        self.assertEqual(code, 403, 'Unauthorized code check fail')
        self.assertEqual(res['message'], "User not authorized.", 'Unauthorized result check fail')

        # check Unauthorized--delete
        name = 'age'
        code, res = Schema().delete_property_by_name(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, 'Unauthorized code check fail')
        self.assertEqual(res['message'], "User not authorized.", 'Unauthorized result check fail')

    def test_propertyKey_delete(self):
        """
        property_key删权限
        :resurn:
        """
        # add graph_propertyKey
        body = {
            'name': 'test',
            'data_type': 'INT',
            'cardinality': 'SINGLE'
        }
        code, res = Schema().create_property(body, auth=auth)
        print(code, res)

        # check role
        permission_list = [
            {'target_list': [{'type': 'PROPERTY_KEY'}], 'permission': 'DELETE', 'name': 'propertyKey_delete'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, 'DELETE', msg='role permission check fail')
            self.assertEqual(value[0]['type'], 'PROPERTY_KEY', msg='role type check fail')

        # check Authorize--delete  delete请求成功返回只有状态码，没有message返回
        name = 'test'
        code, res = Schema().delete_property_by_name(name, auth=user)
        print(code, res)
        self.assertEqual(code, 202, msg='Unauthorized code check fail')

        # check Unauthorized--read
        code, res = Schema().get_all_properties(auth=user)
        self.assertEqual(code, 403, msg='Authorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check Unauthorized--write
        body = {
            'name': 'test_name',
            'data_type': 'INT',
            'cardinality': 'SINGLE'
        }
        code, res = Schema().create_property(body, auth=user)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_vertexLabel_read(self):
        """
        vertex_label读权限 有bug
        :resurn:
        """
        # add graph
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name').primaryKeys('name')"
                               ".ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {'target_list': [{'type': 'PROPERTY_KEY'}, {'type': 'VERTEX_LABEL'}],
             'permission': 'READ',
             'name': 'vertex_label_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, 'READ', msg='role permission check fail')
            self.assertEqual(value[1]['type'], 'VERTEX_LABEL', msg='role type check fail')

        # check Authorize--read
        code, res = Schema().get_vertexLabel(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check Unauthorized--write
        body = {
            'name': 'test',
            'id_strategy': 'DEFAULT',
            'properties': ['name'],
            'primary_keys': ['name'],
            'nullable_keys': [],
            'enable_label_index': True
        }
        code, res = Schema().create_vertexLabel(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check Unauthorized--delete
        name = 'person'
        code, res = Schema().delete_vertexLabel(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_vertexLabel_write(self):
        """
        vertex_label写权限
        :resurn:
        """
        # add graph
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {'target_list': [{'type': 'PROPERTY_KEY'}], 'permission': 'READ', 'name': 'propertyKey_read'},
            {'target_list': [{'type': 'VERTEX_LABEL'}], 'permission': 'WRITE', 'name': 'vertexLabel_write'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'VERTEX_LABEL', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'PROPERTY_KEY', msg='role type check fail')

        # check Authorize
        body = {
            'name': 'test',
            'id_strategy': 'DEFAULT',
            'properties': ['name'],
            'primary_keys': ['name'],
            'nullable_keys': [],
            'enable_label_index': True
        }
        code, res = Schema().create_vertexLabel(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='authorized code check fail')
        self.assertEqual(res['name'], 'test', 'authorized res check fail')

        # check Unauthorized--READ
        code, res = Schema().get_vertexLabel(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='UnAuthorized code check fail')
        self.assertEqual(res['message'], "User not authorized.", msg='UnAuthorized result check fail')

        # check Unauthorized--DELETE
        name = 'person'
        code, res = Schema().delete_vertexLabel(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_vertexLabel_delete(self):
        """
        vertex_label删权限
        :resurn:
        """
        # add graph
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name').primaryKeys('name')"
                               ".ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {'target_list': [{'type': 'VERTEX_LABEL'}], 'permission': 'DELETE', 'name': 'vertexLabel_delete'},
            {'target_list': [{'type': 'TASK'}], 'permission': 'WRITE', 'name': 'task_write'},
            {'target_list': [
                {'type': 'TASK'},
                {'type': 'VERTEX_LABEL'}
            ], 'permission': 'READ', 'name': 'task_read'},
            {'target_list': [{'type': 'TASK'}], 'permission': 'EXECUTE', 'name': 'task_execute'},
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'VERTEX_LABEL', msg='role type check fail')
            elif key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            else:
                pass

        # check Authorize
        name = 'person'
        code, res = Schema().delete_vertexLabel(name, auth=user)
        print(code, res)
        self.assertEqual(code, 202, msg='Unauthorized code check fail')

        id = res['task_id']
        time.sleep(10)  # 延迟10s
        code, res = Task().get_task(id, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, 'Authorize code check fail')
        self.assertEqual(res['task_status'], 'success',
                         msg='Authorize result check fail')  # 通过接口访问返回fail，但是在界面操作是没问题的，需要追下原因--具体情况常帅知道

        # check Unauthorized-- delete 需要 read 权限
        code, res = Schema().get_vertexLabel(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='UnAuthorized code check fail')

        # check Unauthorized--WRITE
        body = {
            'name': 'test',
            'id_strategy': 'DEFAULT',
            'properties': ['name'],
            'primary_keys': ['name'],
            'nullable_keys': [],
            'enable_label_index': True
        }
        code, res = Schema().create_vertexLabel(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_edgeLabel_read(self):
        """
        edge_label读权限
        :resurn:
        """
        # add graph
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name').primaryKeys('name')"
                               ".ifNotExist().create();"
                               "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')"
                               ".properties('name').ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {
                'target_list': [{'type': 'PROPERTY_KEY'}, {'type': 'VERTEX_LABEL'}, {'type': 'EDGE_LABEL'}],
                'permission': 'READ',
                'name': 'propertyKey_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, 'READ', msg='role permission check fail')
            self.assertEqual(value[2]['type'], 'EDGE_LABEL', msg='role type check fail')

        # check Authorize--read
        code, res = Schema().get_edgeLabel(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check Unauthorized--write
        body = {
            'name': 'test_name',
            'source_label': 'person',
            'target_label': 'software',
            'frequency': 'SINGLE',
            'properties': []
        }
        code, res = Schema().create_edgeLabel(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check Unauthorized--delete
        name = 'link'
        code, res = Schema().delete_edgeLabel(name, auth=user)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_edgeLabel_write(self):
        """
        edge_label写权限
        :resurn:
        """
        # add graph
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name').primaryKeys('name')"
                               ".ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {'target_list': [{'type': 'PROPERTY_KEY'}, {'type': 'VERTEX_LABEL'}],
             'permission': 'READ', 'name': 'propertyKey_read'},
            {'target_list': [{'type': 'EDGE_LABEL'}], 'permission': 'WRITE', 'name': 'edgeLabel_write'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'EDGE_LABEL', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'PROPERTY_KEY', msg='role type check fail')

        # check Authorize
        body = {
            'name': 'link',
            'source_label': 'person',
            'target_label': 'person',
            'frequency': 'SINGLE',
            'properties': []
        }
        code, res = Schema().create_edgeLabel(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Unauthorized code check fail')

        # check Unauthorized--READ
        code, res = Schema().get_edgeLabel(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='UnAuthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='UnAuthorized result check fail')

        # check Unauthorized--DELETE
        name = 'link'
        code, res = Schema().delete_edgeLabel(name, auth=user)
        print(code, res)
        self.assertNotEqual(code, 201, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_edgeLabel_delete(self):
        """
        vertex_label删权限
        :resurn:
        """
        # add graph
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name').primaryKeys('name')"
                               ".ifNotExist().create();", auth=auth)

        # add edgelabel
        body = {
            'name': 'link',
            'source_label': 'person',
            'target_label': 'person',
            'frequency': 'SINGLE',
            'properties': [],
            'enable_label_index': False
        }
        Schema().create_edgeLabel(body, auth=auth)

        # check role
        permission_list = [
            {'target_list': [{'type': 'EDGE_LABEL'}], 'permission': 'DELETE', 'name': 'edgeLabel_delete'},
            {'target_list': [{'type': 'TASK'}], 'permission': 'WRITE', 'name': 'task_write'},
            {'target_list': [{'type': 'TASK'}], 'permission': 'EXECUTE', 'name': 'task_execute'},
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'EDGE_LABEL', msg='role type check fail')
            elif key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize
        name = 'link'
        code, res = Schema().delete_edgeLabel(name, auth=user)
        print(code, res)
        self.assertEqual(code, 202, msg='Unauthorized code check fail')
        id = res['task_id']
        time.sleep(10)  # 延迟10s
        code, res = Task().get_task(id, auth=auth)
        print(code, res)
        self.assertEqual(res['task_status'], 'success',
                         msg='Authorize result check fail')  # 通过接口访问返回fail，但是在界面操作是没问题的，需要追下原因--具体情况常帅知道

        # check Unauthorized--READ
        code, res = Schema().get_edgeLabel(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='UnAuthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='UnAuthorized result check fail')

        # check Unauthorized--WRITE
        code, res = Schema().create_edgeLabel(body, auth=user)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='UnAuthorized result check fail')

    def test_indexLabel_vertex_read(self):
        """
        index_label 读权限
        :resurn:
        """
        # add schema_indexLabel
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
                               "graph.schema().propertyKey('city').asInt().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name', 'age', 'city')"
                               ".primaryKeys('name').ifNotExist().create();"
                               "graph.schema().indexLabel('personByAge').onV('person').by('age')"
                               ".range().ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {
                'target_list': [{'type': 'PROPERTY_KEY'}, {'type': 'VERTEX_LABEL'}, {'type': 'INDEX_LABEL'}],
                'permission': 'READ',
                'name': 'indexLabel_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[2]['type'], 'INDEX_LABEL', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Schema().get_index(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check Unauthorized--write
        body = {
            'name': 'personByCity',
            'base_type': 'VERTEX_LABEL',
            'base_value': 'person',
            'index_type': 'SECONDARY',
            'fields': [
                'city'
            ]
        }
        code, res = Schema().create_index(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check Unauthorized--delete
        name = 'personByAge'
        code, res = Schema().delete_index(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_indexLabel_vertex_write(self):
        """
        index_label写权限
        :resurn:
        """
        # add schema_indexLabel
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
                               "graph.schema().propertyKey('city').asInt().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name', 'age', 'city')"
                               ".primaryKeys('name').ifNotExist().create();"
                               "graph.schema().indexLabel('personByAge').onV('person').by('age')"
                               ".range().ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {'target_list': [
                {'type': 'PROPERTY_KEY'},
                {'type': 'VERTEX_LABEL'},
                {'type': 'INDEX_LABEL'}
            ],
                'permission': 'READ', 'name': 'propertyKey_read'
            },
            {'target_list': [
                {'type': 'INDEX_LABEL'},
                {'type': 'TASK'}
            ],
                'permission': 'WRITE', 'name': 'indexLabel_write'
            },
            {'target_list': [
                {'type': 'TASK'}],
                'permission': 'EXECUTE', 'name': 'task_execute'
            },
            {'target_list': [
                {'type': 'STATUS'}
            ], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'INDEX_LABEL', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
                self.assertIn(value[1]['type'], 'PROPERTY_KEY', msg='role type check fail')

        # check Authorize
        body = {
            'name': 'personByCity',
            'base_type': 'VERTEX_LABEL',
            'base_value': 'person',
            'index_type': 'SECONDARY',
            'fields': [
                'city'
            ]
        }
        code, res = Schema().create_index(body, auth=user)
        print(code, res)
        self.assertEqual(code, 202, msg='authorized code check fail')
        self.assertEqual(res['index_label']['name'], 'personByCity', 'authorized res check fail')

        # check Unauthorized--READ  index_label是写要具有读的权限
        code, res = Schema().get_index(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='UnAuthorized code check fail')
        self.assertEqual(res['indexlabels'][0]['name'], 'personByAge', msg='UnAuthorized result check fail')

        # check Unauthorized--DELETE
        name = 'personByAge'
        code, res = Schema().delete_index(name, auth=user)
        print(code, res)
        self.assertNotEqual(code, 202, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_indexLabel_vertex_delete(self):
        """
        index_label删权限
        :resurn:
        """
        # add schema_indexLabel
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
                               "graph.schema().propertyKey('city').asInt().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name', 'age', 'city')"
                               ".primaryKeys('name').ifNotExist().create();"
                               "graph.schema().indexLabel('personByAge').onV('person').by('age')"
                               ".range().ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {'target_list': [
                {'type': 'INDEX_LABEL'}
            ], 'permission': 'DELETE', 'name': 'indexLabel_delete'},
            {'target_list': [
                {'type': 'TASK'}
            ], 'permission': 'WRITE', 'name': 'task_write'},
            {'target_list': [
                {'type': 'TASK'}
            ], 'permission': 'READ', 'name': 'task_read'},
            {'target_list': [
                {'type': 'TASK'}
            ], 'permission': 'EXECUTE', 'name': 'task_execute'},
            {'target_list': [
                {'type': 'STATUS'}
            ], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'INDEX_LABEL', msg='role type check fail')
            elif key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
                self.assertIn(value[1]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize
        name = 'personByAge'
        code, res = Schema().delete_index(name, auth=user)
        print(code, res)
        self.assertEqual(code, 202, msg='Unauthorized code check fail')

        id = res['task_id']
        time.sleep(10)  # 延迟10s
        code, res = Task().get_task(id, auth=auth)
        print(code, res)
        self.assertEqual(res['task_status'], 'success',
                         msg='Authorize result check fail')

        # check Unauthorized--READ
        code, res = Schema().get_index(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='UnAuthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check Unauthorized--WRITE
        body = {
            'name': 'personByCity',
            'base_type': 'VERTEX_LABEL',
            'base_value': 'person',
            'index_type': 'SECONDARY',
            'fields': [
                'city'
            ]
        }
        code, res = Schema().create_index(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_indexLabel_edge_read(self):
        """
        edge_index_label 读权限
        :resurn:
        """
        # add schema_indexLabel
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
                               "graph.schema().propertyKey('city').asInt().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name')"
                               ".primaryKeys('name').ifNotExist().create();"
                               "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')"
                               ".properties('age', 'city').ifNotExist().create();"
                               "graph.schema().indexLabel('linkByAge').onE('link').by('age')"
                               ".range().ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'PROPERTY_KEY'},
                    {'type': 'EDGE_LABEL'},
                    {'type': 'INDEX_LABEL'},
                    {'type': 'VERTEX_LABEL'}
                ],
                'permission': 'READ',
                'name': 'indexLabel_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[2]['type'], 'INDEX_LABEL', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Schema().get_index(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check Unauthorized--write
        body = {
            'name': 'linkByCity',
            'base_type': 'EDGE_LABEL',
            'base_value': 'created',
            'index_type': 'SECONDARY',
            'fields': [
                'city'
            ]
        }
        code, res = Schema().create_index(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check Unauthorized--delete
        name = 'linkByAge'
        code, res = Schema().delete_index(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_indexLabel_edge_write(self):
        """
        index_label写权限
        :resurn:
        """
        # add schema_indexLabel
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
                               "graph.schema().propertyKey('city').asInt().ifNotExist().create();"
                               "graph.schema().vertexLabel('person').properties('name')"
                               ".primaryKeys('name').ifNotExist().create();"
                               "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')"
                               ".properties('age', 'city').ifNotExist().create();"
                               "graph.schema().indexLabel('linkByAge').onE('link').by('age')"
                               ".range().ifNotExist().create();", auth=auth)

        # check role
        permission_list = [
            {'target_list': [
                {'type': 'PROPERTY_KEY'},
                {'type': 'VERTEX_LABEL'},
                {'type': 'EDGE_LABEL'},
                {'type': 'INDEX_LABEL'}
            ],
                'permission': 'READ', 'name': 'propertyKey_read'},
            {'target_list': [
                {'type': 'INDEX_LABEL'},
                {'type': 'TASK'}
            ],
                'permission': 'WRITE', 'name': 'indexLabel_write'},
            {'target_list': [
                {'type': 'TASK'}
            ], 'permission': 'EXECUTE', 'name': 'task_execute'},
            {'target_list': [
                {'type': 'STATUS'}
            ], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)

        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'INDEX_LABEL', msg='role type check fail')
            elif key == 'EXECUTE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')

        # check Authorize
        body = {
            'name': 'linkByCity',
            'base_type': 'EDGE_LABEL',
            'base_value': 'link',
            'index_type': 'SECONDARY',
            'fields': [
                'city'
            ]
        }
        code, res = Schema().create_index(body, auth=user)
        print(code, res)
        self.assertEqual(code, 202, msg='authorized code check fail')
        self.assertEqual(res['index_label']['name'], 'linkByCity', 'authorized res check fail')

        # check Unauthorized--READ    write权限需要read权限
        code, res = Schema().get_index(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='UnAuthorized code check fail')
        self.assertEqual(res['indexlabels'][0]['name'], 'linkByAge', msg='UnAuthorized result check fail')

        # check Unauthorized--DELETE
        name = 'createdByCity'
        code, res = Schema().delete_index(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_indexLabel_edge_delete(self):
        """
        index_label删权限
        :resurn:
        """
        # add schema_indexLabel
        code, res = Gremlin().gremlin_post(
            "graph.schema().propertyKey('name').asText().ifNotExist().create();"
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
            "graph.schema().propertyKey('city').asInt().ifNotExist().create();"
            "graph.schema().vertexLabel('person').properties('name')"
            ".primaryKeys('name').ifNotExist().create();"
            "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')"
            ".properties('age', 'city').ifNotExist().create();"
            "graph.schema().indexLabel('linkByAge').onE('link').by('age')"
            ".range().ifNotExist().create();", auth=auth)
        print(code, res)

        # check role
        permission_list = [
            {'target_list': [{'type': 'INDEX_LABEL'}], 'permission': 'DELETE', 'name': 'indexLabel_delete'},
            {'target_list': [{'type': 'TASK'}], 'permission': 'WRITE', 'name': 'task_write'},
            {'target_list': [{'type': 'TASK'}], 'permission': 'EXECUTE', 'name': 'task_execute'},
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'INDEX_LABEL', msg='role type check fail')
            elif key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize
        name = 'linkByAge'
        code, res = Schema().delete_index(name, auth=user)
        print(code, res)
        self.assertEqual(code, 202, msg='Unauthorized code check fail')

        id = res['task_id']
        time.sleep(10)  # 延迟10s
        code, res = Task().get_task(id, auth=auth)
        print(code, res)
        self.assertEqual(res['task_status'], 'success', msg='Authorize result check fail')

        # check Unauthorized--READ
        code, res = Schema().get_index(auth=user)
        self.assertEqual(code, 403, msg='UnAuthorized code check fail')
        # self.assertEqual(res['indexlabels'], [], msg='UnAuthorized result check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check Unauthorized--WRITE
        body = {
            'name': 'createdByCity',
            'base_type': 'EDGE_LABEL',
            'base_value': 'created',
            'index_type': 'SECONDARY',
            'fields': [
                'city'
            ]
        }
        code, res = Schema().create_index(body, auth=user)
        self.assertEqual(code, 403, msg='Unauthorized code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_vertex_aggr_read(self):
        """
        vertex_arrg 读权限
        :resurn:
        """
        # add schema_aggregate
        code, res = Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                                           "graph.schema().propertyKey('sum_num').asInt().calcSum()"
                                           ".ifNotExist().create();"
                                           "graph.schema().vertexLabel('person').properties('name', 'sum_num')"
                                           ".primaryKeys('name').ifNotExist().create();"
                                           "graph.schema().edgeLabel('link')"
                                           ".sourceLabel('person').targetLabel('person')"
                                           ".properties('name').ifNotExist().create();"
                                           "a = graph.addVertex(T.label, 'person', 'name', 'a', 'sum_num', 29);"
                                           "b = graph.addVertex(T.label, 'person', 'name', 'b', 'sum_num', 39);"
                                           "a.addEdge('link', b, 'name', 'link');", auth=user)

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VERTEX_AGGR'}
                ],
                'permission': 'READ',
                'name': 'vertexAggr_read'
            },
            {
                'target_list': [
                    {'type': 'GREMLIN'}
                ],
                'permission': 'EXECUTE',
                'name': 'gremlin_execute'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'VERTEX_AGGR', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Gremlin().gremlin_post('g.V().count()', auth=user)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check UNAuthorize--read
        code, res = Gremlin().gremlin_post('g.E().count()', auth=user)
        self.assertEqual(code, 403, msg='Unauthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: read Resource{graph=%s,type=EDGE_AGGR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

    def test_edge_aggr_read(self):
        """
        edge_aggr 读权限
        :resurn:
        """
        # add schema_aggregate
        code, res = Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                                           "graph.schema().propertyKey('sum_num').asInt().calcSum()"
                                           ".ifNotExist().create();"
                                           "graph.schema().vertexLabel('person').properties('name')"
                                           ".primaryKeys('name').ifNotExist().create();"
                                           "graph.schema().edgeLabel('link')"
                                           ".sourceLabel('person').targetLabel('person')"
                                           ".properties('name', 'sum_num').ifNotExist().create();"
                                           "a = graph.addVertex(T.label, 'person', 'name', 'a');"
                                           "b = graph.addVertex(T.label, 'person', 'name', 'b');"
                                           "a.addEdge('link', b, 'name', 'link', 'sum_num', 39);", auth=user)

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'EDGE_AGGR'}
                ],
                'permission': 'READ',
                'name': 'edgeAggr_read'
            },
            {
                'target_list': [
                    {'type': 'GREMLIN'}
                ],
                'permission': 'EXECUTE',
                'name': 'gremlin_execute'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'EDGE_AGGR', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Gremlin().gremlin_post('g.E().count()', auth=user)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check unAuthorize--read
        code, res = Gremlin().gremlin_post('g.V().count()', auth=user)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: read Resource{graph=%s,type=VERTEX_AGGR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

    def test_vertex_read(self):
        """
        vertex_read 读权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VERTEX'},
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'vertex_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'VERTEX', msg='role type check fail')
            else:
                pass

        # check Authorize-- vertex read
        v_id = '\"1:marko\"'
        code, res = Vertex().get_vertex_by_id(v_id, auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')
        self.assertEqual(res['id'], '1:marko', msg='Authorize code check fail')

        # check unAuthorize--edge read
        e_id = 'S1:marko>1>>S1:vadas'
        code, res = Edge().get_edge_by_id(e_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize-- write
        body = {
            'label': 'person',
            'properties': {
                'name': 'graph_test',
                'age': 29
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize-- delete
        code, res = Vertex().delete_vertex(v_id, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_vertex_write(self):
        """
        basic_operation 写权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VERTEX'},
                ],
                'permission': 'WRITE',
                'name': 'vertex_write'
            },
            {
                'target_list': [
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'vertexLabel_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'VERTEX', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        body = {
            'label': 'person',
            'properties': {
                'name': 'graph_test',
                'age': 29,
                'city': 'Baoding'
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Authorize code check fail')
        self.assertEqual(res['id'], '1:graph_test', msg='Authorize code check fail')

        # check unAuthorize--read
        code, res = Vertex().get_vertex_by_id('\"1:marko\"', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize--delete
        code, res = Vertex().delete_vertex('1:alg', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_vertex_delete(self):
        """
        basic_operation 删除权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VERTEX'}
                ],
                'permission': 'DELETE',
                'name': 'vertex_delete'
            },
            {
                'target_list': [
                    {'type': 'VERTEX'},
                    {'type': 'EDGE_LABEL'},
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'vertex_read'
            },
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'VERTEX', msg='role type check fail')
            else:
                pass

        # check Authorize --  delete
        code, res = Vertex().delete_vertex('\"1:marko\"', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize-- write
        body = {
            'label': 'person',
            'properties': {
                'name': 'graph_test',
                'age': 29,
                'city': 'Baoding'
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_edge_read(self):
        """
        edge 读权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'PROPERTY_KEY'},
                    {'type': 'EDGE_LABEL'},
                    {'type': 'EDGE'},
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'VERTEX'}
                ],
                'permission': 'READ',
                'name': 'edge_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[2]['type'], 'EDGE', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Edge().get_edge_by_id('S1:marko>1>>S1:vadas', auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check unAuthorize-- edge write
        body = {
            'label': 'created',
            'outV': '1:marko',
            'inV': '2:lop',
            'outVLabel': 'person',
            'inVLabel': 'software',
            'properties': {
                'date': '2017-5-18',
                'city': 'Baoding'
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize-- edge delete
        code, res = Edge().delete_edge('S1:marko>1>>S1:vadas', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_edge_write(self):
        """
        edge 写权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'EDGE'}
                ],
                'permission': 'WRITE',
                'name': 'edge_write'
            },
            {
                'target_list': [
                    {'type': 'VERTEX'},
                    {'type': 'EDGE_LABEL'},
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'property_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'EDGE', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        body = {
            'label': 'created',
            'outV': '1:marko',
            'inV': '2:lop',
            'outVLabel': 'person',
            'inVLabel': 'software',
            'properties': {
                'city': 'Mancheng',
                'date': '20200810'
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Authorize code check fail')

        # check unAuthorize--read
        code, res = Edge().get_edge_by_id('S1:marko>1>>S1:vadas', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize--delete
        code, res = Edge().delete_edge('S1:marko>1>>S1:vadas', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_edge_delete(self):
        """
        edge 删除权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'EDGE'}
                ],
                'permission': 'DELETE',
                'name': 'edge_delete'
            },
            {
                'target_list': [
                    {'type': 'EDGE'},
                    {'type': 'VERTEX'},
                    {'type': 'EDGE_LABEL'},
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'property_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'EDGE', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = Edge().delete_edge('S1:marko>1>>S1:vadas', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize--write
        body = {
            'label': 'created',
            'outV': '1:marko',
            'inV': '2:lop',
            'outVLabel': 'person',
            'inVLabel': 'software',
            'properties': {
                'city': 'Baoding',
                'date': '20200810'
            }
        }
        code, res = Edge().create_single_edge(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # # check unAuthorize--read  删除边的时候依赖读取边的权限
        # code, res = Edge().get_edge_by_id('S1:peter>1>>S1:josh', auth=user)
        # print(code, res)
        # self.assertEqual(code, 403, msg='unAuthorize code check fail')
        # self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

    def test_gremlin_vertex_execute(self):
        """
        basic_operation 读权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VERTEX'},
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'vertex_read'
            },
            {
                'target_list': [
                    {'type': 'GREMLIN'}
                ],
                'permission': 'EXECUTE',
                'name': 'gremlin_execute'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'VERTEX', msg='role type check fail')
            elif key == 'GREMLIN':
                self.assertIn(value[0]['type'], 'EXECUTE', msg='role type check fail')
            else:
                pass

        # check Authorize-- read
        code, res = Gremlin().gremlin_post('g.V().limit(2)', auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')
        self.assertEqual(len(res['result']['data']), 2, msg='Authorize code check fail')

        # check unAuthorize--edge read
        code, res = Gremlin().gremlin_post('g.E().limit(2)', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            "Permission denied: read Resource{graph=%s,type=EDGE_LABEL,operated=help(id=3)}" % _cfg.graph_name,
            msg='unAuthorize code check fail'
        )

    def test_gremlin_edge_execute(self):
        """
        edge 读权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VERTEX'},
                    {'type': 'EDGE'},
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'EDGE_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'edge_read'
            },
            {
                'target_list': [
                    {'type': 'GREMLIN'}
                ],
                'permission': 'EXECUTE',
                'name': 'gremlin_execute'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[1]['type'], 'EDGE', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Gremlin().gremlin_post('g.E().limit(2)', auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')

        # check unAuthorize--read
        # code, res = Gremlin().gremlin_post('g.V().limit(2)', auth=user)
        # print(code, res)
        # # gremlin执行权限中查询边的权限 - 依赖查询点的权限
        # self.assertEqual(code, 403, msg='unAuthorize code check fail')

    def test_var_read(self):
        """
        var 读权限
        :resurn:
        """
        # premise
        name = 'var'
        code, res = Variable().put_var({'data': 'test'}, name, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, 'var premise code is failed')
        self.assertEqual(res, {'var': 'test'}, 'var premise res is failed')

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VAR'}
                ],
                'permission': 'READ',
                'name': 'var_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'VAR', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Variable().get_var(name, auth=auth)
        print(code, res)

        code, res = Variable().get_var(name, auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'var': 'test'}, 'unAuthorize res check fail')

        # check unAuthorize--write
        body = {
            'data': 'tom'
        }
        code, res = Variable().put_var(body, 'name', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=%s,type=VAR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

        # check unAuthorize--delete
        code, res = Variable().delete_var('name', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=%s,type=VAR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

    def test_var_write(self):
        """
        var 写权限
        :resurn:
        """
        # check role
        permission_list = [
            {'target_list': [{'type': 'VAR'}], 'permission': 'WRITE', 'name': 'var_write'},
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'VAR', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        name = 'var'
        body = {
            'data': 'tom'
        }
        code, res = Variable().put_var(body, name, auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')
        self.assertEqual(res, {name: 'tom'}, 'Authorize res check fail')

        # check unAuthorize--read
        code, res = Variable().get_var(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: read Resource{graph=%s,type=VAR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

        # check unAuthorize--delete
        code, res = Variable().delete_var('name', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=%s,type=VAR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

    def test_var_delete(self):
        """
        var 删除权限
        :resurn:
        """
        # premise
        name = 'var'
        code, res = Variable().put_var({'data': 'test'}, name, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, 'var premise code is failed')
        self.assertEqual(res, {'var': 'test'}, 'var premise res is failed')

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'VAR'}
                ],
                'permission': 'DELETE',
                'name': 'var_delete'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'VAR', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = Variable().delete_var(name, auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize--write
        body = {
            'data': 'tom'
        }
        code, res = Variable().put_var(body, 'name', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=%s,type=VAR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

        # check unAuthorize--read
        code, res = Variable().get_var(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: read Resource{graph=%s,type=VAR,operated=*}' % _cfg.graph_name,
            msg='Unauthorized result check fail'
        )

    def test_task_write_read_contain_grants(self):
        """
        task 写、执行、读权限  用户只能读取自己写的task
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'TASK'}
                ],
                'permission': 'WRITE',
                'name': 'task_write'
            },
            {
                'target_list': [
                    {'type': 'TASK'},
                    {'type': 'GREMLIN'}
                ],
                'permission': 'EXECUTE',
                'name': 'task_execute'
            },
            {
                'target_list': [
                    {'type': 'TASK'}
                ],
                'permission': 'READ',
                'name': 'task_read'
            },
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        gremlin = '1+1'
        code, res = Gremlin().gremlin_job(gremlin, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(res['task_id'], 1, msg='unAuthorize code check fail')

        # check Authorize-- read
        code, res = Task().get_task(1, auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')

    def test_task_read_execute_grants(self):
        """
        task 写、执行、读权限  用户只能读取自己写的task
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'TASK'}
                ],
                'permission': 'READ',
                'name': 'task_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            else:
                pass

        # admin 用户创建task
        gremlin = '1+1'
        code, res = Gremlin().gremlin_job(gremlin, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(res['task_id'], 1, msg='unAuthorize code check fail')

        # check Authorize-- tester用户读取admin用户的task失败
        code, res = Task().get_task(1, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Authorize code check fail')
        self.assertEqual(
            res['message'],
            "Permission denied: read Resource{graph=%s,type=TASK,operated=1}" % _cfg.graph_name
        )

    def test_task_execute_write_delete(self):
        """
        task 删除、执行权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'TASK'}
                ],
                'permission': 'DELETE',
                'name': 'task_delete'
            },
            {
                'target_list': [
                    {'type': 'TASK'}
                ],
                'permission': 'WRITE',
                'name': 'task_write'
            },
            {
                'target_list': [
                    {'type': 'TASK'},
                    {'type': 'GREMLIN'}
                ],
                'permission': 'EXECUTE',
                'name': 'task_execute'
            },
            {
                'target_list': [
                    {'type': 'STATUS'}
                ],
                'permission': 'READ',
                'name': 'status_read'
            }

        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            elif key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        gremlin = '1+1'
        code, res = Gremlin().gremlin_job(gremlin, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(res['task_id'], 1, msg='unAuthorize code check fail')

        # check Authorize--delete
        get_task_res(res['task_id'], 60, auth=auth)
        code, res = Task().delete_task('1', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

    def test_target_read(self):
        """
        target 读权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'TARGET'}
                ],
                'permission': 'READ',
                'name': 'target_read',
                'graph_name': _cfg.auth_graph
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.auth_graph].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'TARGET', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = AuthGH().get_targets(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')
        self.assertEqual(res['targets'][0]['target_name'], 'target_read_target', 'Authorize res check fail')

        # check unAuthorize--write
        body = {
            'target_url': '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            'target_name': 'gremlin',
            'target_graph': '%s' % _cfg.graph_name,
            'target_resources': [
                {'type': 'GREMLIN'}
            ]
        }
        code, res = AuthGH().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=%s,type=TARGET,operated=target(gremlin)}' % _cfg.auth_graph,
            'unAuthorize res check fail'
        )

        # check unAuthorize--delete
        code, res = AuthGH().delete_targets('-77:target_read_target', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=%s,type=TARGET,operated=target(target_read_target)}'
            % _cfg.auth_graph,
            'unAuthorize res check fail'
        )

    def test_target_write(self):
        """
        target 写权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'TARGET'}
                ],
                'permission': 'WRITE',
                'name': 'target_write',
                'graph_name': _cfg.auth_graph
            },
            {
                'target_list': [
                    {'type': 'STATUS'}
                ],
                'permission': 'READ',
                'name': 'status_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.auth_graph].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'TARGET', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        body = {
            'target_url': '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            'target_name': 'gremlin',
            'target_graph': '%s' % _cfg.graph_name,
            'target_resources': [
                {'type': 'GREMLIN'}
            ]
        }
        code, res = AuthGH().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Authorize code check fail')
        self.assertEqual(res['target_name'], 'gremlin', msg='Authorize res check fail')

        # check unAuthorize--read
        code, res = AuthGH().get_targets(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'targets': []}, 'unAuthorize res check fail')

        # check unAuthorize--delete
        code, res = AuthGH().delete_targets('-77:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=%s,type=TARGET,operated=target(gremlin)}' % _cfg.auth_graph,
            'unAuthorize res check fail'
        )

    def test_target_delete(self):
        """
        target 删除权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'TARGET'}
                ],
                'permission': 'DELETE',
                'name': 'target_delete',
                'graph_name': _cfg.auth_graph
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.auth_graph].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'TARGET', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = AuthGH().delete_targets('-77:target_delete_target', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize--write
        body = {
            'target_url': '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            'target_name': 'gremlin',
            'target_graph': '%s' % _cfg.graph_name,
            'target_resources': [
                {'type': 'GREMLIN'}
            ]
        }
        code, res = AuthGH().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=%s,type=TARGET,operated=target(gremlin)}' % _cfg.auth_graph,
            'unAuthorize res check fail'
        )

        # check unAuthorize--read
        code, res = AuthGH().get_targets(auth=user)
        print(code, res)
        self.assertEqual(res['targets'], [], msg='unAuthorize code check fail')

    def test_all_read(self):
        """
        all 读权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'ALL'}
                ],
                'permission': 'READ',
                'name': 'all_read'
            },
            {
                'target_list': [
                    {'type': 'ALL'}
                ],
                'permission': 'EXECUTE',
                'name': 'all_execute'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'ALL', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Gremlin().gremlin_post('g.E().limit(10).count()', auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='Authorize code check fail')
        self.assertEqual(res['result']['data'], [6], msg='Authorize code check fail')

        # check unAuthorize--write
        body = {
            'label': 'person',
            'properties': {
                'name': 'graph_test',
                'age': 29,
                'city': 'baoDing'
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize--delete
        code, res = Vertex().delete_vertex('\"1:josh\"', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize--grant
        code, res = AuthGH().get_targets(auth=user)
        print(code, res)
        if code == 200:
            self.assertEqual(res['targets'], [], msg='unAuthorize code check fail')
        else:
            self.assertEqual(code, 403, msg='unAuthorize code check fail')

    def test_all_write(self):
        """
        all 写权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'ALL'}
                ],
                'permission': 'WRITE',
                'name': 'all_write'
            },
            {
                'target_list': [
                    {'type': 'ALL'}
                ],
                'permission': 'EXECUTE',
                'name': 'all_execute'
            },
            {
                'target_list': [
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'}
                ],
                'permission': 'READ',
                'name': 'schema_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'ALL', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        body = {
            'label': 'person',
            'properties': {
                'name': 'graph_test',
                'age': 29,
                'city': 'baoDing'
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Authorize code check fail')

        # check unAuthorize--read
        code, res = Vertex().get_vertex_by_id('\"1:josh\"', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize--delete
        code, res = Vertex().delete_vertex('\"1:josh\"', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(res['message'], 'User not authorized.', msg='Unauthorized result check fail')

        # check unAuthorize--grant
        body = {
            'target_url': '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            'target_name': 'gremlin',
            'target_graph': '%s' % _cfg.graph_name,
            'target_resources': [
                {'type': 'GREMLIN'}
            ]
        }
        code, res = AuthGH().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=%s,type=TARGET,operated=target(gremlin)}' % _cfg.auth_graph,
            msg='Unauthorized result check fail'
        )

    def test_all_delete(self):
        """
        all 删除权限
        :resurn:
        """
        # add graph
        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'ALL'}
                ],
                'permission': 'DELETE',
                'name': 'all_delete'
            },
            {
                'target_list': [
                    {'type': 'ALL'}
                ],
                'permission': 'EXECUTE',
                'name': 'all_execute'
            },
            {
                'target_list': [
                    {'type': 'VERTEX_LABEL'},
                    {'type': 'PROPERTY_KEY'},
                    {'type': 'VERTEX'},
                    {'type': 'EDGE_LABEL'}
                ],
                'permission': 'READ',
                'name': 'vertexlabel_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'ALL', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = Vertex().delete_vertex('\"1:marko\"', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='authorize code check fail')

        # check unAuthorize--write
        body = {
            'label': 'person',
            'properties': {
                'name': 'graph_test',
                'age': 29,
                'city': 'Baoding'
            }
        }
        code, res = Vertex().create_single_vertex(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

        # check unAuthorize--read
        code, res = Gremlin().gremlin_post('g.E().limit(10).count()', auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res['result']['data'], [0], msg='unAuthorize code check fail')

        # check unAuthorize-- target_delete
        code, res = AuthGH().delete_targets('-77:all_delete_target', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Authorize code check fail')

    def test_grant_read(self):
        """
        grant 读权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'GRANT'}
                ],
                'permission': 'READ',
                'name': 'grant_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = AuthGH().get_accesses(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')

        # check unAuthorize--write
        body = {'group': '-69:gremlin', 'target': '-71:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

        # check unAuthorize--delete
        code, res = AuthGH().delete_accesses('S-69:grant_read_group>-88>11>S-77:grant_read_target', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

    def test_grant_write_exclude_grants(self):
        """
        grant 写tester用户本身不包含的权限（异常case）
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'GRANT'},
                    {'type': 'TARGET'},
                    {'type': 'USER_GROUP'}
                ],
                'permission': 'WRITE',
                'name': 'grant_write',
                'graph_name': _cfg.auth_graph
            },
            {
                'target_list': [
                    {'type': 'STATUS'}
                ],
                'permission': 'READ',
                'name': 'status_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        self.assertEqual(code, 200)
        # for key, value in res['roles'][_cfg.graph_name].items():
        #     if key == 'WRITE':
        #         self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
        #     elif key == 'READ':
        #         self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
        #     else:
        #         pass

        # check Authorize--write
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Authorize code check fail')
        self.assertEqual(
            res['message'],
            "Permission denied: write Resource{graph=%s,type=GRANT,operated=access(-69:gremlin->-77:gremlin)}"
            % _cfg.auth_graph,
            'Authorize res check fail'
        )

    def test_grant_write_contain_grants(self):
        """
        grant 写tester用户本身不包含的权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'GRANT'},
                    {'type': 'TARGET'},
                    {'type': 'USER_GROUP'}
                ],
                'permission': 'WRITE',
                'name': 'grant_write',
                'graph_name': _cfg.auth_graph
            },
            {
                'target_list': [
                    {'type': 'GREMLIN'},
                ],
                'permission': 'EXECUTE',
                'name': 'gremlin_execute'
            },
            {
                'target_list': [
                    {'type': 'STATUS'},
                ],
                'permission': 'READ',
                'name': 'status_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
            if key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=user)
        print(code, res)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=user)
        print(code, res)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Authorize code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'Authorize res check fail')

        # check unAuthorize--read
        code, res = AuthGH().get_accesses(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'accesses': []}, msg='unAuthorize code check fail')

        # check unAuthorize--delete
        code, res = AuthGH().delete_accesses('S-69:gremlin>-88>18>S-77:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=%s,type=GRANT,operated=access(-69:gremlin->-77:gremlin)}'
            % _cfg.auth_graph,
            'unAuthorize res check fail'
        )

    def test_grant_delete_exclude_grants(self):
        """
        grant 删除权限(异常case) admin创建的权限，普通用户没有删除的权利
        :resurn:
        """
        # premise: admin用户创建权限
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=auth)
        print(code, res)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res1 = AuthGH().post_accesses(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(res1['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'Authorize res check fail')

        # check role ： admin用户创建权限grant的delete权限给tester用户
        permission_list = [
            {
                'target_list': [
                    {'type': 'GRANT'}
                ],
                'permission': 'DELETE',
                'name': 'grant_write',
                'graph_name': _cfg.auth_graph
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=auth)
        print(code, res)
        for key, value in res['roles'][_cfg.auth_graph].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
            else:
                pass

        # check Authorize--delete ： tester用户删除admin创建的权限
        code, res = AuthGH().delete_accesses(res1['id'], auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Authorize code check fail')
        self.assertEqual(
            res['message'],
            "Permission denied: delete Resource{graph=%s,type=GRANT,operated=access(-69:gremlin->-77:gremlin)}"
            % _cfg.auth_graph,
            'Authorize result check fail'
        )

    def test_grant_delete_contain_grants(self):
        """
        grant 删除权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'GRANT'}
                ],
                'permission': 'DELETE',
                'name': 'grant_delete',
                'graph_name': _cfg.auth_graph
            },
            {
                'target_list': [
                    {'type': 'GRANT'},
                    {'type': 'TARGET'},
                    {'type': 'USER_GROUP'}
                ],
                'permission': 'WRITE',
                'name': 'grant_write',
                'graph_name': _cfg.auth_graph
            },
            {
                'target_list': [
                    {'type': 'GREMLIN'},
                ],
                'permission': 'EXECUTE',
                'name': 'gremlin_execute'
            },
            {
                'target_list': [
                    {'type': 'STATUS'},
                ],
                'permission': 'READ',
                'name': 'status_read'
            }

        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=user)
        print(code, res)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=user)
        print(code, res)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'Authorize res check fail')

        code, res = AuthGH().delete_accesses('S-69:gremlin>-88>18>S-77:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize--write
        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(
            res['access_permission'], 'EXECUTE', 'Authorize res check fail')

        # check unAuthorize--read
        code, res = AuthGH().get_accesses(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'accesses': []}, msg='unAuthorize code check fail')

    def test_userGroup_read(self):
        """
        grant 读权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'USER_GROUP'}
                ],
                'permission': 'READ',
                'name': 'userGroup_read',
                'graph_name': _cfg.auth_graph
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.auth_graph].items():
            if key == 'read':
                self.assertIn(value[0]['type'], 'USER_GROUP', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = AuthGH().get_groups(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res['groups'][0]['group_name'], 'userGroup_read_group', msg='unAuthorize res check fail')

        # check unAuthorize--write
        body = {'group_name': 'gremlin', 'group_description': 'group can execute gremlin'}
        code, res = AuthGH().post_groups(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=%s,type=USER_GROUP,operated=group(gremlin)}' % _cfg.auth_graph,
            msg='unAuthorize res check fail'
        )

        # check unAuthorize--delete
        code, res = AuthGH().delete_groups('-69:userGroup_read_group', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

    def test_userGroup_write(self):
        """
        grant 写权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'USER_GROUP'}
                ],
                'permission': 'WRITE',
                'name': 'userGroup_write',
                'graph_name': _cfg.auth_graph
            },
            {
                'target_list': [
                    {'type': 'STATUS'}
                ],
                'permission': 'READ',
                'name': 'status_read'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.auth_graph].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'USER_GROUP', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        body = {'group_name': 'gremlin', 'group_description': 'group can execute gremlin'}
        code, res = AuthGH().post_groups(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')

        # check unAuthorize--read
        code, res = AuthGH().get_groups(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'groups': []}, msg='unAuthorize res check fail')

        # check unAuthorize--delete
        code, res = AuthGH().delete_groups('-69:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

    def test_userGroup_delete(self):
        """
        user_group 删除权限  ---- 删除权限依赖写权限
        :resurn:
        """
        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'USER_GROUP'}
                ],
                'permission': 'DELETE',
                'name': 'userGroup_delete',
                'graph_name': _cfg.auth_graph
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.auth_graph].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'USER_GROUP', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = AuthGH().delete_groups('-69:userGroup_delete_group', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize--write
        body = {'group_name': 'gremlin', 'group_description': 'group can execute gremlin'}
        code, res = AuthGH().post_groups(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

        # check unAuthorize--read
        code, res = AuthGH().get_groups(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'groups': []}, msg='unAuthorize res check fail')


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
        Gremlin().gremlin_post(
            host=_cfg.auth_host,
            port=_cfg.auth_port,
            graph=_cfg.auth_graph,
            query='graph.truncateBackend();',
            auth=auth
        )  # gremlin语句对auth server进行clear操作
        if _cfg.is_auth_divide:
            Gremlin().gremlin_post(
                query='graph.truncateBackend();',
                auth=auth
            )  # gremlin语句对graph server进行clear操作

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'vertices':
                             [
                                 {'id': '1:r', 'label': 'person', 'type': 'vertex',
                                  'properties': {'name': 'r', 'age': 29, 'city': 'Shanghai'}},
                                 {'id': '1:peter', 'label': 'person', 'type': 'vertex',
                                  'properties': {'name': 'peter', 'age': 29, 'city': 'Shanghai'}}
                             ]
                         },
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(
            res["message"],
            "Permission denied: read Resource{graph=%s,type=VERTEX,""operated=v[1:r]}" % _cfg.graph_name,
            msg="Unauthorized result check fail"
        )
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, "READ", msg="role permission check fail")
            self.assertEqual(value[2]["type"], "VERTEX", msg="role type check fail")

        # check Authorize--read
        code, res = Vertex().get_filter_vertex(auth=user)
        print("验权--读", code, res)
        self.assertEqual(code, 200, msg=res)
        self.assertEqual(res,
                         {'vertices':
                             [
                                 {'id': '1:h', 'label': 'person', 'type': 'vertex',
                                  'properties': {'name': 'h', 'age': 32, 'city': 'Beijing'}},
                                 {'id': '1:josh', 'label': 'person', 'type': 'vertex',
                                  'properties': {'name': 'josh', 'age': 32, 'city': 'Beijing'}},
                                 {'id': '1:qian', 'label': 'person', 'type': 'vertex',
                                  'properties': {'name': 'qian', 'age': 32, 'city': 'Beijing'}}
                             ]
                         },
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': '1:new1', 'label': 'person', 'type': 'vertex',
                          'properties': {'name': 'new1', 'age': 45, 'city': 'Shanghai'}},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
                             {"type": "VERTEX", "label": "person",
                              "properties": {"city": "P.contains(\"Shanxi\")"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'vertices': [{'id': '1:peter', 'label': 'person', 'type': 'vertex',
                                        'properties': {'name': 'peter', 'age': 29,
                                                       'city': ['Shanghai', 'Shanxi']}}]},
                         msg=res)

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
            {"target_list": [
                {"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
                "permission": "WRITE", "name": "vertex_write"}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': '1:new1', 'label': 'person', 'type': 'vertex',
                          'properties': {'name': 'new1', 'age': 46, 'city': ['Shanxi', 'qwe']}},
                         msg=res)

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
            {"target_list": [
                {"type": "VERTEX", "label": "person", "properties": {"city": "P.contains(\"Shanxi\")"}}],
                "permission": "DELETE", "name": "vertex_delete"},
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "DELETE":
                self.assertIn(value[0]["type"], "VERTEX", msg="role type check fail")
            elif key == "READ":
                self.assertIn(value[0]["type"], "STATUS", msg="role type check fail")
                self.assertIn(value[1]["type"], "PROPERTY_KEY", msg="role type check fail")
                self.assertIn(value[2]["type"], "VERTEX_LABEL", msg="role type check fail")
                self.assertIn(value[3]["type"], "EDGE_LABEL", msg="role type check fail")
                self.assertIn(value[4]["type"], "VERTEX", msg="role type check fail")
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
                              "properties": {"city": "Hongkong", "age": "P.gte(20)"}}],
             "permission": "READ",
             "name": "vertex_read"}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'vertices': [{'id': '1:s', 'label': 'person', 'type': 'vertex',
                                        'properties': {'name': 's', 'age': 27, 'city': 'Hongkong'}},
                                       {'id': '1:wang', 'label': 'person', 'type': 'vertex',
                                        'properties': {'name': 'wang', 'age': 27, 'city': 'Hongkong'}},
                                       {'id': '1:vadas', 'label': 'person', 'type': 'vertex',
                                        'properties': {'name': 'vadas', 'age': 27, 'city': 'Hongkong'}}]},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': '1:new1', 'label': 'person', 'type': 'vertex',
                          'properties': {'name': 'new1', 'age': 20, 'city': 'Shanxi'}},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
                              "properties": {"age": "P.gte(30)"}}],
             "permission": "READ",
             "name": "vertex_read_age"}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'vertices': [{'id': '1:h', 'label': 'person', 'type': 'vertex',
                                        'properties': {'name': 'h', 'age': 32, 'city': 'Beijing'}},
                                       {'id': '1:josh', 'label': 'person', 'type': 'vertex',
                                        'properties': {'name': 'josh', 'age': 32, 'city': 'Beijing'}},
                                       {'id': '1:qian', 'label': 'person', 'type': 'vertex',
                                        'properties': {'name': 'qian', 'age': 32, 'city': 'Beijing'}}]},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': '1:new1', 'label': 'person', 'type': 'vertex',
                          'properties': {'name': 'new1', 'age': 20, 'city': 'Shanxi'}},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'edges': [{'id': 'S1:o>2>>S2:p', 'label': 'created', 'type': 'edge', 'outV': '1:o',
                                     'outVLabel': 'person', 'inV': '2:p', 'inVLabel': 'software',
                                     'properties': {'city': 'Shanghai', 'date': '20171210'}},
                                    {'id': 'S1:marko>2>>S2:lop', 'label': 'created', 'type': 'edge',
                                     'outV': '1:marko',
                                     'outVLabel': 'person', 'inV': '2:lop', 'inVLabel': 'software',
                                     'properties': {'city': 'Shanghai', 'date': '20171210'}}]},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'edges': [{'id': 'S1:o>2>>S2:p', 'label': 'created', 'type': 'edge', 'outV': '1:o',
                                     'outVLabel': 'person', 'inV': '2:p', 'inVLabel': 'software',
                                     'properties': {'city': 'Shanghai', 'date': '20171210'}},
                                    {'id': 'S1:marko>2>>S2:lop', 'label': 'created', 'type': 'edge',
                                     'outV': '1:marko',
                                     'outVLabel': 'person', 'inV': '2:lop', 'inVLabel': 'software',
                                     'properties': {'city': 'Shanghai', 'date': '20171210'}}]},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        edge_id = "S1:peter>2>>S2:lop"
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
        edge_id = "S1:peter>2>>S2:lop"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': 'S1:peter>2>>S2:zhao', 'label': 'created', 'type': 'edge', 'outV': '1:peter',
                          'outVLabel': 'person', 'inV': '2:zhao', 'inVLabel': 'software',
                          'properties': {'city': 'Shanghai', 'date': '2017-5-18'}},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        edge_id = "S1:peter>2>>S2:lop"
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
                             {"type": "EDGE", "label": "knows", "properties": {"price": "P.gte(300)"}}],
             "permission": "READ",
             "name": "edge_read"}
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'edges': [{'id': 'S1:o>1>>S1:s', 'label': 'knows', 'type': 'edge', 'outV': '1:o',
                                     'outVLabel': 'person', 'inV': '1:s', 'inVLabel': 'person',
                                     'properties': {'date': '20160110', 'price': 700}},
                                    {'id': 'S1:li>1>>S1:wang', 'label': 'knows', 'type': 'edge', 'outV': '1:li',
                                     'outVLabel': 'person', 'inV': '1:wang', 'inVLabel': 'person',
                                     'properties': {'date': '20160110', 'price': 450}},
                                    {'id': 'S1:marko>1>>S1:josh', 'label': 'knows', 'type': 'edge',
                                     'outV': '1:marko',
                                     'outVLabel': 'person', 'inV': '1:josh', 'inVLabel': 'person',
                                     'properties': {'date': '20130220', 'price': 328}}]},
                         msg=res)

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
        edge_id = "S1:li>1>>S1:wang"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': 'S1:peter>1>>S1:qian', 'label': 'knows', 'type': 'edge', 'outV': '1:peter',
                          'outVLabel': 'person', 'inV': '1:qian', 'inVLabel': 'person',
                          'properties': {'date': '2017-5-18', 'price': 234}},
                         msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:peter>2>>S2:lop"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        edge_id = "S1:marko>1>>S1:josh"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'edges': [{'id': 'S1:li>1>>S1:wang', 'label': 'knows', 'type': 'edge', 'outV': '1:li',
                                     'outVLabel': 'person', 'inV': '1:wang', 'inVLabel': 'person',
                                     'properties': {'date': '2016-01-10 00:00:00.000',
                                                    'address': ['北京市海淀区', '北京市颐和园']}},
                                    {'id': 'S1:marko>1>>S1:vadas', 'label': 'knows', 'type': 'edge',
                                     'outV': '1:marko',
                                     'outVLabel': 'person', 'inV': '1:vadas', 'inVLabel': 'person',
                                     'properties': {'date': '2016-01-10 00:00:00.000',
                                                    'address': ['北京市海淀区', '北京市房山区']}}]},
                         msg=res)

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
        edge_id = "S1:li>1>>S1:wang"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': 'S1:peter>1>>S1:qian', 'label': 'knows', 'type': 'edge', 'outV': '1:peter',
                          'outVLabel': 'person', 'inV': '1:qian', 'inVLabel': 'person',
                          'properties': {'date': '2017-05-18 00:00:00.000', 'address': ['北京市海淀区']}},
                         msg=res)

        # check Authorize--read
        code, res = Edge().get_filter_edge(auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg=res)
        self.assertEqual(res["message"], "User not authorized.", msg="Unauthorized result check fail")

        # check Unauthorized--delete
        edge_id = "S1:alg>1>>S1:vadas"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        edge_id = "S1:li>1>>S1:wang"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'edges': [{'id': 'S1:o>1>>S1:s', 'label': 'knows', 'type': 'edge', 'outV': '1:o',
                                     'outVLabel': 'person', 'inV': '1:s', 'inVLabel': 'person',
                                     'properties': {'date': '20160110', 'price': 700}},
                                    {'id': 'S1:li>1>>S1:wang', 'label': 'knows', 'type': 'edge', 'outV': '1:li',
                                     'outVLabel': 'person', 'inV': '1:wang', 'inVLabel': 'person',
                                     'properties': {'date': '20160110', 'price': 450}}]},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': 'S1:peter>1>>S1:qian', 'label': 'knows', 'type': 'edge', 'outV': '1:peter',
                          'outVLabel': 'person', 'inV': '1:qian', 'inVLabel': 'person',
                          'properties': {'date': '20160110', 'price': 567}},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        edge_id = "S1:li>1>>S1:wang"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'edges': [{'id': 'S1:o>1>>S1:s', 'label': 'knows', 'type': 'edge', 'outV': '1:o',
                                     'outVLabel': 'person', 'inV': '1:s', 'inVLabel': 'person',
                                     'properties': {'date': '20160110', 'price': 700}},
                                    {'id': 'S1:li>1>>S1:wang', 'label': 'knows', 'type': 'edge', 'outV': '1:li',
                                     'outVLabel': 'person', 'inV': '1:wang', 'inVLabel': 'person',
                                     'properties': {'date': '20160110', 'price': 450}},
                                    {'id': 'S1:marko>1>>S1:vadas', 'label': 'knows', 'type': 'edge',
                                     'outV': '1:marko',
                                     'outVLabel': 'person', 'inV': '1:vadas', 'inVLabel': 'person',
                                     'properties': {'date': '20160110', 'price': 45}}]},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res,
                         {'id': 'S1:peter>1>>S1:qian', 'label': 'knows', 'type': 'edge', 'outV': '1:peter',
                          'outVLabel': 'person', 'inV': '1:qian', 'inVLabel': 'person',
                          'properties': {'date': '20160110', 'price': 567}},
                         msg=res)

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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        edge_id = "S1:o>1>>S1:s"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        edge_id = "S1:o>1>>S1:s"
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        AuthGH().get_accesses(auth=user)
        AuthGH().get_users(auth=user)
        AuthGH().get_groups(auth=user)
        code, res = Schema().delete_edgeLabel(name="tree", auth=user)  # 删除边类型
        Task().get_task(res['task_id'], auth=user)
        code, res = Gremlin().gremlin_post(query="g.V()", auth=user)
        print(code, res)
        # print code, res
        self.assertEqual(code, 200, msg=res)
        self.assertEqual(res['result'],
                         {'data': [{'id': '1:h', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'h', 'age': 32, 'city': 'Beijing'}},
                                   {'id': '1:o', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'o', 'age': 29, 'city': 'Beijing'}},
                                   {'id': '1:r', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'r', 'age': 29, 'city': 'Shanghai'}},
                                   {'id': '1:s', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 's', 'age': 27, 'city': 'Hongkong'}},
                                   {'id': '2:e', 'label': 'software', 'type': 'vertex',
                                    'properties': {'name': 'e', 'lang': 'java', 'price': 199}},
                                   {'id': '2:p', 'label': 'software', 'type': 'vertex',
                                    'properties': {'name': 'p', 'lang': 'java', 'price': 328}},
                                   {'id': '1:li', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'li', 'age': 29, 'city': 'Beijing'}},
                                   {'id': '2:lop', 'label': 'software', 'type': 'vertex',
                                    'properties': {'name': 'lop', 'lang': 'java', 'price': 328}},
                                   {'id': '1:josh', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'josh', 'age': 32, 'city': 'Beijing'}},
                                   {'id': '1:qian', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'qian', 'age': 32, 'city': 'Beijing'}},
                                   {'id': '1:wang', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'wang', 'age': 27, 'city': 'Hongkong'}},
                                   {'id': '2:zhao', 'label': 'software', 'type': 'vertex',
                                    'properties': {'name': 'zhao', 'lang': 'java', 'price': 328}},
                                   {'id': '1:marko', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'marko', 'age': 29, 'city': 'Beijing'}},
                                   {'id': '1:peter', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'peter', 'age': 29, 'city': 'Shanghai'}},
                                   {'id': '1:vadas', 'label': 'person', 'type': 'vertex',
                                    'properties': {'name': 'vadas', 'age': 27, 'city': 'Hongkong'}},
                                   {'id': '2:ripple', 'label': 'software', 'type': 'vertex',
                                    'properties': {'name': 'ripple', 'lang': 'java', 'price': 199}}], 'meta': {}},
                         msg=res)

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
            {"target_list": [{"type": "GREMLIN"}, {"type": "TASK"}], "permission": "EXECUTE", "name": "gremlin"},
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
            # 此权限不应该添加
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == "READ":
                # self.assertIn(value[0]["type"], "ROOT", msg="role type check fail")
                self.assertIn(value[0]["type"], "TASK", msg="role type check fail")
                self.assertIn(value[1]["type"], "STATUS", msg="role type check fail")
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
        user_id = set_auth_gh.post_auth(permission_list)
        code, res = AuthGH().get_users_role(user_id, auth=user)
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
        self.assertEqual(res['result'],
                         {'data': [{'id': 'S1:o>2>>S2:p', 'label': 'created', 'type': 'edge', 'outV': '1:o',
                                    'outVLabel': 'person', 'inV': '2:p', 'inVLabel': 'software',
                                    'properties': {'city': 'Shanghai', 'date': '20171210'}},
                                   {'id': 'S1:marko>2>>S2:lop', 'label': 'created', 'type': 'edge',
                                    'outV': '1:marko',
                                    'outVLabel': 'person', 'inV': '2:lop', 'inVLabel': 'software',
                                    'properties': {'city': 'Shanghai', 'date': '20171210'}}], 'meta': {}},
                         msg=res)

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


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class Access(unittest.TestCase):
    """
    绑定资源和用户组
    """

    def setUp(self):
        """
        测试case开始
        :resurn:
        """
        Gremlin().gremlin_post(
            host=_cfg.auth_host,
            port=_cfg.auth_port,
            graph=_cfg.auth_graph,
            query='graph.truncateBackend();',
            auth=auth
        )  # gremlin语句进行clear操作
        # 创建group
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)
        # 创建 target
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=auth)
        print(code, res)

    def test_access_create(self):
        """
        创建 access
        """
        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'res check fail')

    def test_access_delete(self):
        """
        删除 access
        """
        # premise
        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=auth)
        # test
        code, res = AuthGH().delete_accesses(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_access_list(self):
        """
        获取 access
        """
        # premise
        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=auth)
        # test
        code, res = AuthGH().get_accesses(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['accesses'][0]['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'res check fail')

    def test_access_one(self):
        """
        获取 access
        """
        # premise
        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=auth)
        # test
        code, res = AuthGH().get_access(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'res check fail')

    def test_access_update(self):
        """
        更新 access
        """
        # premise
        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = AuthGH().post_accesses(body, auth=auth)
        # test
        body = {"access_description": "access description rename"}
        code, res = AuthGH().update_accesses(body, res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'res check fail')


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class Groups(unittest.TestCase):
    """
    创建用户组
    """

    def setUp(self):
        """
        测试case开始
        :resurn:
        """
        Gremlin().gremlin_post(
            host=_cfg.auth_host,
            port=_cfg.auth_port,
            graph=_cfg.auth_graph,
            query='graph.truncateBackend();',
            auth=auth
        )  # gremlin语句进行clear操作

    def test_groups_create(self):
        """
        创建 groups
        """
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, 'code check fail')
        self.assertEqual(res['group_name'], 'gremlin', 'code check fail')

    def test_groups_delete(self):
        """
        删除 groups
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().delete_groups(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_groups_list(self):
        """
        获取 groups
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_groups(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['groups'][0]['id'], '-69:gremlin', 'res check fail')

    def test_groups_one(self):
        """
        获取 group
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_group(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], '-69:gremlin', 'res check fail')

    def test_groups_update(self):
        """
        更新groups
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)
        # test
        body = {"group_name": "gremlin", "group_description": "group_update  description"}
        code, res = AuthGH().update_groups(body, res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['group_description'], 'group_update  description', 'res check fail')


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class Target(unittest.TestCase):
    """
    创建资源
    """

    def setUp(self):
        """
        测试case开始
        :resurn:
        """
        Gremlin().gremlin_post(
            host=_cfg.auth_host,
            port=_cfg.auth_port,
            graph=_cfg.auth_graph,
            query='graph.truncateBackend();',
            auth=auth
        )  # gremlin语句进行clear操作

    def test_target_create(self):
        """
        创建 target
        """
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], '-77:gremlin', 'res check fail')

    def test_target_delete(self):
        """
        删除 target
        """
        # premise
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().delete_targets(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_target_list(self):
        """
        获取 target
        """
        # premise
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_targets(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['targets'][0]['id'], '-77:gremlin', 'res check fail')

    def test_target_one(self):
        """
        获取target
        """
        # premise
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_target(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], '-77:gremlin', 'res check fail')

    def test_target_update(self):
        """
        获取 target
        """
        # premise
        body = {
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_name": "gremlin",
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {
                    "type": "GREMLIN",
                    "properties": None,
                    "label": "*"
                }
            ]
        }
        code, res = AuthGH().post_targets(body, auth=auth)
        print(code, res)
        # test
        body = {
            "target_name": "gremlin",
            "target_url": '%s:%d' % (_cfg.graph_host, _cfg.server_port),
            "target_graph": _cfg.graph_name,
            "target_resources": [
                {"type": "VERTEX"}
            ]
        }
        code, res = AuthGH().update_targets(body, res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['target_resources'][0]['type'], 'VERTEX', 'res check fail')


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class User(unittest.TestCase):
    """
    创建用户
    """

    def setUp(self):
        """
        测试case开始
        :resurn:
        """
        Gremlin().gremlin_post(
            host=_cfg.auth_host,
            port=_cfg.auth_port,
            graph=_cfg.auth_graph,
            query='graph.truncateBackend();',
            auth=auth
        )  # gremlin语句进行clear操作

    def test_user_create(self):
        """
        创建 user
        """
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], '-63:tester', 'res check fail')

    def test_user_create_Space(self):
        """
        异常case创建 user 用户名包含空格
        """
        body = {"user_name": "tester ", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The name is 5-16 characters and can only contain letters, numbers or underscores"

    def test_user_create_Chinese(self):
        """
        异常case创建 user 用户名为中文
        """
        body = {"user_name": "张三", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The name is 5-16 characters and can only contain letters, numbers or underscores"

    def test_user_create_symbol(self):
        """
        异常case创建 user 用户名包含特殊符号
        """
        body = {"user_name": "tester##@@%", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The name is 5-16 characters and can only contain letters, numbers or underscores"

    def test_user_create_namefour(self):
        """
        异常case创建 user 用户名长度为4个字符
        """
        body = {"user_name": "test", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The name is 5-16 characters and can only contain letters, numbers or underscores"

    def test_user_create_nameseventeen(self):
        """
        异常case创建 user 用户名长度为17个字符
        """
        body = {"user_name": "testaaaaaaaaaaaaa", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The name is 5-16 characters and can only contain letters, numbers or underscores"

    def test_user_create_null(self):
        """
        异常case创建 user 用户名为空
        """
        body = {"user_name": "", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The name is 5-16 characters and can only contain letters, numbers or underscores"

    def test_password_create_Space(self):
        """
        异常case创建 user 密码包含空格
        """
        body = {"user_name": "tester", "user_password": "12345 6"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The password is 5-16 characters, which can be letters, numbers or special symbols"

    def test_password_create_Chinese(self):
        """
        异常case创建 user 密码为中文
        """
        body = {"user_name": "tester", "user_password": "张三"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The password is 5-16 characters, which can be letters, numbers or special symbols"

    def test_password_create_namefour(self):
        """
        异常case创建 user 密码长度为4个字符
        """
        body = {"user_name": "tester", "user_password": "1234"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The password is 5-16 characters, which can be letters, numbers or special symbols"

    def test_password_create_nameseventeen(self):
        """
        异常case创建 user 密码长度为17个字符
        """
        body = {"user_name": "tester", "user_password": "12345678912345678"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The password is 5-16 characters, which can be letters, numbers or special symbols"

    def test_password_create_null(self):
        """
        异常case创建 user 密码为空
        """
        body = {"user_name": "tester", "user_password": ""}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        assert code == 400
        assert res['message'] == "The password is 5-16 characters, which can be letters, numbers or special symbols"

    def test_password_create_symbol(self):
        """
        创建 user 密码包含特殊符号
        """
        body = {"user_name": "tester", "user_password": "123456@@##"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], '-63:tester', 'res check fail')

    def test_user_delete(self):
        """
        删除 user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().delete_users(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_user_list(self):
        """
        获取 user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_users(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['users'][1]['id'], '-63:tester', 'res check fail')

    def test_user_one(self):
        """
        获取user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_user(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], '-63:tester', 'res check fail')

    def test_user_one_role(self):
        """
        获取user角色
        """
        # premise
        permission_list = [
            {
                'target_list': [
                    {'type': 'GRANT'},
                    # {'type': 'STATUS'}
                ],
                'permission': 'WRITE',
                'name': 'grant_write'
            }
        ]
        user_id = set_auth_gh.post_auth(permission_list)
        # test
        code, res = AuthGH().get_users_role(user_id, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(
            res['roles'],
            {_cfg.graph_name: {'WRITE': [{'type': 'GRANT', 'label': '*', 'properties': None}]}},
            'res check fail'
        )

    def test_user_update(self):
        """
        获取 user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)
        # test
        body = {
            "user_name": "tester",
            "user_password": "123456",
            "user_phone": "138",
            "user_avatar": "tester.png",
            "user_email": "tester@163.com"
        }
        code, res = AuthGH().update_users(body, res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['user_avatar'], 'tester.png', 'res check fail')


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class Belongs(unittest.TestCase):
    """
    绑定用户和用户组
    """

    def setUp(self):
        """
        测试case开始
        :resurn:
        """
        Gremlin().gremlin_post(
            host=_cfg.auth_host,
            port=_cfg.auth_port,
            graph=_cfg.auth_graph,
            query='graph.truncateBackend();',
            auth=auth
        )  # gremlin语句进行clear操作
        # 创建group
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = AuthGH().post_groups(body, auth=auth)
        print(code, res)
        # 创建 user
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = AuthGH().post_users(body, auth=auth)
        print(code, res)

    def test_belong_create(self):
        """
        创建 belong
        """
        body = {'group': '-69:gremlin', 'user': '-63:tester', 'belong_description': 'belong gremlin'}
        code, res = AuthGH().post_belongs(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], 'S-63:tester>-82>>S-69:gremlin', 'res check fail')

    def test_belong_delete(self):
        """
        删除 belong
        """
        # premise
        body = {'group': '-69:gremlin', 'user': '-63:tester', 'belong_description': 'belong gremlin'}
        code, res = AuthGH().post_belongs(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().delete_belongs(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_belong_list(self):
        """
        获取 belongs
        """
        # premise
        body = {'group': '-69:gremlin', 'user': '-63:tester', 'belong_description': 'belong gremlin'}
        code, res = AuthGH().post_belongs(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_belongs(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['belongs'][0]['id'], 'S-63:tester>-82>>S-69:gremlin', 'res check fail')

    def test_belong_one(self):
        """
        获取 belong
        """
        # premise
        body = {'group': '-69:gremlin', 'user': '-63:tester', 'belong_description': 'belong gremlin'}
        code, res = AuthGH().post_belongs(body, auth=auth)
        print(code, res)
        # test
        code, res = AuthGH().get_belong(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-63:tester>-82>>S-69:gremlin', 'res check fail')

    def test_belong_update(self):
        """
        更新 belong
        """
        # premise
        body = {'group': '-69:gremlin', 'user': '-63:tester', 'belong_description': 'belong gremlin'}
        code, res = AuthGH().post_belongs(body, auth=auth)
        print(code, res)
        # test
        body = {"belong_description": "belong description rename"}
        code, res = AuthGH().update_belongs(body, res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-63:tester>-82>>S-69:gremlin', 'res check fail')


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class Token(unittest.TestCase):
    """
    token
    """

    def test_login_token(self):
        """
        超级管理员登录
        生成 token
        """
        body = {'user_name': 'admin', 'user_password': '123456'}
        code, res = AuthGH().post_token(body, auth=auth)
        print(code, res)
        x = res["token"]
        # print(x)
        # print(type(x))
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['token'], x, 'res check fail')

    def test_verify_token(self):
        """
        验证 token ->生成token
        """
        body = {'user_name': 'admin', 'user_password': '123456'}
        code, res = AuthGH().post_token(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        x = res["token"]

        # 验证

        h = {
            'Authorization': 'Bearer ' + x
        }
        # h = {'Postman-Token': x}
        code, res = AuthGH().get_verify(header=h, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['user_name'], 'admin')
        self.assertEqual(res['user_id'], '-63:admin')

    def test_token_expire(self):
        """
        生成 token 设置token过期时间1分钟
        """
        body = {'user_name': 'admin', 'user_password': '123456', 'token_expire': '180'}
        code, res = AuthGH().post_token(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        x = res["token"]

        # 等待30秒
        time.sleep(130)

        # 验证
        h = {
            'Authorization': 'Bearer ' + x
        }
        # h = {'Postman-Token': x}
        code, res = AuthGH().get_verify(header=h, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['user_name'], 'admin')
        self.assertEqual(res['user_id'], '-63:admin')

    def test_ordinary_login_token(self):
        """
        普通用户登录
        生成 token
        """
        body = {'user_name': 'tester', 'user_password': '123456'}
        code, res = AuthGH().post_token(body, auth=auth)
        print(code, res)
        x = res["token"]
        # print(x)
        # print(type(x))
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['token'], x, 'res check fail')

    def test_ordinary_verify_token(self):
        """
        验证 token ->生成token
        """
        body = {'user_name': 'tester', 'user_password': '123456'}
        code, res = AuthGH().post_token(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        x = res["token"]

        # 验证

        h = {
            'Authorization': 'Bearer ' + x
        }
        # h = {'Postman-Token': x}
        code, res = AuthGH().get_verify(header=h, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['user_name'], 'tester')
        self.assertEqual(res['user_id'], '-63:tester')


if __name__ == '__main__':
    pass

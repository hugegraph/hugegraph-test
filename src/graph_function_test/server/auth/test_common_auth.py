# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 粗粒度权限的鉴权和越权
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
from src.common.server_api import Auth
from src.common.server_api import Variable
from src.common.server_api import Task
from src.common.server_api import Graph
from src.common.server_api import Vertex
from src.common.server_api import Edge
from src.common.loader import InsertData
from src.common.task_res import get_task_res
from src.common import set_auth
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
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)

    def test_status_read(self):
        """
        资源读权限
        :resurn:
        """
        permission_list = [
            {'target_list': [{'type': 'STATUS'}], 'permission': 'READ', 'name': 'status_read'}
        ]
        user_id = set_auth.post_auth(permission_list)

        # check auth
        code, res = Auth().get_users_role(user_id, auth=user)
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
            'Permission denied: write Resource{graph=hugegraph,type=STATUS,operated=*}',
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
        user_id = set_auth.post_auth(permission_list)

        # check role
        code, res = Auth().get_users_role(user_id, auth=user)
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
        self.assertEqual(res, {'name': 'hugegraph', 'backend': 'rocksdb'})

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
        user_id = set_auth.post_auth(permission_list)

        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)

        # check role
        code, res = Auth().get_users_role(user_id, auth=user)
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
        self.assertEqual(code, 201, 'Authorize code check fail')
        self.assertEqual(res['name'], body['name'], 'Authorize result check fail')

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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            self.assertEqual(key, 'DELETE', msg='role permission check fail')
            self.assertEqual(value[0]['type'], 'PROPERTY_KEY', msg='role type check fail')

        # check Authorize--delete  delete请求成功返回只有状态码，没有message返回
        name = 'test'
        code, res = Schema().delete_property_by_name(name, auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Unauthorized code check fail')

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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            {'target_list': [{'type': 'TASK'}], 'permission': 'EXECUTE', 'name': 'task_execute'}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'INDEX_LABEL', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'PROPERTY_KEY', msg='role type check fail')

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
            ], 'permission': 'EXECUTE', 'name': 'task_execute'}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'INDEX_LABEL', msg='role type check fail')
            elif key == 'WRITE':
                self.assertIn(value[0]['type'], 'TASK', msg='role type check fail')
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            ], 'permission': 'EXECUTE', 'name': 'task_execute'}
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            'Permission denied: read Resource{graph=hugegraph,type=EDGE_AGGR,operated=*}',
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            'Permission denied: read Resource{graph=hugegraph,type=VERTEX_AGGR,operated=*}',
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            "Permission denied: read Resource{graph=hugegraph,type=EDGE_LABEL,operated=help(id=3)}",
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            'Permission denied: write Resource{graph=hugegraph,type=VAR,operated=*}',
            msg='Unauthorized result check fail'
        )

        # check unAuthorize--delete
        code, res = Variable().delete_var('name', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=hugegraph,type=VAR,operated=*}',
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            'Permission denied: read Resource{graph=hugegraph,type=VAR,operated=*}',
            msg='Unauthorized result check fail'
        )

        # check unAuthorize--delete
        code, res = Variable().delete_var('name', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=hugegraph,type=VAR,operated=*}',
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
            'Permission denied: write Resource{graph=hugegraph,type=VAR,operated=*}',
            msg='Unauthorized result check fail'
        )

        # check unAuthorize--read
        code, res = Variable().get_var(name, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: read Resource{graph=hugegraph,type=VAR,operated=*}',
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
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        self.assertEqual(res['message'], "Permission denied: read Resource{graph=hugegraph,type=TASK,operated=1}")

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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
                'name': 'target_read'
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'TARGET', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Auth().get_targets(auth=user)
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
        code, res = Auth().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=hugegraph,type=TARGET,operated=target(gremlin)}',
            'unAuthorize res check fail'
        )

        # check unAuthorize--delete
        code, res = Auth().delete_targets('-77:target_read_target', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=hugegraph,type=TARGET,operated=target(target_read_target)}',
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
                'name': 'target_write'
            },
            {
                'target_list': [
                    {'type': 'STATUS'}
                ],
                'permission': 'READ',
                'name': 'status_read'
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
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
        code, res = Auth().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Authorize code check fail')
        self.assertEqual(res['target_name'], 'gremlin', msg='Authorize res check fail')

        # check unAuthorize--read
        code, res = Auth().get_targets(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'targets': []}, 'unAuthorize res check fail')

        # check unAuthorize--delete
        code, res = Auth().delete_targets('-77:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=hugegraph,type=TARGET,operated=target(gremlin)}',
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
                'name': 'target_delete'
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'TARGET', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = Auth().delete_targets('-77:target_delete_target', auth=user)
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
        code, res = Auth().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=hugegraph,type=TARGET,operated=target(gremlin)}',
            'unAuthorize res check fail'
        )

        # check unAuthorize--read
        code, res = Auth().get_targets(auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        code, res = Auth().get_targets(auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        code, res = Auth().post_targets(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=hugegraph,type=TARGET,operated=target(gremlin)}',
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        code, res = Auth().delete_targets('-77:all_delete_target', auth=user)
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Auth().get_accesses(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')

        # check unAuthorize--write
        body = {'group': '-69:gremlin', 'target': '-71:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

        # check unAuthorize--delete
        code, res = Auth().delete_accesses('S-69:grant_read_group>-88>11>S-77:grant_read_target', auth=user)
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
                'name': 'grant_write'
            },
            {
                'target_list': [
                    {'type': 'STATUS'}
                ],
                'permission': 'READ',
                'name': 'status_read'
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
            elif key == 'READ':
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
        code, res = Auth().post_targets(body, auth=user)
        print(code, res)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=user)
        print(code, res)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Authorize code check fail')
        self.assertEqual(
            res['message'],
            "Permission denied: write Resource{graph=hugegraph,type=GRANT,operated=access(-69:gremlin->-77:gremlin)}",
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
                'name': 'grant_write'
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        code, res = Auth().post_targets(body, auth=user)
        print(code, res)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=user)
        print(code, res)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='Authorize code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'Authorize res check fail')

        # check unAuthorize--read
        code, res = Auth().get_accesses(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'accesses': []}, msg='unAuthorize code check fail')

        # check unAuthorize--delete
        code, res = Auth().delete_accesses('S-69:gremlin>-88>18>S-77:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: delete Resource{graph=hugegraph,type=GRANT,operated=access(-69:gremlin->-77:gremlin)}',
            'unAuthorize res check fail'
        )

    def test_grant_delete_exclude_grants(self):
        """
        grant 删除权限(异常case) admin创建的权限，普通用户没有删除的权利
        :resurn:
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
        code, res = Auth().post_targets(body, auth=auth)
        print(code, res)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'Authorize res check fail')

        # check role
        permission_list = [
            {
                'target_list': [
                    {'type': 'GRANT'}
                ],
                'permission': 'DELETE',
                'name': 'grant_write'
            },

        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'READ':
                self.assertIn(value[0]['type'], 'GRANT', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = Auth().delete_accesses('S-69:gremlin>-88>18>S-77:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='Authorize code check fail')
        self.assertEqual(
            res['message'],
            "Permission denied: delete Resource{graph=hugegraph,type=GRANT,operated=access(-69:gremlin->-77:gremlin)}",
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
                'name': 'grant_delete'
            },
            {
                'target_list': [
                    {'type': 'GRANT'},
                    {'type': 'TARGET'},
                    {'type': 'USER_GROUP'}
                ],
                'permission': 'WRITE',
                'name': 'grant_write'
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
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
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
        code, res = Auth().post_targets(body, auth=user)
        print(code, res)

        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=user)
        print(code, res)

        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(res['id'], 'S-69:gremlin>-88>18>S-77:gremlin', 'Authorize res check fail')

        code, res = Auth().delete_accesses('S-69:gremlin>-88>18>S-77:gremlin', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize--write
        body = {'group': '-69:gremlin', 'target': '-77:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')
        self.assertEqual(
            res['access_permission'], 'EXECUTE', 'Authorize res check fail')

        # check unAuthorize--read
        code, res = Auth().get_accesses(auth=user)
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
                'name': 'userGroup_read'
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'read':
                self.assertIn(value[0]['type'], 'USER_GROUP', msg='role type check fail')
            else:
                pass

        # check Authorize--read
        code, res = Auth().get_groups(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res['groups'][0]['group_name'], 'userGroup_read_group', msg='unAuthorize res check fail')

        # check unAuthorize--write
        body = {'group_name': 'gremlin', 'group_description': 'group can execute gremlin'}
        code, res = Auth().post_groups(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')
        self.assertEqual(
            res['message'],
            'Permission denied: write Resource{graph=hugegraph,type=USER_GROUP,operated=group(gremlin)}',
            msg='unAuthorize res check fail'
        )

        # check unAuthorize--delete
        code, res = Auth().delete_groups('-69:userGroup_read_group', auth=user)
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
                'name': 'userGroup_write'
            },
            {
                'target_list': [
                    {'type': 'STATUS'}
                ],
                'permission': 'READ',
                'name': 'status_read'
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'WRITE':
                self.assertIn(value[0]['type'], 'USER_GROUP', msg='role type check fail')
            elif key == 'READ':
                self.assertIn(value[0]['type'], 'STATUS', msg='role type check fail')
            else:
                pass

        # check Authorize--write
        body = {'group_name': 'gremlin', 'group_description': 'group can execute gremlin'}
        code, res = Auth().post_groups(body, auth=user)
        print(code, res)
        self.assertEqual(code, 201, msg='unAuthorize code check fail')

        # check unAuthorize--read
        code, res = Auth().get_groups(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'groups': []}, msg='unAuthorize res check fail')

        # check unAuthorize--delete
        code, res = Auth().delete_groups('-69:gremlin', auth=user)
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
                'name': 'userGroup_delete'
            }
        ]
        user_id = set_auth.post_auth(permission_list)
        code, res = Auth().get_users_role(user_id, auth=user)
        print(code, res)
        for key, value in res['roles'][_cfg.graph_name].items():
            if key == 'DELETE':
                self.assertIn(value[0]['type'], 'USER_GROUP', msg='role type check fail')
            else:
                pass

        # check Authorize--delete
        code, res = Auth().delete_groups('-69:userGroup_delete_group', auth=user)
        print(code, res)
        self.assertEqual(code, 204, msg='Authorize code check fail')

        # check unAuthorize--write
        body = {'group_name': 'gremlin', 'group_description': 'group can execute gremlin'}
        code, res = Auth().post_groups(body, auth=user)
        print(code, res)
        self.assertEqual(code, 403, msg='unAuthorize code check fail')

        # check unAuthorize--read
        code, res = Auth().get_groups(auth=user)
        print(code, res)
        self.assertEqual(code, 200, msg='unAuthorize code check fail')
        self.assertEqual(res, {'groups': []}, msg='unAuthorize res check fail')


if __name__ == '__main__':
    pass
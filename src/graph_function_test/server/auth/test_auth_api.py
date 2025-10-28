# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 设置用户的多种权限
create_time: 2020/4/22 5:17 下午
"""
import pytest
import sys
import os
import unittest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common import set_auth
from src.common.server_api import Auth
from src.common.server_api import Gremlin
from src.config import basic_config as _cfg

auth = None
user = None
if _cfg.is_auth:
    auth = _cfg.admin_password
    user = _cfg.test_password


@pytest.mark.skipif(_cfg.is_auth is False, reason='hugegraph启动时没有配置权限')
class Access(unittest.TestCase):
    """
    绑定资源和用户组
    """

    group_id = None
    target_id = None

    def setUp(self):
        """
        测试case开始
        :resurn:
        """
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # gremlin语句进行clear操作
        # 创建group
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)
        self.group_id = res.get('id', None)
        assert self.group_id is not None
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
        code, res = Auth().post_targets(body, auth=auth)
        print(code, res)
        self.target_id = res.get('id')
        assert self.target_id is not None

    def test_access_create(self):
        """
        创建 access
        """
        body = {'group': self.group_id, 'target': self.target_id, 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], 'S-36:gremlin>-55>-55>18>S-44:gremlin', 'res check fail')

    def test_access_delete(self):
        """
        删除 access
        """
        # premise
        body = {'group': '-36:gremlin', 'target': '-44:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=auth)
        # test
        code, res = Auth().delete_accesses(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_access_list(self):
        """
        获取 access
        """
        # premise
        body = {'group': '-36:gremlin', 'target': '-44:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=auth)
        # test
        code, res = Auth().get_accesses(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['accesses'][0]['id'], 'S-36:gremlin>-55>-55>18>S-44:gremlin', 'res check fail')

    def test_access_one(self):
        """
        获取 access
        """
        # premise
        body = {'group': '-36:gremlin', 'target': '-44:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=auth)
        # test
        code, res = Auth().get_access(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-36:gremlin>-55>-55>18>S-44:gremlin', 'res check fail')

    def test_access_update(self):
        """
        更新 access
        """
        # premise
        body = {'group': '-36:gremlin', 'target': '-44:gremlin', 'access_permission': 'EXECUTE'}
        code, res = Auth().post_accesses(body, auth=auth)
        # test
        body = {"access_description": "access description rename"}
        code, res = Auth().update_accesses(body, res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-36:gremlin>-55>-55>18>S-44:gremlin', 'res check fail')


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
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # gremlin语句进行clear操作

    def test_groups_create(self):
        """
        创建 groups
        """
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, 'code check fail')
        self.assertEqual(res['group_name'], 'gremlin', 'code check fail')

    def test_groups_delete(self):
        """
        删除 groups
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().delete_groups(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_groups_list(self):
        """
        获取 groups
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_groups(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['groups'][0]['id'], '-36:gremlin', 'res check fail')

    def test_groups_one(self):
        """
        获取 group
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_group(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], '-36:gremlin', 'res check fail')

    def test_groups_update(self):
        """
        更新groups
        """
        # premise
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)
        # test
        body = {"group_name": "gremlin", "group_description": "group_update  description"}
        code, res = Auth().update_groups(body, res['id'], auth=auth)
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
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # gremlin语句进行clear操作

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
        code, res = Auth().post_targets(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], '-44:gremlin', 'res check fail')

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
        code, res = Auth().post_targets(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().delete_targets(res['id'], auth=auth)
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
        code, res = Auth().post_targets(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_targets(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['targets'][0]['id'], '-44:gremlin', 'res check fail')

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
        code, res = Auth().post_targets(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_target(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], '-44:gremlin', 'res check fail')

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
        code, res = Auth().post_targets(body, auth=auth)
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
        code, res = Auth().update_targets(body, res['id'], auth=auth)
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
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # gremlin语句进行clear操作

    def test_user_create(self):
        """
        创建 user
        """
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = Auth().post_users(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], '-30:tester', 'res check fail')

    def test_user_delete(self):
        """
        删除 user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = Auth().post_users(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().delete_users(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_user_list(self):
        """
        获取 user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = Auth().post_users(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_users(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['users'][1]['id'], '-30:tester', 'res check fail')

    def test_user_one(self):
        """
        获取user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = Auth().post_users(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_user(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], '-30:tester', 'res check fail')

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
        user_id = set_auth.post_auth(permission_list)
        # test
        code, res = Auth().get_users_role(user_id, auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(
            res['roles'],
            {'hugegraph': {'WRITE': [{'type': 'GRANT', 'label': '*', 'properties': None}]}},
            'res check fail'
        )

    def test_user_update(self):
        """
        获取 user
        """
        # premise
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = Auth().post_users(body, auth=auth)
        print(code, res)
        # test
        body = {
            "user_name": "tester",
            "user_password": "123456",
            "user_phone": "138",
            "user_avatar": "tester.png",
            "user_email": "tester@163.com"
        }
        code, res = Auth().update_users(body, res['id'], auth=auth)
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
        Gremlin().gremlin_post('graph.truncateBackend();', auth=auth)  # gremlin语句进行clear操作
        # 创建group
        body = {"group_name": "gremlin", "group_description": "group can execute gremlin"}
        code, res = Auth().post_groups(body, auth=auth)
        print(code, res)
        # 创建 user
        body = {"user_name": "tester", "user_password": "123456"}
        code, res = Auth().post_users(body, auth=auth)
        print(code, res)

    def test_belong_create(self):
        """
        创建 belong
        """
        body = {'group': '-36:gremlin', 'user': '-30:tester', 'belong_description': 'belong gremlin'}
        code, res = Auth().post_belongs(body, auth=auth)
        print(code, res)
        self.assertEqual(code, 201, msg='code check fail')
        self.assertEqual(res['id'], 'S-30:tester>-49>-49>>S-36:gremlin', 'res check fail')

    def test_belong_delete(self):
        """
        删除 belong
        """
        # premise
        body = {'group': '-36:gremlin', 'user': '-30:tester', 'belong_description': 'belong gremlin'}
        code, res = Auth().post_belongs(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().delete_belongs(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 204, msg='code check fail')

    def test_belong_list(self):
        """
        获取 belongs
        """
        # premise
        body = {'group': '-36:gremlin', 'user': '-30:tester', 'belong_description': 'belong gremlin'}
        code, res = Auth().post_belongs(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_belongs(auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['belongs'][0]['id'], 'S-30:tester>-49>-49>>S-36:gremlin', 'res check fail')

    def test_belong_one(self):
        """
        获取 belong
        """
        # premise
        body = {'group': '-36:gremlin', 'user': '-30:tester', 'belong_description': 'belong gremlin'}
        code, res = Auth().post_belongs(body, auth=auth)
        print(code, res)
        # test
        code, res = Auth().get_belong(res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-30:tester>-49>-49>>S-36:gremlin', 'res check fail')

    def test_belong_update(self):
        """
        更新 belong
        """
        # premise
        body = {'group': '-36:gremlin', 'user': '-30:tester', 'belong_description': 'belong gremlin'}
        code, res = Auth().post_belongs(body, auth=auth)
        print(code, res)
        # test
        body = {"belong_description": "belong description rename"}
        code, res = Auth().update_belongs(body, res['id'], auth=auth)
        print(code, res)
        self.assertEqual(code, 200, msg='code check fail')
        self.assertEqual(res['id'], 'S-30:tester>-49>-49>>S-36:gremlin', 'res check fail')


if __name__ == '__main__':
    pass

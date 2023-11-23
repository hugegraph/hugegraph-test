# -*- coding:utf-8 -*-
"""
author     : lxb
note       : auth 接口测试
create_time: 2020/4/22 5:17 下午
"""
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../..')

from src.config import basic_config as _cfg
from src.common.server_api import AuthGH, AuthGHV3

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class AuthBody(object):
    """
    权限公共方法
    """

    def __init__(self):
        """初始化"""
        self.auth = AuthGH()
        self.target_graph = _cfg.graph_name
        self.target_url = _cfg.graph_host + ":" + str(_cfg.server_port)
        self.auth_user = "tester"
        self.auth_password = _cfg.test_password['tester']

    def create_target(self, target_list, name, graph=None):
        """
        创建资源
        """
        if graph is None:
            graph = self.target_graph
        body = {
            "target_name": name + "_target",
            "target_graph": graph,
            "target_url": self.target_url,
            "target_resources": target_list
        }
        status, res = self.auth.post_targets(body=body, auth=auth)
        # print(status, res)
        return res["id"]

    def create_group(self, name):
        """创建组"""
        body = {
            "group_name": name + "_group",
            "group_description": "%s graph_test" % (name + "_group")
        }
        status, res = self.auth.post_groups(body, auth=auth)
        # print(status, res)
        return res["id"]

    def create_access(self, group, target, premission):
        """创建group到target的连接"""
        body = {
            "group": group,
            "target": target,
            "access_permission": premission
        }
        status, res = self.auth.post_accesses(body, auth=auth)
        # print(status, res)
        return res["id"]

    def create_user(self):
        """创建用户user"""
        user_id = ''
        status, res = self.auth.get_users(auth=auth)
        for user in res['users']:
            if user['user_name'] == self.auth_user:
                user_id = user['id']
            else:
                pass
        if user_id == '':
            body = {
                "user_name": self.auth_user,
                "user_password": self.auth_password,
            }
            status, res = self.auth.post_users(body, auth=auth)
            user_id = res['id']
        return user_id

    def create_belong(self, user, group):
        """创建用户的授权"""
        body = {
            "user": user,
            "group": group,
        }
        status, res = self.auth.post_belongs(body, auth=auth)
        # print(status, res)

    def create_auth(self, type_list, permission, target_name="target_name",
                    groupname="group_test", name="test001", pw="123456"):
        """创建一个用户，并为其指定权限"""
        target_id = self.create_target(type_list, target_name)
        group_id = self.create_group(groupname)
        access_id = self.create_access(group_id, target_id, permission)
        user_id = self.create_user()
        self.create_belong(user_id, group_id)
        return user_id


def post_auth(auth_list):
    """
    处理请求参数 - 给用户赋权
    :param auth_list:
    """
    auth_body = AuthBody()
    ### 创建用户并获取用户id
    user_id = auth_body.create_user()
    for each in auth_list:
        ### 创建target并获取target_id
        target_name = each["name"]
        target_resources = each["target_list"]
        if "graph_name" in each:
            graph_name = each['graph_name']
        else:
            graph_name = None
        target_id = auth_body.create_target(target_resources, target_name, graph=graph_name)
        ### 创建group 并获取group_id
        group_id = auth_body.create_group(each["name"])
        ### 创建 access
        access_id = auth_body.create_access(group_id, target_id, each["permission"])
        ### 创建 belong
        auth_body.create_belong(user_id, group_id)
    return user_id


class AuthBodyV3(object):
    """
    权限公共方法
    """

    def __init__(self):
        """初始化"""
        self.auth = AuthGHV3()
        self.target_graph = _cfg.graph_name
        self.target_url = _cfg.graph_host + ":" + str(_cfg.server_port)
        self.auth_user = "tester"
        self.auth_password = _cfg.test_password['tester']

    def create_target(self, target_list, name, graph=None):
        """
        创建资源
        """
        if graph is None:
            graph = self.target_graph
        body = {
            "target_name": name + "_target",
            "target_graph": graph,
            "target_resources": target_list
        }
        print(body)
        status, res = self.auth.post_targets(body=body, auth=auth)
        print(status, res)
        return res["id"]

    def create_group(self, name):
        """创建组"""
        body = {
            "group_name": name + "_group",
            "group_description": "%s graph_test" % (name + "_group")
        }
        status, res = self.auth.post_groups(body, auth=auth)
        # print(status, res)
        return res["id"]

    def create_access(self, group, target, premission):
        """创建group到target的连接"""
        body = {
            "group": group,
            "target": target,
            "access_permission": premission
        }
        status, res = self.auth.post_accesses(body, auth=auth)
        return res["id"]

    def create_user(self):
        """创建用户user"""
        user_id = ''
        status, res = self.auth.get_users(auth=auth)
        for user in res['users']:
            if user['user_name'] == self.auth_user:
                user_id = user['id']
            else:
                pass
        if user_id == '':
            body = {
                "user_name": self.auth_user,
                "user_password": self.auth_password,
            }
            status, res = self.auth.post_users(body, auth=auth)
            user_id = res['id']
        return user_id

    def create_belong(self, user, group):
        """创建用户的授权"""
        body = {
            "user": user,
            "group": group,
        }
        status, res = self.auth.post_belongs(body, auth=auth)
        # print(status, res)

    def create_auth(self, type_list, permission, target_name="target_name",
                    groupname="group_test", name="test001", pw="123456"):
        """创建一个用户，并为其指定权限"""
        target_id = self.create_target(type_list, target_name)
        group_id = self.create_group(groupname)
        access_id = self.create_access(group_id, target_id, permission)
        user_id = self.create_user()
        self.create_belong(user_id, group_id)
        return user_id


def post_auth_v3(auth_list):
    """
    处理请求参数 - 给用户赋权
    :param auth_list:
    """
    auth_body = AuthBodyV3()
    ### 创建用户并获取用户id
    user_id = auth_body.create_user()
    print(user_id)
    for each in auth_list:
        ### 创建target并获取target_id
        target_name = each["name"]
        target_resources = each["target_list"]
        if "graph_name" in each:
            graph_name = each['graph_name']
        else:
            graph_name = None
        target_id = auth_body.create_target(target_resources, target_name, graph=graph_name)
        print(target_id)
        ### 创建group 并获取group_id
        group_id = auth_body.create_group(each["name"])
        ### 创建 access
        access_id = auth_body.create_access(group_id, target_id, each["permission"])
        ### 创建 belong
        auth_body.create_belong(user_id, group_id)
    return user_id


def clear_auth():
    """
    清空权限
    :return:
    """
    # 获取所有用户 并 删除用户
    code, res = AuthGHV3().get_users(auth=_cfg.admin_password)
    assert code == 200
    for user in res['users']:
        user_id = user['id']
        if user_id != 'admin':
            code, res = AuthGHV3().delete_users(user_id, auth=_cfg.admin_password)
            assert code == 204
            # print("{user:%s} is deleted " % user_id)
    # 获取所有target 并 删除target
    code, res = AuthGHV3().get_targets(auth=_cfg.admin_password)
    assert code == 200
    for target in res['targets']:
        target_id = target["id"]
        code, res = AuthGHV3().delete_targets(target_id, auth=_cfg.admin_password)
        assert code == 204
        # print("{target:%s} is deleted " % target_id)
    # 获取所有group 并 删除group
    code, res = AuthGHV3().get_groups(auth=_cfg.admin_password)
    assert code == 200
    for group in res['groups']:
        group_id = group["id"]
        code, res = AuthGHV3().delete_groups(group_id, auth=_cfg.admin_password)
        assert code == 204
        # print("{group:%s} is deleted " % group_id)


if __name__ == '__main__':
    clear_auth()

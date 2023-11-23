# -*- coding:utf-8 -*-
"""
author  : lxb
note    : test_graphspace
time    : 2022/5/19 下午4:32
"""
import os
import sys
import json

from src.common.server_api import GraphSpace

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = {"admin": "admin"}

graph_space_name = "gs_tmp"


class TestGraphSpace:
    """
    测试图空间
    """
    def teardown(self):
        """
        :return:
        """
        code, res = GraphSpace().delete_graph_space(space=graph_space_name, auth=auth)
        assert code == 204

    def test_create_graphspace_auth(self):
        """
        创建图空间
        :return:
        """
        body = {
          "name": graph_space_name,
          "description": "graph space test",
          "cpu_limit": 100,
          "memory_limit": 100,
          "compute_cpu_limit": 100,
          "compute_memory_limit": 100,
          "storage_limit": 100,
          "oltp_namespace": "hgser",
          "olap_namespace": "hgcp",
          "operator_image_path": _cfg.operator_image_path,
          "internal_algorithm_image_url": _cfg.internal_algorithm_image_url,
          "storage_namespace": "storage",
          "max_graph_number": 50,
          "max_role_number": 10,
          "auth": True,
          "configs": {}
        }
        code, res = GraphSpace().create_graph_space(body=body, auth=auth)
        print(code, res)
        assert code == 201

    def test_create_graphspace_no_auth(self):
        """
        创建图空间
        :return:
        """
        body = {
          "name": graph_space_name,
          "description": "graph space test",
          "cpu_limit": 100,
          "memory_limit": 100,
          "compute_cpu_limit": 100,
          "compute_memory_limit": 100,
          "storage_limit": 100,
          "oltp_namespace": "hgser",
          "olap_namespace": "hgcp",
          "operator_image_path": _cfg.operator_image_path,
          "internal_algorithm_image_url": _cfg.internal_algorithm_image_url,
          "storage_namespace": "storage",
          "max_graph_number": 50,
          "max_role_number": 10,
          "auth": False,
          "configs": {}
        }
        code, res = GraphSpace().create_graph_space(body=body, auth=auth)
        print(code, res)
        assert code == 201

    def test_get_graphspace(self):
        """
        查询图空间
        :return:
        """
        code, res = GraphSpace().get_graph_spaces(auth=auth)
        print(code, res)
        assert code == 200

    def test_get_one_graphspace(self):
        """
        查询图空间
        :return:
        """
        code, res = GraphSpace().get_one_graph_space(auth=auth)
        print(code, res)
        assert code == 200

    def test__update_graphspace(self):
        """
        查询图空间
        :return:
        """
        body = {
            "name": graph_space_name,
            "description": "graph space test",
            "cpu_limit": 100,
            "memory_limit": 100,
            "compute_cpu_limit": 100,
            "compute_memory_limit": 100,
            "storage_limit": 100,
            "oltp_namespace": "hgser",
            "olap_namespace": "hgcp",
            "operator_image_path": _cfg.operator_image_path,
            "internal_algorithm_image_url": _cfg.internal_algorithm_image_url,
            "storage_namespace": "storage",
            "max_graph_number": 50,
            "max_role_number": 10,
            "auth": False,
            "configs": {}
        }
        code, res = GraphSpace().create_graph_space(body=body, auth=auth)
        print(code, res)
        assert code == 201

        update_body = {
            "action": "update",
            "update": {
                "name": graph_space_name,
                "description": "update graph space",
                "cpu_limit": 20,
                "memory_limit": 512,
                "storage_limit": 200,
                "oltp_namespace": "hugegraph-server-update1",
                "olap_namespace": "hugegraph-computer-update1",
                "storage_namespace": "lxb_storage",
                "compute_cpu_limit": 100,
                "compute_memory_limit": 512,
                "max_graph_number": 2,
                "max_role_number": 21
            }
        }
        code, res = GraphSpace().update_graph_space(body=update_body, space=graph_space_name, auth=auth)
        print(code, res)
        assert code == 200

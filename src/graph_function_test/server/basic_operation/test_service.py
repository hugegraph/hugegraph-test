# -*- coding:utf-8 -*-
"""
author  : lxb
note    : test_service
time    : 2022/2/16 下午7:37
"""
import os
import sys
import json

from src.common.server_api import GraphSpace
from src.common.server_api import Service

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password

graph_space_name = "gs_tmp"
service_name = "ser_tmp"
service_name1 = "ser_tmp1"


class TestGraphSpace:
    """
    测试图服务的增删改查
    """

    def setup_class(self):
        """
        创建图计算空间
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

        body = {
            "name": service_name1,
            "type": "OLTP",
            "count": 1,
            "cpu_limit": 20,
            "memory_limit": 50,
            "storage_limit": 50,
            "deployment_type": "K8S",
            "route_type": "NodePort",
            "urls": [],
            "description": "test oltp service"
        }
        code, res = Service().create_service(space=graph_space_name, body=body, auth=auth)
        print(code, res)
        assert code == 201

    # def setup(self):
    #     """
    #
    #     :return:
    #     """
    #     body = {
    #         "name": service_name1,
    #         "type": "OLTP",
    #         "count": 1,
    #         "cpu_limit": 20,
    #         "memory_limit": 50,
    #         "storage_limit": 50,
    #         "deployment_type": "K8S",
    #         "route_type": "NodePort",
    #         "urls": [],
    #         "description": "test oltp service"
    #     }
    #     code, res = Service().create_service(space=graph_space_name, body=body, auth=auth)
    #     print(code, res)
    #     assert code == 201

    # def teardown(self):
    #     """
    #     删除图service
    #     :return:
    #     """
    #     code, res = Service().delete_service(
    #         space=graph_space_name,
    #         service=service_name,
    #         param={"confirm_message": "I'm sure to delete the service"},
    #         auth=auth
    #     )
    #     print(code, res)
    #     assert code == 204

    def teardown_class(self):
        """
        删除图空间
        :return:
        """
        code, res = GraphSpace().delete_graph_space(space=graph_space_name, auth=auth)
        print(code, res)
        assert code == 204

    def test_create_servcie(self):
        """
        创建service
        :return:
        """
        body = {
            "name": service_name,
            "type": "OLTP",
            "count": 1,
            "cpu_limit": 20,
            "memory_limit": 50,
            "storage_limit": 50,
            "deployment_type": "K8S",
            "route_type": "NodePort",
            "urls": [],
            "description": "test oltp service"
        }
        code, res = Service().create_service(space=graph_space_name, body=body, auth=auth)
        print(code, res)
        assert code == 201

        code, res = Service().delete_service(
            space=graph_space_name,
            service=service_name,
            param={"confirm_message": "I'm sure to delete the service"},
            auth=auth
        )
        print(code, res)
        assert code == 204

    def test_get_one_servcie(self):
        """
        get one service
        :return:
        """
        code, res = Service().get_one_service(space=graph_space_name, service=service_name1, auth=auth)
        print(code, res)
        assert code == 200

    def test_get_servcie(self):
        """
        get service
        :return:
        """
        code, res = Service().get_service(space=graph_space_name, auth=auth)
        print(code, res)
        assert code == 200

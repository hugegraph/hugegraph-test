# -*- coding:utf-8 -*-
"""
author     : lxb
note       :
create_time: 2020/4/22 5:17 下午
"""
import pytest
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Algorithm
from src.common.task_res import get_task_res
from src.common.server_api import Gremlin
from src.common.loader import InsertData
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class TestClusterCoeffcient:
    """
    接口cluster_coeffcient：聚类系数
    """

    @staticmethod
    def setup_class(self):
        """
        测试类开始
        """
        Gremlin().gremlin_post('graph.truncateBackend();')
        InsertData(gremlin='gremlin_alg_03.txt').gremlin_graph()

    @pytest.mark.caseL0
    def test_cluster_coeffcient_01(self):
        """
        param = []
        :return:
        """
        body = {}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges': 13, 'vertices': 16, 'cluster_coeffcient': 0.14285714285714285}
        else:
            assert 0

    @pytest.mark.caseL0
    def test_cluster_coeffcient_02(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "BOTH"}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges': 13, 'vertices': 16, 'cluster_coeffcient': 0.14285714285714285}
        else:
            assert 0

    @pytest.mark.caseL0
    def test_cluster_coeffcient_03(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "IN"}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges_in': 13, 'vertices_in': 9, 'cluster_coeffcient': 0.3333333333333333}
        else:
            assert 0

    @pytest.mark.caseL0
    def test_cluster_coeffcient_04(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "OUT"}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges_out': 13, 'vertices_out': 7, 'cluster_coeffcient': 0.25}
        else:
            assert 0

    @pytest.mark.caseL0
    def test_cluster_coeffcient_05(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "IN", "degree": -1}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges_in': 13, 'vertices_in': 9, 'cluster_coeffcient': 0.3333333333333333}
        else:
            assert 0

    @pytest.mark.caseL0
    def test_cluster_coeffcient_06(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "OUT", "degree": -1}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges_out': 13, 'vertices_out': 7, 'cluster_coeffcient': 0.25}
        else:
            assert 0

    @pytest.mark.caseL0
    def test_cluster_coeffcient_07(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "OUT", "degree": 1}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges_out': 13, 'vertices_out': 7, 'cluster_coeffcient': 0.0}
        else:
            assert 0

    @pytest.mark.caseL0
    def test_cluster_coeffcient_08(self):
        """
        param = [direction, degree]
        :return:
        """
        body = {"direction": "IN", "degree": 1}
        code, res = Algorithm().post_cluster_coeffcient(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'edges_in': 13, 'vertices_in': 9, 'cluster_coeffcient': 0.0}
        else:
            assert 0


if __name__ == '__main__':
    pass
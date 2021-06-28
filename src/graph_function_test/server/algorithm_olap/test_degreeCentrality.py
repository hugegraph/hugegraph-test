# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 度中心算法 测试
create_time: 2020/4/22 5:17 下午
"""
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Algorithm
from src.common.task_res import get_task_res
from src.common.server_api import Gremlin
from src.common.loader import InsertData
from src.config import basic_config as _cfg
from src.common.tools import clear_graph

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class TestDegreeCentrality:
    """
    接口degree_centrality：度中心性
    """

    @staticmethod
    def setup_class(self):
        """
        测试类开始
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用gremlin语句进行truncate操作

        InsertData(gremlin='gremlin_alg_02.txt').gremlin_graph()

    def test_degree_centrality_01(self):
        """
        no param
        :return:
        """
        body = {}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:lop': 1, '1:josh': 1, '1:marko': 3,
                              '1:peter': 3, '1:vadas': 1, '2:ripple': 3}
        else:
            assert 0

    def test_degree_centrality_02(self):
        """
        param = [label]
        :return:
        """
        body = {"label": "created"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:marko': 1, '1:peter': 1, '2:ripple': 2}
        else:
            assert 0

    def test_degree_centrality_03(self):
        """
        param = [label]
        :return:
        """
        body = {"label": "knows"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:josh': 1, '1:marko': 2, '1:peter': 2, '1:vadas': 1}
        else:
            assert 0

    def test_degree_centrality_04(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "BOTH"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:lop': 1, '1:josh': 1, '1:marko': 3,
                              '1:peter': 3, '1:vadas': 1, '2:ripple': 3}
        else:
            assert 0

    def test_degree_centrality_05(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "OUT"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:lop': 1, '1:marko': 3, '1:peter': 2}
        else:
            assert 0

    def test_degree_centrality_06(self):
        """
        param = [direction]
        :return:
        """
        body = {"direction": "IN"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:josh': 1, '1:peter': 1, '1:vadas': 1, '2:ripple': 3}
        else:
            assert 0

    def test_degree_centrality_07(self):
        """
        param = [top]
        :return:
        """
        body = {"top": 0}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:lop': 1, '1:josh': 1, '1:marko': 3,
                               '1:peter': 3, '1:vadas': 1, '2:ripple': 3}
        else:
            assert 0

    def test_degree_centrality_08(self):
        """
        param = [top]
        :return:
        """
        body = {"top": 5}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 3, '1:marko': 3, '1:peter': 3, '1:josh': 1, '1:vadas': 1}
        else:
            assert 0

    def test_degree_centrality_09(self):
        """
        param = [top、direction]
        :return:
        """
        body = {"direction": "OUT", "top": 5}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:marko': 3, '1:peter': 2, '2:lop': 1}
        else:
            assert 0

    def test_degree_centrality_10(self):
        """
        param = [top、direction、label]
        :return:
        """
        body = {"direction": "OUT", "top": 5, "label": "created"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:marko': 1, '1:peter': 1}
        else:
            assert 0

    def test_degree_centrality_11(self):
        """
        param = [top、direction、label]
        :return:
        """
        body = {"direction": "IN", "top": 5, "label": "created"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 2}
        else:
            assert 0

    def test_degree_centrality_12(self):
        """
        param = [top、direction、label]
        :return:
        """
        body = {"direction": "OUT", "top": 5, "label": "created"}
        code, res = Algorithm().post_degree_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:marko': 1, '1:peter': 1}
        else:
            assert 0


if __name__ == '__main__':
    pass

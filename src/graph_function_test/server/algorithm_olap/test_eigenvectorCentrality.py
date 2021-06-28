# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap算法 特征向量中心性
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


class TestEigenvectorCentrality:
    """
    接口eigenvector_centrality：特征中心性
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

    def test_eigenvector_centrality_01(self):
        """
        param = [depth]
        :return:
        """
        body = {"depth": 5}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert 1
            # assert result == {'2:ripple': 3, '1:marko': 4, '1:josh': 2, '1:vadas': 3, '1:peter': 4, '2:lop': 3}
        else:
            assert 0

    def test_eigenvector_centrality_02(self):
        """
        param = [depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": -1}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert 1
            # assert result == {'2:ripple': 3, '1:marko': 5, '1:josh': 2, '1:vadas': 5, '1:peter': 4, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_03(self):
        """
        param = [depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": 2}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert 1
            # assert result == {'2:ripple': 2, '1:peter': 1, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_04(self):
        """
        param = [depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 10, '1:marko': 10, '1:josh': 10,
                              '1:vadas': 10, '1:peter': 10, '2:lop': 10}
        else:
            assert 0

    def test_eigenvector_centrality_05(self):
        """
        param = [depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": 2}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert 1
            # assert result == {'2:ripple': 4, '1:marko': 4, '1:josh': 7, '1:vadas': 5, '1:peter': 6, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_06(self):
        """
        param = [depth, sample, label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "created"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 3, '1:marko': 3, '1:josh': 1,
                              '1:vadas': 1, '1:peter': 3, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_07(self):
        """
        param = [depth, sample, label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "knows"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 1, '1:marko': 4, '1:josh': 4,
                              '1:vadas': 4, '1:peter': 4, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_08(self):
        """
        param = [depth, sample, direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "BOTH"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 10, '1:marko': 10, '1:josh': 10,
                              '1:vadas': 10, '1:peter': 10, '2:lop': 10}
        else:
            assert 0

    def test_eigenvector_centrality_09(self):
        """
        param = [depth, sample, direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "OUT"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 5, '1:marko': 1, '1:josh': 3,
                              '1:vadas': 2, '1:peter': 2, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_10(self):
        """
        param = [depth, sample, direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "IN"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 1, '1:marko': 6, '1:josh': 1,
                              '1:vadas': 1, '1:peter': 3, '2:lop': 2}
        else:
            assert 0

    def test_eigenvector_centrality_11(self):
        """
        param = [depth, sample, degree]
        :return:
        """
        body = {"depth": 5, "sample": -1, "degree": 5}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 10, '1:marko': 10, '1:josh': 10, '1:vadas': 10, '1:peter': 10, '2:lop': 10}
        else:
            assert 0

    def test_eigenvector_centrality_12(self):
        """
        param = [depth, sample, top]
        :return:
        """
        body = {"depth": 5, "sample": -1, "top": 5}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 10, '1:marko': 10, '1:josh': 10, '1:vadas': 10, '1:peter': 10}
        else:
            assert 0

    def test_eigenvector_centrality_13(self):
        """
        param = [depth, sample, top, degree, source_sample]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 10, '1:marko': 10, '1:josh': 10,
                              '1:vadas': 10, '1:peter': 10, '2:lop': 10}
        else:
            assert 0

    def test_eigenvector_centrality_14(self):
        """
        param = [depth, sample, top, degree, source_sample, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "label":"created"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 3, '1:marko': 3, '1:peter': 3, '1:josh': 1, '1:vadas': 1, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_15(self):
        """
        param = [depth, sample, top, degree, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction":"BOTH"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 10, '1:marko': 10, '1:josh': 10,
                              '1:vadas': 10, '1:peter': 10, '2:lop': 10}
        else:
            assert 0

    def test_eigenvector_centrality_16(self):
        """
        param = [depth, sample, top, degree, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction":"IN"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:marko': 6, '1:peter': 3, '2:lop': 2, '2:ripple': 1, '1:josh': 1, '1:vadas': 1}
        else:
            assert 0

    def test_eigenvector_centrality_17(self):
        """
        param = [depth, sample, top, degree, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction": "OUT"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 5, '1:josh': 3, '1:vadas': 2, '1:peter': 2, '1:marko': 1, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_18(self):
        """
        param = [depth, sample, top, degree, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction": "BOTH", "label": "created"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 3, '1:marko': 3, '1:peter': 3, '1:josh': 1, '1:vadas': 1, '2:lop': 1}
        else:
            assert 0

    def test_eigenvector_centrality_19(self):
        """
        param = [depth, sample, top, degree, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": 10,
                "direction": "BOTH", "label": "created"}
        code, res = Algorithm().post_eigenvector_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 3, '1:marko': 3, '1:peter': 3, '1:josh': 1, '1:vadas': 1, '2:lop': 1}
        else:
            assert 0


if __name__ == '__main__':
    pass

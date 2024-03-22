# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap 算法 紧密中心性
create_time: 2020/4/22 5:17 下午
"""
import sys
import os
import pytest

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


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='社区版已支持 Server-OLAP 算法，等待重构开启')
class TestClosenessCentrality:
    """
    接口 closeness_centrality：紧密中心性
    """

    @staticmethod
    def setup_class(self):
        """
        测试类开始
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用 gremlin 语句进行 truncate 操作

        InsertData(gremlin='gremlin_alg_02.txt').gremlin_graph()

    def test_closeness_centrality_01(self):
        """
        param=[depth]
        :return:
        """
        body = {"depth": 5}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_02(self):
        """
        param=[depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": -1}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_03(self):
        """
        param=[depth, source_sample]
        :return:
        """
        body = {"depth": 5, "source_sample": 2}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_04(self):
        """
        param=[depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_05(self):
        """
        param=[depth, sample]
        :return:
        """
        body = {"depth": 5, "sample": 2}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_06(self):
        """
        param=[depth, label, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "created"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 2.0, '1:marko': 1.5, '1:josh': 0.0,
                              '1:vadas': 0.0, '1:peter': 1.5, '2:lop': 0.0}
        else:
            assert 0

    def test_closeness_centrality_07(self):
        """
        param=[depth, label, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "knows"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 0.0, '1:marko': 2.5, '1:josh': 1.8333334,
                              '1:vadas': 1.8333334, '1:peter': 2.5, '2:lop': 0.0}
        else:
            assert 0

    def test_closeness_centrality_08(self):
        """
        param=[depth, direction, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "BOTH"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_09(self):
        """
        param=[depth, direction, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "OUT"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 0.0, '1:marko': 3.5, '1:josh': 0.0,
                              '1:vadas': 0.0, '1:peter': 2.0, '2:lop': 1.0}
        else:
            assert 0

    def test_closeness_centrality_10(self):
        """
        param=[depth, direction, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "IN"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 3.0, '1:marko': 0.0, '1:josh': 1.5,
                              '1:vadas': 1.0, '1:peter': 1.0, '2:lop': 0.0}
        else:
            assert 0

    def test_closeness_centrality_11(self):
        """
        param=[depth, degree, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "degree": 5}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_12(self):
        """
        param=[depth, top, sample]
        :return:
        """
        body = {"depth": 5, "sample": -1, "top": 5}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:peter': 4.0,
                              '1:josh': 2.6666665, '1:vadas': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_13(self):
        """
        param=[depth, degree, sample, top, source_sample]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_14(self):
        """
        param=[depth, degree, sample, top, source_sample, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "label": "created"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 2.0, '1:marko': 1.5, '1:peter': 1.5,
                              '1:josh': 0.0, '1:vadas': 0.0, '2:lop': 0.0}
        else:
            assert 0

    def test_closeness_centrality_15(self):
        """
        param=[depth, degree, sample, top, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "BOTH"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 4.0, '1:josh': 2.6666665,
                              '1:vadas': 2.6666665, '1:peter': 4.0, '2:lop': 2.6666665}
        else:
            assert 0

    def test_closeness_centrality_16(self):
        """
        param=[depth, degree, sample, top, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "IN"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 3.0, '1:josh': 1.5, '1:vadas': 1.0,
                              '1:peter': 1.0, '1:marko': 0.0, '2:lop': 0.0}
        else:
            assert 0

    def test_closeness_centrality_17(self):
        """
        param=[depth, degree, sample, top, source_sample, direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "OUT"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:marko': 3.5, '1:peter': 2.0, '2:lop': 1.0,
                              '2:ripple': 0.0, '1:josh': 0.0, '1:vadas': 0.0}
        else:
            assert 0

    def test_closeness_centrality_18(self):
        """
        param=[depth, degree, sample, top, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1,
                "direction": "BOTH", "label": "created"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 2.0, '1:marko': 1.5, '1:peter': 1.5,
                              '1:josh': 0.0, '1:vadas': 0.0, '2:lop': 0.0}
        else:
            assert 0

    def test_closeness_centrality_19(self):
        """
        param=[depth, degree, sample, top, source_sample, direction, label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": 10,
                "direction": "BOTH", "label": "created"}
        code, res = Algorithm().post_closeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 2.0, '1:marko': 1.5, '1:peter': 1.5,
                              '1:josh': 0.0, '1:vadas': 0.0, '2:lop': 0.0}
        else:
            assert 0


if __name__ == '__main__':
    pass

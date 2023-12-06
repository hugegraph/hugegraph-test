# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap算法 中介中心性 测试
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


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='目前只有商业版支持OLAP算法')
class TestBetweenessCentrality:
    """
    betweeness_centrality：中介中心性算法
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

        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

    def test_betweeness_centrality_01(self):
        """
        params = [depth]
        :return:
        """
        body = {"depth": 5}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_02(self):
        """
        params = [depth、source_sample]  source_sample 目前不起作用
        :return:
        """
        body = {"depth": 5, "source_sample": -1}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_03(self):
        """
        params = [depth、source_sample]  source_sample 目前不起作用
        :return:
        """
        body = {"depth": 5, "source_sample": 2}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_04(self):
        """
        params = [depth、sample]   sample 目前不起作用
        :return:
        """
        body = {"depth": 5, "sample": -1}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_05(self):
        """
        params = [depth、sample]  sample 目前不起作用
        :return:
        """
        body = {"depth": 5, "sample": 2}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_06(self):
        """
        params = [depth、sample、label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "created"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 0.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 2.0, '1:peter': 0.0, '2:lop': 0.0}

        else:
            assert 0

    def test_betweeness_centrality_07(self):
        """
        params = [depth、sample、label]
        :return:
        """
        body = {"depth": 5, "sample": -1, "label": "knows"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 0.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 0.0, '1:peter': 0.0, '2:lop': 0.0}
        else:
            assert 0

    def test_betweeness_centrality_08(self):
        """
        params = [depth、sample、direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "BOTH"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_09(self):
        """
        params = [depth、sample、direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "OUT"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 2.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 4.0, '1:peter': 4.0, '2:lop': 2.0}
        else:
            assert 0

    def test_betweeness_centrality_10(self):
        """
        params = [depth、sample、direction]
        :return:
        """
        body = {"depth": 5, "sample": -1, "direction": "IN"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 2.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 4.0, '1:peter': 4.0, '2:lop': 2.0}
        else:
            assert 0

    def test_betweeness_centrality_11(self):
        """
        params = [depth、sample、degree]
        :return:
        """
        body = {"depth": 5, "sample": -1, "degree": 5}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_12(self):
        """
        params = [depth、sample、top]
        :return:
        """
        body = {"depth": 5, "sample": -1, "top": 3}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:vadas': 9.0, '1:peter': 9.0, '2:ripple': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_13(self):
        """
        params = [depth、sample、top、source_sample、degree]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_14(self):
        """
        params = [depth、sample、top、source_sample、degree、label]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "label": "created"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:vadas': 2.0, '2:ripple': 0.0, '1:marko': 0.0,
                              '1:josh': 0.0, '1:peter': 0.0, '2:lop': 0.0}
        else:
            assert 0

    def test_betweeness_centrality_15(self):
        """
        params = [depth、sample、top、source_sample、degree、direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "BOTH"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'2:ripple': 4.0, '1:marko': 0.0, '1:josh': 0.0,
                              '1:vadas': 9.0, '1:peter': 9.0, '2:lop': 4.0}
        else:
            assert 0

    def test_betweeness_centrality_16(self):
        """
        params = [depth、sample、top、source_sample、degree、direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "IN"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:vadas': 4.0, '1:peter': 4.0, '2:ripple': 2.0,
                              '2:lop': 2.0, '1:marko': 0.0, '1:josh': 0.0}
        else:
            assert 0

    def test_betweeness_centrality_17(self):
        """
        params = [depth、sample、top、source_sample、degree、direction]
        :return:
        """
        body = {"depth": 5, "degree": 50, "sample": -1, "top": 10, "source_sample": -1, "direction": "OUT"}
        code, res = Algorithm().post_betweeness_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:vadas': 4.0, '1:peter': 4.0, '2:ripple': 2.0,
                              '2:lop': 2.0, '1:marko': 0.0, '1:josh': 0.0}
        else:
            assert 0


if __name__ == '__main__':
    pass

# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap算法 环算法
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
from src.common.tools import clear_graph

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='目前只有商业版支持OLAP算法')
class TestRingsDetect01:
    """
    接口rings_detect：环路检测
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

        InsertData(gremlin='gremlin_hlm.txt').gremlin_graph()

    def test_rings_detect_01(self):
        """
        param = [depth]
        :return:
        """
        body = {"depth": 5}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_02(self):
        """
        param = [depth, source_label]
        :return:
        """
        body = {"depth": 5, "source_label": "男人"}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 8
        else:
            assert 0

    def test_rings_detect_03(self):
        """
        param = [depth, direction]
        :return:
        """
        body = {"depth": 5, "direction": "BOTH"}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_04(self):
        """
        param = [depth, direction]
        :return:
        """
        body = {"depth": 5, "direction": "IN"}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 0
        else:
            assert 0

    def test_rings_detect_05(self):
        """
        param = [depth, direction]
        :return:
        """
        body = {"depth": 5, "direction": "OUT"}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 0
        else:
            assert 0

    def test_rings_detect_06(self):
        """
        param = [depth, label]
        :return:
        """
        body = {"depth": 5, "label": "妻"}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 0
        else:
            assert 0

    def test_rings_detect_07(self):
        """
        param = [depth, degree]
        :return:
        """
        body = {"depth": 5, "degree": 5}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_08(self):
        """
        param = [depth, capacity]
        :return:
        """
        body = {"depth": 5, "capacity": 50}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_09(self):
        """
        param = [depth, limit]
        :return:
        """
        body = {"depth": 5, "limit": -1}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_10(self):
        """
        param = [depth, direction, degree]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_11(self):
        """
        param = [depth, direction, degree, limit]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "limit": -1}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_12(self):
        """
        param = [depth, direction, degree, limit, label]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "limit": -1, "label": "妻"}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 0
        else:
            assert 0

    def test_rings_detect_13(self):
        """
        param = [depth, direction, degree, limit, label, capacity]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "limit": -1, "label": "妻", "capacity": 50}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 0
        else:
            assert 0

    def test_rings_detect_14(self):
        """
        param = [depth, workers]
        :return:
        """
        body = {"depth": 5, "workers": -1}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_15(self):
        """
        param = [depth, workers]
        :return:
        """
        body = {"depth": 5, "workers": 0}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_16(self):
        """
        :return:
        """
        body = {"depth": 5, "workers": 100}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_17(self):
        """
        param = [depth, direction, degree, workers]
        :return:
        """
        body = {"direction": "BOTH", "depth": 5, "degree": 50, "workers": 0}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_18(self):
        """
        param = [depth, count_only, workers]
        :return:
        """
        body = {"depth": 5, "count_only": True, "workers": 0}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['rings_count'] == 18
        else:
            assert 0

    def test_rings_detect_19(self):
        """
        param = [depth, count_only, workers]
        :return:
        """
        body = {"depth": 5, "count_only": False, "workers": 0}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 18
        else:
            assert 0

    def test_rings_detect_20(self):
        """
        param = [depth, count_only, workers]
        :return:
        """
        body = {"depth": 5, "count_only": True, "workers": 10}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['rings_count'] == 18
        else:
            assert 0


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='目前只有商业版支持OLAP算法')
class TestRingsDetect02:
    """
    接口rings_detect：环路检测
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
        InsertData(gremlin='gremlin_alg_05.txt').gremlin_graph()

    def test_rings_detect_01(self):
        """
        :return:
        """
        body = {"depth": 5, "limit": 2}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 2
        else:
            assert 0

    def test_rings_detect_02(self):
        """
        :return:
        """
        body = {"depth": 5, "limit": 1}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 1
        else:
            assert 0

    def test_rings_detect_03(self):
        """
        :return:
        """
        body = {"depth": 5, "limit": 3}
        code, res = Algorithm().post_rings_detect(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert len(result['rings']) == 3
        else:
            assert 0


if __name__ == '__main__':
    pass


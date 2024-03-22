### -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap 算法 lpa 社区发现
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


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='社区版已支持 Server-OLAP 算法，等待重构开启')
class TestLpa:
    """
    接口 lpa：lpa 社区发现 --- 发现社区的结果会一直变化
    """

    def setup(self):
        """
        case 开始
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用 gremlin 语句进行 truncate 操作

        InsertData(gremlin='gremlin_alg_03.txt').gremlin_graph()

    def test_lpa_01(self):
        """
        :return:
        """
        body = {}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_02(self):
        """
        :return:
        """
        body = {"label": "created", "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_03(self):
        """
        :return:
        """
        body = {"direction": "BOTH", "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_04(self):
        """
        :return:
        """
        body = {"direction": "OUT", "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_05(self):
        """
        :return:
        """
        body = {"direction": "IN", "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_06(self):
        """
        :return:
        """
        body = {"degree": 2, "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_07(self):
        """
        :return:
        """
        body = {"degree": -1, "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_08(self):
        """
        :return:
        """
        body = {"times": 10, "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_09(self):
        """
        :return:
        """
        body = {"percision": 0.5, "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_10(self):
        """
        :return:
        """
        body = {"direction": "BOTH"}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_11(self):
        """
        :return:
        """
        body = {"source_label": "person", "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_12(self):
        """
        :return:
        """
        body = {
            # "source_label": "person",
            "label": "created",
            "direction": "OUT",
            "percision": 0.5,
            "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_13(self):
        """
        :return:
        """
        body = {
            # "source_label": "person",
            "label": "created",
            "direction": "OUT",
            "percision": 0.5,
            "degree": 5,
            "times": 10,
            # "show_community": "1:r",
            "workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_14(self):
        """
        :return:
        """
        body = {"workers": -1}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_15(self):
        """
        :return:
        """
        body = {"workers": 0}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0

    def test_lpa_16(self):
        """
        :return:
        """
        body = {"workers": 100}
        code, res = Algorithm().post_lpa(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result
        else:
            assert 0


if __name__ == '__main__':
    pass

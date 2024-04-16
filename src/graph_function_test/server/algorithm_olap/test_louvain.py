### -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap 算法 louvain 测试
create_time: 2020/4/22 5:17 下午
"""
import sys
import os
import time

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

@pytest.mark.skip(reason="java.lang.IllegalArgumentException: It's not allowed to query with offser/limit when there are uncommitted records.")
class TestLouvain:
    """
    接口 louvain：louvain 社区发现
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

    def test_louvain_01(self):
        """
        :return:
        """
        body = {}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_02(self):
        """
        :return:
        """
        body = {"source_label": "person", "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_03(self):
        """
        :return:
        """
        body = {"degree": 5, "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_04(self):
        """
        :return:
        """
        body = {"times": 5, "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_05(self):
        """
        :return:
        """
        body = {"stable_times": 5, "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_06(self):
        """
        :return:
        """
        body = {"percision": 0.1, "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_07(self):
        """
        :return:
        """
        body = {"show_community": "1:h", "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == []
        else:
            assert 0

    def test_louvain_08(self):
        """
        :return:
        """
        ### 进行 louvain 算法
        Algorithm().post_louvain({}, auth=auth)
        time.sleep(60)
        ### 清空所有层社区 "clear": -1
        body = {"clear": -1, "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == 16
        else:
            assert 0

    def test_louvain_09(self):
        """
        :return:
        """
        ### 进行 louvain 算法
        Algorithm().post_louvain({}, auth=auth)
        time.sleep(60)
        ### 清空 0 层社区 "clear": 0
        body = {"clear": 0, "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == 13
        else:
            assert 0

    def test_louvain_10(self):
        """
        :return:
        """
        ### 进行 louvain 算法
        Algorithm().post_louvain({}, auth=auth)
        time.sleep(60)
        ### 展示 0 层社区
        body = {"show_modularity": 0, "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == 0.3905325443786982
        else:
            assert 0

    def test_louvain_11(self):
        """
        :return:
        """
        body = {"degree": 5,
                "times": 10,
                "stable_times": 5,
                "percision": 0.1,
                "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_12(self):
        """
        :return:
        """
        body = {"degree": -1,
                "times": 10,
                "stable_times": 5,
                "percision": 0.1,
                "source_label": "person",
                "show_community": "1:h",
                "clear": -1,
                "show_modularity": 0,
                "workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == 0
        else:
            assert 0

    def test_louvain_13(self):
        """
        :return:
        """
        body = {"workers": -1}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_14(self):
        """
        :return:
        """
        body = {"workers": 0}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0

    def test_louvain_15(self):
        """
        :return:
        """
        body = {"workers": 100}
        code, res = Algorithm().post_louvain(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result['communities'] == 3 and result['modularity'] == 0.5680473372781065
        else:
            assert 0


if __name__ == '__main__':
    pass

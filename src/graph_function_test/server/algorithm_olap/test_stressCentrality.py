# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 重力中心算法 测试
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


class TestStressCentrality:
    """
    stress_centrality 接口
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

    def test_stressCentrality_01(self):
        """
        :return:
        """
        body = {"depth": 10}
        code, res = Algorithm().post_stress_centrality(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'1:marko': 8, '1:josh': 8, '1:o': 8, '1:peter': 0, '2:p': 8, '1:r': 0, '1:s': 0,
                              '1:wang': 0, '1:qian': 0, '2:ripple': 0, '1:li': 0, '1:vadas': 0, '2:zhao': 0,
                              '2:lop': 8, '2:e': 0, '1:h': 8}
        else:
            assert 0


if __name__ == "__main__":
    pass

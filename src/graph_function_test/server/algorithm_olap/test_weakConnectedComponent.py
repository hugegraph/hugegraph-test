# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 若联通子图 测试
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


class TestWeakConnectedComponent:
    """
    weak_connected_component 接口
    """

    def setup(self):
        """
        case 开始
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用gremlin语句进行truncate操作

        InsertData(gremlin='gremlin_alg_03.txt').gremlin_graph()

    def test_weakConnectedComponent_01(self):
        """
        :return:
        """
        body = {}
        code, res = Algorithm().post_weak_connected_component(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'components': 5, 'iteration_times': 1, 'times': 20}
        else:
            assert 0


if __name__ == "__main__":
    pass

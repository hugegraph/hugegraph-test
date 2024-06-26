# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap 算法 点统计
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


class TestCountVertex:
    """
    接口 count_vertex：统计顶点信息，包括图中顶点数量、各类型的顶点数量
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

        InsertData(gremlin='gremlin_alg_03.txt').gremlin_graph()

    def test_count_vertex(self):
        """
        统计顶点信息接口
        :return:
        """
        body = {}
        code, res = Algorithm().post_count_vertex(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'software': 5, 'person': 11, '*': 16}
        else:
            assert 0


if __name__ == '__main__':
    pass

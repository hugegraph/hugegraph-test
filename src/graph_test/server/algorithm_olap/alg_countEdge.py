# -*- coding:utf-8 -*-
"""
author     : lxb
note       :
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

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class TestCountVertex:
    """
    接口count_edge：统计边信息，包括图中边数量、各类型的边数量
    """

    @staticmethod
    def setup_class(self):
        """
        测试类开始
        """
        Gremlin().gremlin_post('graph.truncateBackend();')
        InsertData(gremlin='gremlin_alg_03.txt').gremlin_graph()

    @pytest.mark.caseL0
    def test_count_edge(self):
        """
        统计边信息接口
        :return:
        """
        body = {}
        code, res = Algorithm().post_count_edge(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'created': 8, '*': 13, 'knows': 5}
        else:
            assert 0


if __name__ == '__main__':
    pass

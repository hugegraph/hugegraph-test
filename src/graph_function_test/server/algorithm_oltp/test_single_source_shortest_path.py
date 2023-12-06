# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 从一顶点出发根据条件进行最短路径查询
create_time:
"""
import os
import sys
import unittest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Traverser
from src.common.server_api import Gremlin
from src.common.loader import InsertData
from src.config import basic_config as _cfg
from src.common.tools import clear_graph

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class TestSingleSourceShortestPath(unittest.TestCase):
    """
    从一个顶点查找depth步可达的最短路径顶点
    """

    @staticmethod
    def setup_class():
        """
        测试类开始
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用gremlin语句进行truncate操作

        InsertData(gremlin='gremlin_traverser.txt').gremlin_graph()

    def test_required_params(self):
        """
        source、max_depth
        :return:
        """
        param_json = {'source': '"1:marko"', 'with_vertex': True}
        code, res = Traverser().get_single_source_shortestPath(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(
            res['paths'],
            {
                '2:ripple': {'weight': 2.0, 'vertices': ['1:marko', '1:josh', '2:ripple']},
                '1:josh': {'weight': 1.0, 'vertices': ['1:marko', '1:josh']},
                '1:vadas': {'weight': 1.0, 'vertices': ['1:marko', '1:vadas']},
                '1:peter': {'weight': 2.0, 'vertices': ['1:marko', '2:lop', '1:peter']},
                '2:lop': {'weight': 1.0, 'vertices': ['1:marko', '2:lop']}
            }
        )


if __name__ == "__main__":
    pass

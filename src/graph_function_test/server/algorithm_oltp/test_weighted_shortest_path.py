# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 根据权重进行最短路径查询
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


class TestWeightedShortestPath(unittest.TestCase):
    """
    查找从起始顶点出发恰好depth步可达的顶点
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
        param_json = {'source': '"1:marko"', 'target': '"2:ripple"', 'weight': '"weight"', 'with_vertex': True}
        code, res = Traverser().get_weighted_shortestPath(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['path'], {'weight': 2.0, 'vertices': ['1:marko', '1:josh', '2:ripple']})


if __name__ == "__main__":
    pass

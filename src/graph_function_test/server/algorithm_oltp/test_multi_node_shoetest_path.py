# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 从部分顶点数据集中进行两两顶点之间中最短路径的查询
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


class TestMultiNodeShortestPath(unittest.TestCase):
    """
    查询部分顶点中两两顶点之前的最短路径
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

        InsertData(gremlin='gremlin_traverser.txt').gremlin_graph()

    def test_reqiured_params(self):
        """
        source、max_depth
        :return:
        """
        json = {
            "vertices": {
              "ids": ["1:vadas", "1:peter", "2:ripple"]
            },
            "step": {
                "direction": "BOTH",
                "properties": {}
            },
            "max_depth": 10,
            "capacity": 100000000,
            "with_vertex": True
        }
        code, res = Traverser().post_multi_node_shortestPath(json=json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['paths']), 3)
        for obj in res['paths']:
            self.assertIn(
                obj,
                [
                    {'objects': ['2:ripple', '1:josh', '1:marko', '1:vadas']},
                    {'objects': ['2:ripple', '1:josh', '2:lop', '1:peter']},
                    {'objects': ['1:vadas', '1:marko', '2:lop', '1:peter']}
                ]
            )


if __name__ == "__main__":
    pass


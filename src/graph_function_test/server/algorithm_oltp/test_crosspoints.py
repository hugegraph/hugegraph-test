# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 根据起始顶点、目的顶点、方向、边的类型（可选）和最大深度等条件查找相交点
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


class TestCrosspoints(unittest.TestCase):
    """
    根据起始顶点、目的顶点、方向、边的类型（可选）和最大深度等条件查找相交点
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
        param_json = {'source': '"2:lop"', 'target': '"2:ripple"', 'max_depth': 5, 'direction': 'IN'}
        code, res = Traverser().get_crosspoints(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['crosspoints']), 1)
        for obj in res['crosspoints']:
            self.assertIn(
                obj,
                [
                    {'crosspoint': '1:josh', 'objects': ['2:lop', '1:josh', '2:ripple']},
                    {'crosspoint': '1:marko', 'objects': ['2:lop', '1:marko', '1:josh', '2:ripple']}
                ]
            )


if __name__ == "__main__":
    pass


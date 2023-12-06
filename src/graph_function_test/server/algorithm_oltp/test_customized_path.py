# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 根据一批顶点，边规则和最大深度等条件进行符合条件的路径查询
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


class TestCustomizedPaths(unittest.TestCase):
    """
    查询一批顶点符合条件的路径
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
        json = {
            "sources": {
                "ids": [],
                "label": "person",
                "properties": {
                    "name": "marko"
                }
            },
            "steps": [
                {
                    "direction": "OUT",
                    "labels": [
                        "knows"
                    ],
                    "weight_by": "weight",
                    "degree": -1
                },
                {
                    "direction": "OUT",
                    "labels": [
                        "created"
                    ],
                    "default_weight": 8,
                    "degree": -1,
                    "sample": -1
                }
            ],
            "sort_by": "INCR",
            "with_vertex": True,
            "capacity": -1,
            "limit": -1
        }
        code, res = Traverser().post_customized_paths(json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(
            res['paths'],
            [
                {'objects': ['1:marko', '1:josh', '2:ripple'], 'weights': [1.0, 8.0]},
                {'objects': ['1:marko', '1:josh', '2:lop'], 'weights': [1.0, 8.0]}
            ]
        )


if __name__ == "__main__":
    pass

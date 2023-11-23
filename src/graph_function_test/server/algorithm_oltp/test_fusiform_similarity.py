# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 按照条件查询一批顶点对应的"梭形相似点"
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


class TestFusiformSimilarity(unittest.TestCase):
    """
    按照条件查询一批顶点对应的"梭形相似点"
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

        InsertData(gremlin='gremlin_hlm.txt').gremlin_graph()

    def test_reqiured_params(self):
        """
        :return:
        """
        json = {
            "sources": {
                "ids": [],
                "label": "男人"
            },
            "min_neighbors": 2,
            "alpha": 0.60,
            "capacity": -1,
            "limit": -1,
            "with_intermediary": False,
            "with_vertex": True
        }
        code, res = Traverser().post_fusiform_similarity(body=json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['similars'], {'1:贾代善': [{'id': '2:贾母', 'score': 0.6, 'intermediaries': []}]})


if __name__ == "__main__":
    pass


# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 通过指定的分片大小split_size，获取顶点分片信息（可以与 Scan 配合使用来获取顶点）。
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


class TestVertexShard(unittest.TestCase):
    """
    通过指定的分片大小split_size，获取顶点分片信息（可以与 Scan 配合使用来获取顶点）。
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

        InsertData(gremlin='gremlin_hlm.txt').gremlin_graph()

    def test_required_params(self):
        """
        :return:
        """
        json = {'split_size': 1048576}
        code, res = Traverser().get_vertex_shard(json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res, {'shards': [{'end': 'iLG65yK0ZZQg8tRMAA==',
                                           'length': 0,
                                           'start': 'hzE65Y+y5YCZ'},
                                          {'end': 'ijI66LW15aeo5aiYAA==',
                                           'length': 0,
                                           'start': 'iLG65yK0ZZQg8tRMAA=='}]})


if __name__ == "__main__":
    pass

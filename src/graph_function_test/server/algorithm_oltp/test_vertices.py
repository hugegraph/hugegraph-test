# -*- coding:utf-8 -*-
"""
author     : lxb
note       : oltp算法 点计数
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


class TestVertices(unittest.TestCase):
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

        InsertData(gremlin='gremlin_hlm.txt').gremlin_graph()

    def test_required_params(self):
        """
        source、max_depth
        :return:
        """
        part_url = "?ids=%s&ids=%s&ids=%s&ids=%s" % ('"1:贾宝玉"', '"1:贾代善"', '"2:林黛玉"', '"2:薛宝钗"')
        code, res = Traverser().get_vertices(part_url, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(4, len(res["vertices"]))


if __name__ == "__main__":
    pass

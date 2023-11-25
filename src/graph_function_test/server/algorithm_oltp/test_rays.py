# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 根据起始顶点、方向、边的类型（可选）和最大深度等条件查找发散到边界顶点的路径
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


class TestRays(unittest.TestCase):
    """
    根据起始顶点、方向、边的类型（可选）和最大深度等条件查找发散到边界顶点的路径
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
        source、max_depth
        :return:
        """
        param_json = {'source': '"1:贾宝玉"', 'max_depth': 2}
        code, res = Traverser().get_rays(param_json=param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['rays']), 9)
        for obj in res['rays']:
            self.assertIn(
                obj,
                [
                    {'objects': ['1:贾宝玉', '2:王夫人', '2:薛姨妈']},
                    {'objects': ['1:贾宝玉', '2:王夫人', '2:贾元春']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '2:贾敏']},
                    {'objects': ['1:贾宝玉', '2:史湘云', '1:史氏']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '1:林如海']},
                    {'objects': ['1:贾宝玉', '2:王夫人', '1:贾珠']},
                    {'objects': ['1:贾宝玉', '2:史湘云', '1:卫若兰']},
                    {'objects': ['1:贾宝玉', '2:王夫人', '1:贾政']},
                    {'objects': ['1:贾宝玉', '2:薛宝钗', '2:薛姨妈']}
                ]
            )


if __name__ == "__main__":
    pass

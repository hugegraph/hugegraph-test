# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 获取所有路径
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


class TestPaths(unittest.TestCase):
    """
    查找从起始顶点出发到达目的顶点的所有路径
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

    def test_get_paths_reqiured_params(self):
        """
        source、max_depth
        :return:
        """
        param_json = {'source': '"1:贾宝玉"', 'target': '"1:贾代善"', 'max_depth': 5}
        code, res = Traverser().get_paths(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(
            res,
            {"paths": [{"objects": ["1:贾宝玉", "2:林黛玉", "1:林如海", "2:贾敏", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:王夫人", "1:贾政", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:王夫人", "1:贾政", "2:贾母", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:林黛玉", "2:贾敏", "2:贾母", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:林黛玉", "2:贾敏", "2:贾母", "1:贾政", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:林黛玉", "2:贾敏", "2:贾母", "1:贾赦", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:史湘云", "1:史氏", "1:史公", "2:贾母", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:林黛玉", "2:贾敏", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:王夫人", "1:贾政", "2:贾母", "1:贾赦", "1:贾代善"]},
                       {"objects": ["1:贾宝玉", "2:王夫人", "1:贾政", "2:贾母", "2:贾敏", "1:贾代善"]}]}
        )

    def test_get_paths_direction_in(self):
        """
        direction = in
        :return:
        """
        param_json = {'source': '"1:贾宝玉"', 'target': '"1:贾代善"', 'max_depth': 5, 'direction': 'IN'}
        code, res = Traverser().get_paths(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(
            res,
            {"paths":
                 [
                     {"objects": ["1:贾宝玉", "2:王夫人", "1:贾政", "1:贾代善"]},
                     {"objects": ["1:贾宝玉", "2:王夫人", "1:贾政", "2:贾母", "1:贾代善"]}
                  ]
             }
        )

    def test_get_paths_direction_out(self):
        """
        direction = out
        :return:
        """
        param_json = {'source': '"1:贾代善"', 'target': '"1:贾宝玉"', 'max_depth': 5, 'direction': 'OUT'}
        code, res = Traverser().get_paths(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(
            res,
            {"paths": [
                {"objects": ["1:贾代善", "1:贾政", "2:王夫人", "1:贾宝玉"]},
                {"objects": ["1:贾代善", "2:贾母", "1:贾政", "2:王夫人", "1:贾宝玉"]}
            ]
            }
        )

    def test_get_paths_reqiured_params(self):
        """
        source、max_depth
        :return:
        """
        param_json = {'source': '"1:贾宝玉"', 'target': '"1:贾代善"', 'max_depth': 4, 'limit': 200}
        code, res = Traverser().get_paths(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['paths']), 5)
        for obj in res['paths']:
            self.assertIn(
                obj,
                [
                    {'objects': ['1:贾宝玉', '2:王夫人', '1:贾政', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '2:贾敏', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '1:林黛玉', '2:贾敏', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:王夫人', '1:贾政', '2:贾母', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '2:贾敏', '2:贾母', '1:贾代善']}
                ]
            )

    def test_post_paths_reqiured_params(self):
        """
        source、max_depth
        :return:
        """
        json = {
            'sources': {'ids': ['1:贾宝玉']},
            'targets': {'ids': ['1:贾代善']},
            'step': {"direction": "BOTH"},
            'max_depth': 4,
            'limit': 100
        }
        code, res = Traverser().post_paths(json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['paths']), 5)
        for obj in res['paths']:
            self.assertIn(
                obj,
                [
                    {'objects': ['1:贾宝玉', '2:王夫人', '1:贾政', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '2:贾敏', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '1:林黛玉', '2:贾敏', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:王夫人', '1:贾政', '2:贾母', '1:贾代善']},
                    {'objects': ['1:贾宝玉', '2:林黛玉', '2:贾敏', '2:贾母', '1:贾代善']}
                ]
            )


if __name__ == "__main__":
    pass
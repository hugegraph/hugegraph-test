# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 在图中进行环路径查询
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


class TestRing(unittest.TestCase):
    """
    在图中查询环
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
        param_json = {'source': '"2:贾母"', 'max_depth': 4}
        code, res = Traverser().get_rings(param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['rings']), 6)
        for obj in res['rings']:
            self.assertIn(
                obj,
                [
                    {'objects': ['2:贾母', '1:贾代善', '1:贾赦', '2:贾母']},
                    {'objects': ['2:贾母', '2:贾敏', '1:贾代善', '1:贾政', '2:贾母']},
                    {'objects': ['2:贾母', '1:贾代善', '1:贾政', '2:贾母']},
                    {'objects': ['2:贾母', '1:贾赦', '1:贾代善', '1:贾政', '2:贾母']},
                    {'objects': ['2:贾母', '1:贾代善', '2:贾敏', '2:贾母']},
                    {'objects': ['2:贾母', '1:贾赦', '1:贾代善', '2:贾敏', '2:贾母']}
                ]
            )


if __name__ == "__main__":
    pass


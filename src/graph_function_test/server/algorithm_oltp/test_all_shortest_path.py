# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 所有的最短路径
create_time:  
"""
import sys
import os
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


class TestAllShorttestPath(unittest.TestCase):
    """
    查询所有最短路径
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

        InsertData(gremlin='gremlin_alg_01.txt').gremlin_graph()

    def test_param_normal(self):
        """
        source test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:marko"', "target": '"1:josh"', "max_depth": 5},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(
            res['paths'],
            [
                {'objects': ['1:marko', '1:vadas', '2:ripple', '1:peter', '1:josh']},
                {'objects': ['1:marko', '1:vadas', '2:lop', '1:peter', '1:josh']}
            ],
            "res is error"
        )

    def test_param_source_null(self):
        """
        source test
        :return:
        """
        code, res = Traverser().all_shortest_path(param={"target": '"1:josh"', "max_depth": 5}, auth=auth)
        print(code, res)
        self.assertEqual(code, 500, "code is error")
        self.assertEqual(res['message'], "The 'source vertex id' can't be null", "res is error")

    def test_param_source_typeInvalid(self):
        """
        source test
        :return:I
        """
        code, res = Traverser().all_shortest_path(
            param={"source": 'invalid', "target": '"1:josh"', "max_depth": 5},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(
            res['message'],
            "The vertex id must be formatted as Number/String/UUID, but got 'invalid'",
            "res is error"
        )

    def test_param_source_valueInvalid(self):
        """
        source test
        :return:I
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"invalid"', "target": '"1:josh"', "max_depth": 5},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(res['message'], "The source vertex with id 'invalid' does not exist", "res is error")

    def test_param_target_null(self):
        """
        target test
        :return:
        """
        code, res = Traverser().all_shortest_path(param={"source": '"1:josh"', "max_depth": 5}, auth=auth)
        print(code, res)
        self.assertEqual(code, 500, "code is error")
        self.assertEqual(res['message'], "The 'target vertex id' can't be null", "res is error")

    def test_param_target_typeInvalid(self):
        """
        target test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": 'invalid', "max_depth": 5},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(
            res['message'],
            "The vertex id must be formatted as Number/String/UUID, but got 'invalid'",
            "res is error"
        )

    def test_param_target_valueInvalid(self):
        """
        target test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"invalid"', "max_depth": 5},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(
            res['message'],
            "The target vertex with id 'invalid' does not exist",
            "res is error"
        )

    def test_param_maxDepth_null(self):
        """
        max_depth test
        :return:
        """
        code, res = Traverser().all_shortest_path(param={"source": '"1:josh"', "target": '"1:marko"'}, auth=auth)
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(res['message'], 'The max depth parameter must be > 0, but got 0', 'res is error')

    def test_param_maxDepth_typeInvalid(self):
        """
        max_depth test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": '"5"'},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 404, "code is error")
        self.assertEqual(res['cause'], 'java.lang.NumberFormatException: For input string: ""5""', 'res is error')

    def test_param_maxDepth_valueInvalid(self):
        """
        max_depth test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 3},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(res, {'paths': []}, 'res is error')

    def test_param_maxDepth_valueInvalid(self):
        """
        max_depth test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 3},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(res, {'paths': []}, 'res is error')

    def test_param_direction_valueOut(self):
        """
        direction: out test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "direction": "OUT"},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(res, {'paths': []}, 'res is error')

    def test_param_direction_valueIn(self):
        """
        direction: in test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "direction": "IN"},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(
            res['paths'],
            [
                {'objects': ['1:josh', '1:peter', '2:lop', '1:vadas', '1:marko']},
                {'objects': ['1:josh', '1:peter', '2:ripple', '1:vadas', '1:marko']}
            ],
            'res is error'
        )

    def test_param_direction_valueBoth(self):
        """
        direction: both test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "direction": "BOTH"},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(
            res['paths'],
            [
                {'objects': ['1:josh', '1:peter', '2:lop', '1:vadas', '1:marko']},
                {'objects': ['1:josh', '1:peter', '2:ripple', '1:vadas', '1:marko']}
            ],
            'res is error'
        )

    def test_param_label_valueNotExist(self):
        """
        label: not exist test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "label": "test"},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(res['message'], "Undefined edge label: 'test'", 'res is error')

    def test_param_label_valueInvalid(self):
        """
        label: invalid test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "label": "knows"},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(res['paths'], [], 'res is error')

    def test_param_capacity_valueInvalid(self):
        """
        capacity: invalid test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "capacity": 2},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(res['message'], 'The max degree must be < capacity', 'res is error')

    def test_param_capacity_valueNormal(self):
        """
        capacity: invalid test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "capacity": 10001},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(
            res['paths'],
            [
                {'objects': ['1:josh', '1:peter', '2:lop', '1:vadas', '1:marko']},
                {'objects': ['1:josh', '1:peter', '2:ripple', '1:vadas', '1:marko']}
            ],
            'res is error'
        )

    def test_param_maxDegree_valueNormal(self):
        """
        capacity: invalid test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "max_degree": 2, "capacity": 3},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(
            res['paths'],
            [{'objects': ['1:josh', '1:peter', '2:lop', '1:vadas', '1:marko']}],
            'res is error'
        )

    def test_param_maxDegree_valueInvalid(self):
        """
        capacity: invalid test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "max_degree": 1},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(res['paths'], [], 'res is error')

    def test_param_skipDegree_valueInvalid(self):
        """
        capacity: invalid test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "max_degree": 2, "skip_degree": 1},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 400, "code is error")
        self.assertEqual(
            res['message'],
            "The skipped degree must be >= max degree, but got skipped degree '1' and max degree '2'",
            'res is error'
        )

    def test_param_skipDegree_valueNormal(self):
        """
        capacity: invalid test
        :return:
        """
        code, res = Traverser().all_shortest_path(
            param={"source": '"1:josh"', "target": '"1:marko"', "max_depth": 4, "max_degree": 2, "skip_degree": 4},
            auth=auth
        )
        print(code, res)
        self.assertEqual(code, 200, "code is error")
        self.assertEqual(
            res['paths'],
            [{'objects': ['1:josh', '1:peter', '2:lop', '1:vadas', '1:marko']}],
            'res is error'
        )


if __name__ == "__main__":
    pass


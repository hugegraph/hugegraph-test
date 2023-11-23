# -*- coding:utf-8 -*-
"""
author     : lxb
note       : oltp算法 kneighbor计算
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


class TestKNeighbor(unittest.TestCase):
    """
    查找从起始顶点出发恰好depth步可达的顶点
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
        param_json = {'source': '"1:贾宝玉"', 'max_depth': 1}
        code, res = Traverser().get_k_neighbor(param_json=param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['vertices']), 4)
        for obj in res['vertices']:
            self.assertIn(obj, ['2:史湘云', '2:薛宝钗', '2:王夫人', '2:林黛玉'])

    def test_direction_in(self):
        """
        direction = in
        :return:
        """
        param_json = {'source': '"1:贾宝玉"', 'max_depth': 1, 'direction': 'IN'}
        code, res = Traverser().get_k_neighbor(param_json=param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['vertices'], ['2:王夫人'])

    def test_direction_out(self):
        """
        direction = out
        :return:
        """
        param_json = {'source': '"1:贾宝玉"', 'max_depth': 1, 'direction': 'OUT'}
        code, res = Traverser().get_k_neighbor(param_json=param_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['vertices']), 3)
        for obj in res['vertices']:
            self.assertIn(obj, ['2:史湘云', '2:薛宝钗', '2:林黛玉'])


class TestPostNeighbor(unittest.TestCase):
    """
    post method 查找从起始顶点出发depth步内可达的所有顶点
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
        # InsertData(gremlin='gremlin_hlm.txt').gremlin_graph()
        Gremlin().gremlin_post(
            "graph.schema().propertyKey('name').asText().ifNotExist().create();"
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
            "graph.schema().propertyKey('city').asText().ifNotExist().create();"
            "graph.schema().propertyKey('lang').asText().ifNotExist().create();"
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();"
            "graph.schema().propertyKey('price').asInt().ifNotExist().create();"
            "person = graph.schema().vertexLabel('person').properties('name', 'age', 'city')"
            ".primaryKeys('name').ifNotExist().create();"
            "software = graph.schema().vertexLabel('software').properties('name', 'lang', 'price')"
            ".primaryKeys('name').ifNotExist().create();"
            "knows = graph.schema().edgeLabel('knows').sourceLabel('person').targetLabel('person')"
            ".properties('date').ifNotExist().create();"
            "created = graph.schema().edgeLabel('created').sourceLabel('person').targetLabel('software')"
            ".properties('date', 'city').ifNotExist().create();"
            "marko = graph.addVertex(T.label, 'person', 'name', 'marko', 'age', 29, 'city', 'Beijing');"
            "vadas = graph.addVertex(T.label, 'person', 'name', 'vadas', 'age', 27, 'city', 'Hongkong');"
            "lop = graph.addVertex(T.label, 'software', 'name', 'lop', 'lang', 'java', 'price', 328);"
            "josh = graph.addVertex(T.label, 'person', 'name', 'josh', 'age', 32, 'city', 'Beijing');"
            "ripple = graph.addVertex(T.label, 'software', 'name', 'ripple', 'lang', 'java', 'price', 199);"
            "peter = graph.addVertex(T.label, 'person', 'name', 'peter', 'age', 29, 'city', 'Shanghai');"
            "li = graph.addVertex(T.label, 'person', 'name', 'li', 'age', 30, 'city', 'Beijing');"
            "zhou = graph.addVertex(T.label, 'person', 'name', 'zhou', 'age', 31, 'city', 'Tianjin');"
            "zheng = graph.addVertex(T.label, 'person', 'name', 'zheng', 'age', 32, 'city', 'Baoding');"
            "lop1 = graph.addVertex(T.label, 'software', 'name', 'lop1', 'lang', 'python', 'price', 268);"
            "marko.addEdge('knows', vadas, 'date', '2016-01-10');"
            "marko.addEdge('knows', josh, 'date', '2013-02-20');"
            "marko.addEdge('created', lop, 'date', '2017-12-10', 'city', 'Shanghai');"
            "josh.addEdge('created', ripple, 'date', '2015-10-10', 'city', 'Beijing');"
            "josh.addEdge('created', lop1, 'date', '2017-12-10', 'city', 'Beijing');"
            "peter.addEdge('created', lop, 'date', '2017-12-10', 'city', 'Beijing');"
            "li.addEdge('created', lop1, 'date', '2021-12-10', 'city', 'Shenzhen');"
            "zhou.addEdge('created', ripple, 'date', '2016-10-10', 'city', 'Beijing');"
            "li.addEdge('knows', vadas, 'date', '2021-01-10');"
            "zhou.addEdge('knows', josh, 'date', '2021-02-10');"
            "zheng.addEdge('created', ripple, 'date', '2015-10-10', 'city', 'Beijing');"
            "zheng.addEdge('knows', peter, 'date', '2021-02-10');"
        )

    def test_reqiured_params(self):
        """

        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH"
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ["2:ripple", "1:marko", "2:lop1", "1:zhou"])

    def test_edge_label_single(self):
        """

        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "edge_steps": [
                    {
                        "label": "knows"
                    }
                ]
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ["1:marko", "1:zhou"])

    def test_edge_label_more(self):
        """

        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "edge_steps": [
                    {
                        "label": "knows"
                    },
                    {
                        "label": "created"
                    }
                ]
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:ripple', '1:marko', '2:lop1', '1:zhou'])

    def test_edge_property_gt(self):
        """

        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "edge_steps": [
                    {
                        "label": "knows",
                        "properties": {
                            "date": "P.gt(2016-01-01)"
                        }
                    },
                    {
                        "label": "created",
                        "properties": {
                            "date": "P.gt(2016-01-01)"
                        }
                    }
                ]
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:lop1', '1:zhou'])

    def test_edge_property_equale(self):
        """

        :return:
        """
        body_json = {
            "source": "2:lop",
            "steps": {
                "direction": "BOTH",
                "edge_steps": [
                    {
                        "label": "created",
                        "properties": {
                            "city": "Shanghai"
                        }
                    }
                ]
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['1:marko'])

    def test_edge_property_more(self):
        """

        :return:
        """
        body_json = {
            "source": "2:lop",
            "steps": {
                "direction": "BOTH",
                "edge_steps": [
                    {
                        "label": "created",
                        "properties": {
                            "city": "Shanghai",
                            "date": "P.gt(2018-01-01)"
                        }
                    }
                ]
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], [])

    def test_edge_label_more_property(self):
        """

        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "edge_steps": [
                    {
                        "label": "knows",
                        "properties": {
                            "date": "P.gt(2016-01-01)"
                        }
                    },
                    {
                        "label": "created",
                        "properties": {
                            "date": "P.gt(2016-01-01)"
                        }
                    }
                ]
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:lop1', '1:zhou'])

    def test_edge_label_single_property(self):
        """

        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "edge_steps": [
                    {
                        "label": "knows",
                        "properties": {
                            "date": "P.gt(2016-01-01)"
                        }
                    }
                ]
            },
            "max_depth": 1
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['1:zhou'])

    def test_max_degree_1(self):
        """
        max_degree = 1
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "max_degree": 1
            },
            "max_depth": 2
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:lop1', '1:li'])

    def test_max_degree_2(self):
        """
        条件：max_degree=2
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "max_degree": 2
            },
            "max_depth": 2
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:ripple', '2:lop1', '1:li', '1:zhou'])

    def test_skip_degree(self):
        """
        条件：skip_degree >= max_degree
        :return:
        """
        body_json = {
            "source": "2:lop",
            "steps": {
                "direction": "BOTH",
                "max_degree": 2,
                "skip_degree": 3
            },
            "max_depth": 2
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['1:peter', '1:marko', '1:zheng'])

    def test_limit(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH"
            },
            "max_depth": 2,
            "limit": 3
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:ripple', '2:lop1', '1:zhou'])

    def test_count_only(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH"
            },
            "max_depth": 2,
            "limit": 3,
            "count_only": True
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], [])
        self.assertEqual(res['size'], 3)

    def test_with_path(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH"
            },
            "max_depth": 2,
            "limit": 3,
            "count_only": False,
            "with_path": True
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:ripple', '2:lop1', '1:zhou'])
        self.assertEqual(res['size'], 3)
        self.assertEqual(len(res['paths']), 3)

    def test_with_edge(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH"
            },
            "max_depth": 2,
            "limit": 3,
            "count_only": False,
            "with_edge": True
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['size'], 3)
        self.assertEqual(len(res['edges']), 3)

    def test_with_vertex_true_and_with_path_false(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH"
            },
            "max_depth": 2,
            "limit": 3,
            "count_only": False,
            "with_vertex": True,
            "with_path": False
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['size'], 3)
        self.assertEqual(len(res['vertices']), 3)

    def test_with_vertex_true_and_with_path_true(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH"
            },
            "max_depth": 2,
            "limit": 3,
            "count_only": False,
            "with_vertex": True,
            "with_path": True
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(len(res['vertices']), 4)

    def test_vertex_label_single(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "vertex_steps": [
                    {
                        "label": "software"
                    }
                ]
            },
            "max_depth": 2
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], [])

    def test_vertex_label_and_property(self):
        """
        :return:
        """
        body_json = {
            "source": "1:josh",
            "steps": {
                "direction": "BOTH",
                "vertex_steps": [
                    {
                        "label": "person",
                        "properties": {
                            "age": "P.gt(30)"
                        }
                    },
                    {
                        "label": "software"
                    }
                ]
            },
            "max_depth": 2
        }
        code, res = Traverser().post_k_neighbor(body=body_json, auth=auth)
        print(code, res)
        self.assertEqual(code, 200)
        self.assertEqual(res['kneighbor'], ['2:ripple', '2:lop1', '1:zhou', '1:zheng'])


if __name__ == "__main__":
    pass

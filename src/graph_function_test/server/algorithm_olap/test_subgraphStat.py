# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap算法 子图计算
create_time: 2020/4/22 5:17 下午
"""
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Algorithm
from src.common.task_res import get_task_res
from src.common.server_api import Gremlin
from src.common.loader import InsertData
from src.config import basic_config as _cfg
from src.common.tools import clear_graph

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class TestSubgraphStat:
    """
    weak_connected_component 接口
    """

    def setup(self):
        """
        case 开始
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用gremlin语句进行truncate操作

        InsertData(gremlin='gremlin_alg_03.txt').gremlin_graph()

    def test_subgraphStat_01(self):
        """
        :return:
        """
        body = {
            "subgraph": "graph.schema().vertexLabel('person').useCustomizeStringId().create();"
                        "graph.schema().edgeLabel('next').sourceLabel('person').targetLabel('person').create(); "
                        "g.addV('person').property(id,'A').as('a').addV('person').property(id,'B').as('b')"
                        ".addV('person').property(id,'C').as('c').addV('person').property(id,'D').as('d')"
                        ".addV('person').property(id,'E').as('e').addV('person').property(id,'F').as('f')"
                        ".addE('next').from('a').to('b').addE('next').from('b').to('c')"
                        ".addE('next').from('b').to('d').addE('next').from('c').to('d')"
                        ".addE('next').from('c').to('e').addE('next').from('d').to('e')"
                        ".addE('next').from('e').to('f').addE('next').from('f').to('d');",
            "copy_schema": False
        }
        code, res = Algorithm().post_subgraph_stat(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {'vertices_count': 6,
                              'edges_count': 8,
                              'degrees': {'D': 4, 'B': 3, 'C': 3, 'E': 3, 'F': 2, 'A': 1},
                              'stress': {'B': 10, 'D': 10, 'C': 4, 'E': 2, 'A': 0, 'F': 0},
                              'betweenness': {'B': 8.0, 'D': 7.0, 'C': 2.0, 'E': 1.0, 'A': 0.0, 'F': 0.0},
                              'eigenvectors': {'F': 29, 'E': 26, 'C': 24, 'A': 23, 'B': 23, 'D': 21},
                              'closeness': {'D': 4.5, 'B': 4.0, 'C': 4.0, 'E': 3.8333333,
                                            'F': 3.3333333, 'A': 2.6666665},
                              'page_ranks': {'D': 0.3024057078508791, 'E': 0.30239649131582375,
                                             'F': 0.27929155083329715, 'B': 0.04625000000000001,
                                             'C': 0.044656249999999995, 'A': 0.024999999999999998},
                              'cluster_coeffcient': {'edges': 8, 'vertices': 6, 'cluster_coeffcient': 0.3},
                              'rings': {'rings_count': 6}}
        else:
            assert 0


if __name__ == "__main__":
    pass

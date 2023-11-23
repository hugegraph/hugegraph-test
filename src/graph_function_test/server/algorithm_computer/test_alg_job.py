# -*- coding:utf-8 -*-
"""
author     : lxb
note       : test_alg_job
time       : 2021/11/8 10:58
"""
import unittest
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.common.server_api import Computer
from src.common.server_api import Graph
from src.common.task_res import get_algorithm_job
from src.common.server_api import Gremlin
from src.common.loader import InsertData
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class GraphCompute(unittest.TestCase):
    """
    基于k8s图计算的接口功能测试
    """

    def setup_class(self):
        """
        创建图
        """
        # 导入图数据
        cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d -g %s -f %s -s %s " \
              "--clear-all-data true  " \
              "--check-vertex false "
        res = InsertData(cmd, schema='icbc_schema.groovy', struct='icbc_struct.json', dir='icbc').load_graph()
        res.communicate()
        assert res.returncode == 0
        # 设置图的读模式
        graph_read_mode = "ALL"
        code, res = Graph().put_graph_read_mode(body=graph_read_mode, auth=auth)
        assert code == 200

    def test_triangle_count(self):
        """

        :return:
        """
        pass

    # def teardown_class(self):
    #     """
    #     修改图的读模式
    #     """
    #     graph_read_mode = "OLTP_ONLY"
    #     code, res = Graph().put_graph_read_mode(graph_read_mode, auth=auth)
    #     assert code == 200

    # def test_triangle_count(self):
    #     """
    #     图计算：三角计数
    #     """
    #     body = {
    #       "algorithm": "triangle-count",
    #       "worker": 10,
    #       "params": {
    #         "closeness_centrality.weight_property": "",
    #         "closeness_centrality.sample_rate": "0.01"
    #       }
    #     }

    # def test_rings(self):
    #     """
    #     环算法
    #     """
    #     body = {
    #         "algorithm": "rings",
    #         "worker": 10,
    #         "params": {
    #             "bsp.max_super_step": "6"
    #         }
    #     }
    #     code, res = Computer().create_computer_job(body=body, auth=auth)
    #     assert code == 201
    #     job_id = res['task_id']
    #     get_algorithm_job(job_id, auth=auth)

    # def test_pagerank(self):
    #     """
    #     pagerank 算法
    #     """
    #     body = {
    #         "algorithm": "page-rank",
    #         "worker": 10,
    #         "params": {
    #             "bsp.max_super_step": "6"
    #         }
    #     }
    #     code, res = Computer().create_computer_job(body=body, auth=auth)
    #     assert code == 201
    #     job_id = res['task_id']
    #     get_algorithm_job(job_id, auth=auth)

    # def test_degree_centrality(self):
    #     """
    #     degree-centrality算法
    #     """
    #     body = {
    #         "algorithm": "degree-centrality",
    #         "worker": 20,
    #         "params": {
    #             "degree_centrality.weight_property": ""
    #         }
    #     }
    #     # 断言异步任务状态码
    #     code, res = Computer().create_computer_job(body=body, auth=auth)
    #     assert code == 201
    #     # 断言异步任务执行结果的状态
    #     job_id = res['task_id']
    #     get_algorithm_job(job_id, auth=auth)
    #     # 断言执行结果的图属性以及属性值变化
    #     code, res = Gremlin().gremlin_post("g.V().limit(1)", auth=auth)
    #     print(code, res)


if __name__ == "__main__":
    pass


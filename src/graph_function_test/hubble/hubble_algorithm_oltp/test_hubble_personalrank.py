# -*- coding: UTF-8 -*-
"""
Created by v_changshuai01 at 2021/5/18
"""
import os
import sys
import unittest

import pytest

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg
from src.common.hubble_api import GraphConnection
from src.common.hubble_api import Gremlin
from src.common.hubble_api import ID
from src.common.hubble_api import Traverser
from src.common.tools import clear_graph


def init_graph():
    """
    对测试环境进行初始化操作
    """

    code, res = GraphConnection().get_graph_connect()
    assert code == 200
    connection_list = res['data']['records']
    for each in connection_list:
        each_id = each['id']
        each_graph = each['graph']
        each_host = each['host']
        each_port = each['port']
        # clear graph
        if _cfg.server_backend == 'cassandra':
            clear_graph(graph_name=each_graph, graph_host=each_host, graph_port=each_port)
        else:
            graph_id = ID.get_graph_id()
            Gremlin().gremlin_query({"content": 'graph.truncateBackend();'},
                                    graph_id=graph_id)  # 适用gremlin语句进行truncate操作
        # delete graph_connection
        code, res = GraphConnection().delete_graph_connect(each_id)
        assert code == 200


@pytest.mark.skipif(_cfg.hubble_version == '1.5', reason='目前只有商业版支持OLAP算法')
class TestHubblePersonalRank(unittest.TestCase):
    """
    hubble的PersonalRank算法API
    """

    def setUp(self):
        """
        每条case的前提条件
        :return:
        """
        init_graph()
        code, res = GraphConnection().add_graph_connect(body={
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        })
        self.assertEqual(code, 200, "创建图链接失败")
        self.assertEqual(res['status'], 200, "创建图链接失败")

    def test_personalRank(self):
        """
        PersonalRank推荐算法
        """
        graph_id = ID.get_graph_id()
        body = {
            "source": "林更新",
            "label": "演出",
            "alpha": 0.85,
            "max_depth": 2,
            "with_label": "SAME_LABEL",
            "degree": 3,
            "sorted": True,
            "limit": 10
        }
        code, res = Traverser.PersonalRank(body=body, graph_id=graph_id)
        print(code, res)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "PersonalRank推荐_算法返回状态码不正确")
        # self.assertEqual(res['data']['records'][0]['task_name'], body["content"], "非gremlin异步任务或者异步任务内容有误")
        # self.assertEqual(res['data']['records'][0]['task_type'], "gremlin", "非gremlin异步任务或者异步任务执行失败")


if __name__ == '__main__':
    unittest.main()

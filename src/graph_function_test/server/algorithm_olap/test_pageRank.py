# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap算法 pageRank计算
create_time: 2020/4/22 5:17 下午
"""
import pytest
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


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='目前只有商业版支持OLAP算法')
class TestPageRank:
    """
    page_rank 接口
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

    def test_pageRank_01(self):
        """
        :return:
        """
        body = {}
        code, res = Algorithm().post_page_rank(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            rank_code, rank_res = Gremlin().gremlin_post("g.V('1:marko')")
            print(rank_code, rank_res)
            assert result['last_changed_rank'] == 0.00015807441539237438 and \
                   rank_res['result']['data'][0]['properties']['r_rank'] == 0.05084635172453192
        else:
            assert 0


if __name__ == "__main__":
    pass

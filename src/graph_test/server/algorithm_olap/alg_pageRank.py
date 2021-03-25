# -*- coding:utf-8 -*-
"""
author     : lxb
note       :
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

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


class TestPageRank:
    """
    page_rank 接口
    """

    def setup(self):
        """
        case 开始
        """
        Gremlin().gremlin_post('graph.truncateBackend();')
        InsertData(gremlin='gremlin_alg_03.txt').gremlin_graph()

    @pytest.mark.caseL0
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
            assert result['last_changed_rank'] == 0.00015807441539228417 and \
                   rank_res['result']['data'][0]['properties']['r_rank'] == 0.05084635172453192
        else:
            assert 0


if __name__ == "__main__":
    pass


# -*- coding:utf-8 -*-
"""
author     : lxb
note       : olap 算法 kcore
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


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='社区版已支持 Server-OLAP 算法，等待重构开启')
class TestKCore01:
    """
    接口 kcore：K-Core 社区发现
    """

    @staticmethod
    def setup_class(self):
        """
        测试类开始
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用 gremlin 语句进行 truncate 操作

        InsertData(gremlin='gremlin_alg_06.txt').gremlin_graph()

    def test_kcore_01(self):
        """
        无参数
        :return:
        """
        body = {}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_02(self):
        """
        :return:
        """
        body = {"k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop'],
                                         ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_03(self):
        """
        :return:
        """
        body = {"direction": "BOTH", "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop'],
                                         ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_04(self):
        """
        :return:
        """
        body = {"direction": "IN", "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_05(self):
        """
        :return:
        """
        body = {"direction": "OUT", "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_06(self):
        """
        :return:
        """
        body = {"label": "created", "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_07(self):
        """
        :return:
        """
        body = {"k": 3}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_09(self):
        """
        :return:
        """
        body = {"alpha": 0.1, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_10(self):
        """
        :return:
        """
        body = {"alpha": 0.9, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_11(self):
        """
        :return:
        """
        body = {"degree": 1, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_12(self):
        """
        :return:
        """
        body = {"degree": 3, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_13(self):
        """
        :return:
        """
        body = {"merged": True, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_14(self):
        """
        :return:
        """
        body = {"merged": False, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop'],
                                         ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_15(self):
        """
        :return:
        """
        body = {"direction": "BOTH", "k": 2, "degree": 3}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_16(self):
        """
        :return:
        """
        body = {"direction": "BOTH", "k": 2, "degree": 3, "alpha": 0.6, "merged": True}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]} != {'kcores': []}
        else:
            assert 0

    def test_kcore_17(self):
        """
        校验基本参数 + alpha=0.6, merged=true
        :return:
        """
        body = {"direction": "BOTH", "k": 2, "alpha": 0.6, "merged": True}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_18(self):
        """
        校验基本参数 +alpha=0.6, merged=true,direction=IN
        :return:
        """
        body = {"direction": "IN", "k": 2, "degree": 3, "alpha": 0.6, "merged": True}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_19(self):
        """
        校验基本参数 + alpha=0.6, merged=true,direction=OUT
        :return:
        """
        body = {"direction": "OUT", "k": 3, "degree": 3, "alpha": 0.6, "merged": True}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_20(self):
        """
        校验基本参数 + alpha=0.6, merged=true,label=knows
        :return:
        """
        body = {"direction": "OUT", "k": 3, "degree": 3, "alpha": 0.6, "merged": True, "label": "knows"}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0

    def test_kcore_21(self):
        """
        :return:
        """
        body = {"workers": -1, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop'],
                                         ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_22(self):
        """
        :return:
        """
        body = {"workers": 0, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop'],
                                         ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}
        else:
            assert 0

    def test_kcore_23(self):
        """
        :return:
        """
        body = {"workers": 100, "k": 2}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': [['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop'],
                                         ['2:ripple', '1:marko', '1:josh', '1:vadas', '2:lop']]}

        else:
            assert 0

    def test_kcore_24(self):
        """
        校验基本参数 + alpha=0.6, merged=true,label=knows
        :return:
        """
        body = {"direction": "OUT", "k": 4, "degree": 3, "alpha": 0.6, "merged": True, "label": "knows", "workers": 0}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0


@pytest.mark.skipif(_cfg.graph_type == 'open_source', reason='社区版已支持 Server-OLAP 算法，等待重构开启')
class TestKCore02:
    """
    接口 kcore：K-Core 社区发现
    """

    @staticmethod
    def setup_class(self):
        """
        测试类开始
        """
        print('++++++++++++++++ start ')
        cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
              "--clear-all-data true "
        InsertData(part_cmd=cmd, schema='schema_checkVertex.groovy', struct='struct_checkVertex.json',
                   dir='network').load_graph()

    @staticmethod
    def teardown_class(self):
        """
        测试类结束
        """
        print('++++++++++++++++ end ')

    def test_kcore_01(self):
        """
        校验基本参数 + alpha=0.6, merged=true,label=knows
        :return:
        """
        body = {"direction": "BOTH", "k": 4, "degree": 3, "alpha": 0.9, "merage": True, "label": "link"}
        code, res = Algorithm().post_kcore(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 300, auth=auth)
            print(result)
            assert result == {'kcores': []}
        else:
            assert 0


if __name__ == '__main__':
    pass

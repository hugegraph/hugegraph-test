# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 梭型算法的数据集需要优化
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
class TestFusiformSimilarity:
    """
    接口fusiform_similarity：棱型发现
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

        InsertData(gremlin='gremlin_alg_04.txt').gremlin_graph()

    def test_fusiform_similarity_01(self):
        """
        无参数
        :return:
        """
        body = {}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_02(self):
        """
        :return:
        """
        body = {"source_label": "person"}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_03(self):
        """
        :return:
        """
        body = {"direction": "BOTH"}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_04(self):
        """
        :return:
        """
        body = {"direction": "OUT"}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_05(self):
        """
        :return:
        """
        body = {"direction": "IN"}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_06(self):
        """
        :return:
        """
        body = {"label": "help"}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_07(self):
        """
        :return:
        """
        body = {"min_neighbors": 2, "min_similars": 4}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            res_assert = {
                '2:lop': [
                    {'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}
                ],
                '1:vadas': [
                    {'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}
                ],
                '2:ripple': [
                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}
                ],
                '1:josh': [
                    {'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}
                ],
                '1:peter': [
                    {'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}
                ]
            }

            assert len(result) == 5
            for k, v in result.items():
                assert k in res_assert
                for obj in v:
                    assert obj in res_assert[k]
        else:
            assert 0

    def test_fusiform_similarity_08(self):
        """
        :return:
        """
        body = {"alpha": 0.8}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_09(self):
        """
        :return:
        """
        body = {"min_similars": 4}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_10(self):
        """
        :return:
        """
        body = {"top": 0}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_11(self):
        """
        :return:
        """
        body = {"top": 4}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_12(self):
        """
        :return:
        """
        body = {"group_property": ""}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            str_res = result.split("'task_result': ")[1].replace('}', '')
            assert str_res == "\"java.lang.IllegalArgumentException: The group property can't be empty\""
        else:
            assert 0

    def test_fusiform_similarity_13(self):
        """
        :return:
        """
        body = {"degree": 5}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_14(self):
        """
        :return:
        """
        body = {"capacity": 5}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_15(self):
        """
        :return:
        """
        body = {"limit": -1}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_16(self):
        """
        :return:
        """
        body = {"limit": 2}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_17(self):
        """
        基本参数校验组合
        :return:
        """
        body = {"direction": "BOTH", "min_neighbors": 2, "min_similars": 4, "degree": -1}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            res_assert = {'1:peter': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '2:lop': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:josh': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:vadas': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '2:ripple': [{'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}]}
            assert len(result) == 5
            for k, v in result.items():
                assert k in res_assert
                for obj in v:
                    assert obj in res_assert[k]
        else:
            assert 0

    def test_fusiform_similarity_18(self):
        """
        校验基本参数 + alpha=0.4, top=1
        :return:
        """
        body = {"direction": "BOTH", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "top": 1}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            res_assert = {'1:peter': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:josh': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '2:lop': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:vadas': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '2:ripple': [{'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}]}
            assert len(result) == 5
            for k, v in result.items():
                assert k in res_assert
                for obj in v:
                    assert obj in res_assert[k]
        else:
            assert 0

    def test_fusiform_similarity_19(self):
        """
        校验基本参数 + alpha=0.4, limit=1
        :return:
        """
        body = {"direction": "BOTH", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "limit": 1}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {
                '1:peter': [
                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}
                ]
            }
        else:
            assert 0

    def test_fusiform_similarity_20(self):
        """
        校验基本参数 + + alpha=0.4, top=1,direction=IN
        :return:
        """
        body = {"direction": "IN", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "top": 1}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_21(self):
        """
        校验基本参数 + + alpha=0.4, top=1,direction=OUT
        :return:
        """
        body = {"direction": "OUT", "min_neighbors": 2, "min_similars": 4, "degree": -1, "alpha": 0.4, "top": 1}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            res_assert = {'1:peter': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:vadas': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '2:ripple': [{'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '2:lop': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:josh': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}]}
            assert len(result) == 5
            for k, v in result.items():
                assert k in res_assert
                for obj in v:
                    assert obj in res_assert[k]
        else:
            assert 0

    def test_fusiform_similarity_22(self):
        """
        校验基本参数workers
        :return:
        """
        body = {"workers": -1}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_23(self):
        """
        校验基本参数workers
        :return:
        """
        body = {"workers": 0}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_24(self):
        """
        校验基本参数workers
        :return:
        """
        body = {"workers": 100}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            assert result == {}
        else:
            assert 0

    def test_fusiform_similarity_25(self):
        """
        校验基本参数 + + alpha=0.4, top=1,direction=OUT,workers=0
        :return:
        """
        body = {"direction": "OUT", "min_neighbors": 2, "min_similars": 4, "degree": -1,
                "alpha": 0.4, "top": 1, "workers": 0}
        code, res = Algorithm().post_fusiform_similarity(body, auth=auth)
        id = res["task_id"]
        if id > 0:
            result = get_task_res(id, 120, auth=auth)
            print(result)
            res_assert = {'2:lop': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                    {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:josh': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                     {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:peter': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '1:vadas': [{'id': '2:ripple', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                      {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}],
                          '2:ripple': [{'id': '1:josh', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:vadas', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '1:peter', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']},
                                       {'id': '2:lop', 'score': 1.0, 'intermediaries': ['1:lily', '1:marko']}]}
            assert len(result) == 5
            for k, v in result.items():
                assert k in res_assert
                for obj in v:
                    assert obj in res_assert[k]
        else:
            assert 0


if __name__ == '__main__':
    pass

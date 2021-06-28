# -*- coding:utf-8 -*-
"""
author     : lxb
note       : aggregate属性: 目前只有cassandra后端支持聚合属性的相关功能操作
create_time:  
"""
import pytest
import sys
import os

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../')

from src.common.server_api import Gremlin
from src.common.tools import clear_graph
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


@pytest.mark.skipif(_cfg.server_backend == 'cassandra', reason='目前只有cassandra后端支持聚合属性的相关功能操作')
class TestAggregate:
    """
    test aggregate function
    """

    def setup(self):
        """
        测试case开始
        :param self:
        :return:
        """
        if _cfg.server_backend == 'cassandra':
            clear_graph()
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 适用gremlin语句进行truncate操作

    def test_aggregate_int_max(self):
        """
        聚合属性 max
        """
        # first load
        query1 = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                 "graph.schema().propertyKey('max_num').asInt().calcMax().ifNotExist().create();" \
                 "graph.schema().vertexLabel('person').properties('name', 'max_num')" \
                 ".primaryKeys('name').ifNotExist().create();" \
                 "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                 ".properties('name', 'max_num').ifNotExist().create();" \
                 "a = graph.addVertex(T.label, 'person', 'name', 'a', 'max_num', 20160110);" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'max_num', 20210110);" \
                 "a.addEdge('link', b, 'name', 'link', 'max_num', 20211110);"
        code, res = Gremlin().gremlin_post(query1, auth=auth)
        print(code, res)
        assert code == 200

        # second load
        query2 = "a = graph.addVertex(T.label, 'person', 'name', 'a', 'max_num', 20180110);" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'max_num', 20190110);" \
                 "a.addEdge('link', b, 'name', 'link', 'max_num', 20201110);"
        code, res = Gremlin().gremlin_post(query2, auth=auth)
        print(code, res)
        assert code == 200

        # assert vertex
        code, res = Gremlin().gremlin_post("g.V()", auth=auth)
        print(code, res)
        assert code == 200
        v = res['result']['data'][0]
        if v['id'] == '1:b':
            assert v['properties']['max_num'] == 20210110
        else:
            assert v['properties']['max_num'] == 20181110

        # assert edge
        code, res = Gremlin().gremlin_post("g.E()", auth=auth)
        print(code, res)
        assert code == 200
        assert res['result']['data'][0]['properties']['max_num'] == 20211110

    def test_aggregate_int_min(self):
        """
        聚合属性 min
        """
        # first load
        query1 = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                "graph.schema().propertyKey('min_num').asInt().calcMin().ifNotExist().create();" \
                "graph.schema().vertexLabel('person').properties('name', 'min_num')" \
                ".primaryKeys('name').ifNotExist().create();" \
                "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                ".properties('name', 'min_num').ifNotExist().create();" \
                "a = graph.addVertex(T.label, 'person', 'name', 'a', 'min_num', 20160110);" \
                "b = graph.addVertex(T.label, 'person', 'name', 'b', 'min_num', 20210110);" \
                "a.addEdge('link', b, 'name', 'link', 'min_num', 20211110);"
        code, res = Gremlin().gremlin_post(query1, auth=auth)
        print(code, res)
        assert code == 200

        # second load
        query2 = "a = graph.addVertex(T.label, 'person', 'name', 'a', 'min_num', 20180110);" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'min_num', 20190110);" \
                 "a.addEdge('link', b, 'name', 'link', 'min_num', 20201110);"
        code, res = Gremlin().gremlin_post(query2, auth=auth)
        print(code, res)
        assert code == 200

        # assert vertex
        code, res = Gremlin().gremlin_post("g.V()", auth=auth)
        print(code, res)
        assert code == 200
        v = res['result']['data'][0]
        if v['id'] == '1:b':
            assert v['properties']['min_num'] == 20190110
        else:
            assert v['properties']['min_num'] == 20161110

        # assert edge
        code, res = Gremlin().gremlin_post("g.E()", auth=auth)
        print(code, res)
        assert code == 200
        assert res['result']['data'][0]['properties']['min_num'] == 20201110

    def test_aggregate_int_sum(self):
        """
        聚合属性 sum
        """
        # first load
        query1 = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                 "graph.schema().propertyKey('sum_num').asInt().calcSum().ifNotExist().create();" \
                 "graph.schema().vertexLabel('person').properties('name', 'sum_num')" \
                 ".primaryKeys('name').ifNotExist().create();" \
                 "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                 ".properties('name', 'sum_num').ifNotExist().create();" \
                 "a = graph.addVertex(T.label, 'person', 'name', 'a', 'sum_num', 20160110);" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'sum_num', 20210110);" \
                 "a.addEdge('link', b, 'name', 'link', 'sum_num', 20211110);"
        code, res = Gremlin().gremlin_post(query1, auth=auth)
        print(code, res)
        assert code == 200

        # second load
        query2 = "a = graph.addVertex(T.label, 'person', 'name', 'a', 'sum_num', 20180110);" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'sum_num', 20190110);" \
                 "a.addEdge('link', b, 'name', 'link', 'sum_num', 20201110);"
        code, res = Gremlin().gremlin_post(query2, auth=auth)
        print(code, res)
        assert code == 200

        # assert vertex
        code, res = Gremlin().gremlin_post("g.V()", auth=auth)
        print(code, res)
        assert code == 200
        v = res['result']['data'][0]
        if v['id'] == '1:b':
            assert v['properties']['sum_num'] == 40400220
        else:
            assert v['properties']['sum_num'] == 40340220

        # assert edge
        code, res = Gremlin().gremlin_post("g.E()", auth=auth)
        print(code, res)
        assert code == 200
        assert res['result']['data'][0]['properties']['sum_num'] == 40412220

    def test_aggregate_int_original(self):
        """
        聚合属性 old
        """
        # first load
        query1 = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                 "graph.schema().propertyKey('first_num').asInt().calcOld().ifNotExist().create();" \
                 "graph.schema().vertexLabel('person').properties('name', 'first_num')" \
                 ".primaryKeys('name').ifNotExist().create();" \
                 "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                 ".properties('name', 'first_num').ifNotExist().create();" \
                 "a = graph.addVertex(T.label, 'person', 'name', 'a', 'first_num', 20160110);" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'first_num', 20210110);" \
                 "a.addEdge('link', b, 'name', 'link', 'first_num', 20211110);"
        code, res = Gremlin().gremlin_post(query1, auth=auth)
        print(code, res)
        assert code == 200

        # second load
        query2 = "a = graph.addVertex(T.label, 'person', 'name', 'a', 'first_num', 20180110);" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'first_num', 20190110);" \
                 "a.addEdge('link', b, 'name', 'link', 'first_num', 20201110);"
        code, res = Gremlin().gremlin_post(query2, auth=auth)
        print(code, res)
        assert code == 200

        # assert vertex
        code, res = Gremlin().gremlin_post("g.V()", auth=auth)
        print(code, res)
        assert code == 200
        v = res['result']['data'][0]
        if v['id'] == '1:b':
            assert v['properties']['first_num'] == 20210110
        else:
            assert v['properties']['first_num'] == 20160110

        # assert edge
        code, res = Gremlin().gremlin_post("g.E()", auth=auth)
        print(code, res)
        assert code == 200
        assert res['result']['data'][0]['properties']['first_num'] == 20211110

    def test_aggregate_date_max(self):
        """
        聚合属性 max
        """
        # first load
        query1 = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                 "graph.schema().propertyKey('latest_time').asDate().calcMax().ifNotExist().create();" \
                 "graph.schema().vertexLabel('person').properties('name', 'latest_time')" \
                 ".primaryKeys('name').ifNotExist().create();" \
                 "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                 ".properties('name', 'latest_time').ifNotExist().create();" \
                 "a = graph.addVertex(T.label, 'person', 'name', 'a', 'latest_time', '2016-01-10 10:23:28');" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'latest_time', '2021-01-10 10:23:28');" \
                 "a.addEdge('link', b, 'name', 'link', 'latest_time', '2021-11-10 10:23:28');"
        code, res = Gremlin().gremlin_post(query1, auth=auth)
        print(code, res)
        assert code == 200

        # second load
        query2 = "a = graph.addVertex(T.label, 'person', 'name', 'a', 'latest_time', '2018-01-10 10:23:28');" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'latest_time', '2019-01-10 10:23:28');" \
                 "a.addEdge('link', b, 'name', 'link', 'latest_time', '2020-11-10 10:23:28');"
        code, res = Gremlin().gremlin_post(query2, auth=auth)
        print(code, res)
        assert code == 200

        # assert vertex
        code, res = Gremlin().gremlin_post("g.V()", auth=auth)
        print(code, res)
        assert code == 200
        v = res['result']['data'][0]
        if v['id'] == '1:b':
            assert v['properties']['latest_time'] == '2021-01-10 10:23:28.000'
        else:
            assert v['properties']['latest_time'] == '2018-01-10 10:23:28.000'

        # assert edge
        code, res = Gremlin().gremlin_post("g.E()", auth=auth)
        print(code, res)
        assert code == 200
        assert res['result']['data'][0]['properties']['latest_time'] == '2021-11-10 10:23:28.000'

    def test_aggregate_date_min(self):
        """
        聚合属性 min
        """
        # first load
        query1 = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                "graph.schema().propertyKey('earliest_time').asDate().calcMin().ifNotExist().create();" \
                "graph.schema().vertexLabel('person').properties('name', 'earliest_time')" \
                ".primaryKeys('name').ifNotExist().create();" \
                "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                ".properties('name', 'earliest_time').ifNotExist().create();" \
                "a = graph.addVertex(T.label, 'person', 'name', 'a', 'earliest_time', '2016-01-10 10:23:28');" \
                "b = graph.addVertex(T.label, 'person', 'name', 'b', 'earliest_time', '2021-01-10 10:23:28');" \
                "a.addEdge('link', b, 'name', 'link', 'earliest_time', '2021-11-10 10:23:28');"
        code, res = Gremlin().gremlin_post(query1, auth=auth)
        print(code, res)
        assert code == 200

        # second load
        query2 = "a = graph.addVertex(T.label, 'person', 'name', 'a', 'earliest_time', '2018-01-10 10:23:28');" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'earliest_time', '2019-01-10 10:23:28');" \
                 "a.addEdge('link', b, 'name', 'link', 'earliest_time', '2020-11-10 10:23:28');"
        code, res = Gremlin().gremlin_post(query2, auth=auth)
        print(code, res)
        assert code == 200

        # assert vertex
        code, res = Gremlin().gremlin_post("g.V()", auth=auth)
        print(code, res)
        assert code == 200
        v = res['result']['data'][0]
        if v['id'] == '1:b':
            assert v['properties']['earliest_time'] == '2019-01-10 10:23:28.000'
        else:
            assert v['properties']['earliest_time'] == '2016-11-10 10:23:28.000'

        # assert edge
        code, res = Gremlin().gremlin_post("g.E()", auth=auth)
        print(code, res)
        assert code == 200
        assert res['result']['data'][0]['properties']['earliest_time'] == '2020-11-10 10:23:28.000'

    def test_aggregate_date_original(self):
        """
        聚合属性 old
        """
        # first load
        query1 = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                 "graph.schema().propertyKey('first_time').asDate().calcOld().ifNotExist().create();" \
                 "graph.schema().vertexLabel('person').properties('name', 'first_time')" \
                 ".primaryKeys('name').ifNotExist().create();" \
                 "graph.schema().edgeLabel('link').sourceLabel('person').targetLabel('person')" \
                 ".properties('name', 'first_time').ifNotExist().create();" \
                 "a = graph.addVertex(T.label, 'person', 'name', 'a', 'first_time', '2016-01-10 10:23:28');" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'first_time', '2021-01-10 10:23:28');" \
                 "a.addEdge('link', b, 'name', 'link', 'first_time', '2021-11-10 10:23:28');"
        code, res = Gremlin().gremlin_post(query1, auth=auth)
        print(code, res)
        assert code == 200

        # second load
        query2 = "a = graph.addVertex(T.label, 'person', 'name', 'a', 'first_time', '2018-01-10 10:23:28');" \
                 "b = graph.addVertex(T.label, 'person', 'name', 'b', 'first_time', '2019-01-10 10:23:28');" \
                 "a.addEdge('link', b, 'name', 'link', 'first_time', '2020-11-10 10:23:28');"
        code, res = Gremlin().gremlin_post(query2, auth=auth)
        print(code, res)
        assert code == 200

        # assert vertex
        code, res = Gremlin().gremlin_post("g.V()", auth=auth)
        print(code, res)
        assert code == 200
        v = res['result']['data'][0]
        if v['id'] == '1:b':
            assert v['properties']['first_time'] == '2021-01-10 10:23:28.000'
        else:
            assert v['properties']['first_time'] == '2016-01-10 10:23:28.000'

        # assert edge
        code, res = Gremlin().gremlin_post("g.E()", auth=auth)
        print(code, res)
        assert code == 200
        assert res['result']['data'][0]['properties']['first_time'] == '2021-11-10 10:23:28.000'


if __name__ == "__main__":
    pass


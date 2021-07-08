# -*- coding:utf-8 -*-
"""
author     : lxb
note       : ttl功能的实现
create_time:  
"""
import pytest
import sys
import os
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../')

from src.common.server_api import Gremlin
from src.common.loader import InsertData
from src.common.tools import target_clear_graph
from src.common.tools import clear_graph
from src.common.tools import run_shell
from src.config import basic_config as _cfg


auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password

target_auth = None
if _cfg.tools_is_auth:
    target_auth = _cfg.tools_target_auth

taret_protocol = 'http'
if _cfg.tools_is_https:
    taret_protocol = 'https'


class TestTTL:
    """
    test ttl function
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

    def test_ttl_vertex_common_property(self):
        """
        gremlin接口创建图 + 顶点非date属性的ttl功能
        """
        # 插入设置ttl的数据
        Gremlin().gremlin_post(
            "graph.schema().propertyKey('name').asText().ifNotExist().create();"
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();"
            "graph.schema().vertexLabel('personA').properties('name', 'age').primaryKeys('name')"
            ".ttl(5000L).ifNotExist().create();"
            "graph.schema().vertexLabel('personB').properties('name', 'date').primaryKeys('name')"
            ".ifNotExist().create();"
            "graph.schema().edgeLabel('linkA').sourceLabel('personA').targetLabel('personA')"
            ".properties('date').ifNotExist().create();"
            "graph.schema().edgeLabel('linkB').sourceLabel('personB').targetLabel('personB')"
            ".properties('age').ifNotExist().create();"
            "marko = graph.addVertex(T.label, 'personA', 'name', 'marko', 'age', 29);"
            "peter = graph.addVertex(T.label, 'personA', 'name', 'peter', 'age', 25);"
            "vadas = graph.addVertex(T.label, 'personB', 'name', 'vadas', 'date', '2020-02-02');"
            "josh = graph.addVertex(T.label, 'personB', 'name', 'josh', 'date', '2020-02-03');",
            auth=auth
        )

        # 进行查询 线程休眠时间大于ttl的设置时间
        time.sleep(10)
        code, res = Gremlin().gremlin_post("g.V('1:marko', '1:prter')")
        print(code, res)
        assert code == 200
        assert res['result']['data'] == []

    def test_ttl_vertex_date_property(self):
        """
        gremlin接口创建图 + 顶点date属性的ttl功能
        """
        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(local_time)
        query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
            "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
            "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
            "graph.schema().vertexLabel('personA').properties('name', 'age').primaryKeys('name')" \
            ".ifNotExist().create();" \
            "graph.schema().vertexLabel('personB').properties('name', 'date').primaryKeys('name')" \
            ".ttl(5000L).ttlStartTime('date').ifNotExist().create();" \
            "graph.schema().edgeLabel('linkA').sourceLabel('personA').targetLabel('personA')" \
            ".properties('date').ifNotExist().create();" \
            "graph.schema().edgeLabel('linkB').sourceLabel('personB').targetLabel('personB')" \
            ".properties('age').ifNotExist().create();" \
            "marko = graph.addVertex(T.label, 'personA', 'name', 'marko', 'age', 29);" \
            "peter = graph.addVertex(T.label, 'personA', 'name', 'peter', 'age', 25);" \
            "vadas = graph.addVertex(T.label, 'personB', 'name', 'vadas', 'date', '%s');" \
            "josh = graph.addVertex(T.label, 'personB', 'name', 'josh', 'date', '%s');" % (local_time, local_time)

        # 插入设置ttl的数据
        Gremlin().gremlin_post(query, auth=auth)

        # 进行查询 线程休眠时间大于ttl的设置时间
        time.sleep(10)
        code, res = Gremlin().gremlin_post("g.V('2:vadas', '2:josh')")
        print(code, res)
        assert code == 200
        assert res['result']['data'] == []

    @pytest.mark.skipif(_cfg.server_backend == 'rocksdb', reason='rocksdb后端中的设置ttl，进行count()操作有bug')
    def test_ttl_use_loader(self):
        """
        ttl + loader导入
        """
        print(_cfg.server_backend)
        # 插入设置ttl的数据 顶点:艺人->ttl=5s；边:属于->ttl=5s
        gremlin = "graph.schema().propertyKey('名称').asText().ifNotExist().create();" \
                  "graph.schema().propertyKey('类型').asText().valueSet().ifNotExist().create();" \
                  "graph.schema().propertyKey('发行时间').asDate().ifNotExist().create();" \
                  "graph.schema().propertyKey('演员').asText().ifNotExist().create();" \
                  "graph.schema().vertexLabel('电影').useCustomizeStringId()" \
                  ".properties('名称','类型','发行时间').ifNotExist().create();" \
                  "graph.schema().vertexLabel('艺人').useCustomizeStringId().properties('演员')" \
                  ".ttl(5000L).ifNotExist().create();" \
                  "graph.schema().vertexLabel('类型').useCustomizeStringId().properties('类型').ifNotExist().create();" \
                  "graph.schema().vertexLabel('年份').useCustomizeStringId().properties('发行时间').ifNotExist().create();" \
                  "graph.schema().edgeLabel('导演').link('艺人','电影').ifNotExist().create();" \
                  "graph.schema().edgeLabel('演出').link('艺人','电影').ifNotExist().create();" \
                  "graph.schema().edgeLabel('属于').link('电影','类型').properties('发行时间')" \
                  ".ttl(5000L).ifNotExist().create();" \
                  "graph.schema().edgeLabel('发行于').link('电影','年份').properties('发行时间').ifNotExist().create();"
        code, res_gremlin = Gremlin().gremlin_post(gremlin, auth=auth)
        print(code, res_gremlin)
        assert 200
        assert res_gremlin['result']['data'][0]['name'] == '发行于'

        cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s "
        res = InsertData(cmd, struct='struct_movie.json', dir='movie').load_graph()
        res.communicate()
        # stdout, stderr = res.communicate()
        # print(' ---> ' + str(stdout) + ' === ' + str(stderr))

        # 进行查询 线程休眠时间大于ttl的设置时间
        time.sleep(30)
        # 断言
        code, res = Gremlin().gremlin_post("g.V().count();", auth=auth)
        assert code == 200
        assert res['result']['data'][0] != 16034    # rocksdb后端中的设置ttl，进行count()操作有bug
        code, res = Gremlin().gremlin_post("g.E().count();", auth=auth)
        assert code == 200
        assert res['result']['data'][0] == 83809   # rocksdb后端中的设置ttl，进行count()操作有bug
        code, res = Gremlin().gremlin_post("g.V('吴宇森');", auth=auth)
        assert code == 200
        assert res['result']['data'] == []
        code, res = Gremlin().gremlin_post("g.E('S铁汉柔情 > 3 >> S动作');", auth=auth)
        assert code == 200
        assert res['result']['data'] == []

    @pytest.mark.skipif(_cfg.tools_target_host == '', reason='ttl功能测试migrate场景中没有配置目标图信息')
    def test_ttl_use_migrate(self):
        """
        顶点ttl + 数据迁移
        """
        # premise = 插入设置ttl的数据 顶点:艺人->ttl=5s；边:属于->ttl=5s
        gremlin = "graph.schema().propertyKey('名称').asText().ifNotExist().create();" \
                  "graph.schema().propertyKey('类型').asText().valueSet().ifNotExist().create();" \
                  "graph.schema().propertyKey('发行时间').asDate().ifNotExist().create();" \
                  "graph.schema().propertyKey('演员').asText().ifNotExist().create();" \
                  "graph.schema().vertexLabel('电影').useCustomizeStringId()" \
                  ".properties('名称','类型','发行时间').ifNotExist().create();" \
                  "graph.schema().vertexLabel('艺人').useCustomizeStringId().properties('演员')" \
                  ".ttl(5000L).ifNotExist().create();" \
                  "graph.schema().vertexLabel('类型').useCustomizeStringId().properties('类型').ifNotExist().create();" \
                  "graph.schema().vertexLabel('年份').useCustomizeStringId().properties('发行时间').ifNotExist().create();" \
                  "graph.schema().edgeLabel('导演').link('艺人','电影').ifNotExist().create();" \
                  "graph.schema().edgeLabel('演出').link('艺人','电影').ifNotExist().create();" \
                  "graph.schema().edgeLabel('属于').link('电影','类型').properties('发行时间')" \
                  ".ttl(5000L).ifNotExist().create();" \
                  "graph.schema().edgeLabel('发行于').link('电影','年份').properties('发行时间').ifNotExist().create();"
        code, res_gremlin = Gremlin().gremlin_post(gremlin, auth=auth)
        print(code, res_gremlin)
        assert 200
        assert res_gremlin['result']['data'][0]['name'] == '发行于'

        cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s "
        res = InsertData(cmd, struct='struct_movie.json', dir='movie').load_graph()
        res.communicate()

        time.sleep(30)  # ttl 生效后进行下边操作

        code, res = Gremlin().gremlin_post("g.V('吴宇森');", auth=auth)
        assert code == 200
        assert res['result']['data'] == []
        code, res = Gremlin().gremlin_post("g.E('S铁汉柔情 > 3 >> S动作');", auth=auth)
        assert code == 200
        assert res['result']['data'] == []

        #### 数据迁移
        target_clear_graph()

        cmd = "./bin/hugegraph --url %s --graph %s %s %s migrate " \
              "--target-url %s " \
              "--target-graph %s " \
              "%s " \
              "%s " \
              "--graph-mode RESTORING "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))

        code, res = Gremlin().gremlin_post(
            "g.V('吴宇森');",
            auth=target_auth,
            host=_cfg.tools_target_host,
            port=_cfg.tools_target_port,
            protocol=taret_protocol
        )
        print(code, res)
        assert code == 200
        assert res['result']['data'] == []
        code, res = Gremlin().gremlin_post(
            "g.E('S铁汉柔情 > 3 >> S动作');",
            auth=target_auth,
            host=_cfg.tools_target_host,
            port=_cfg.tools_target_port,
            protocol=taret_protocol
        )
        print(code, res)
        assert code == 200
        assert res['result']['data'] == []

    def test_ttl_edge_common_property(self):
        """
        gremlin接口创建图 + 边非date属性的ttl功能
        """
        # 插入设置ttl的数据
        Gremlin().gremlin_post("graph.schema().propertyKey('name').asText().ifNotExist().create();"
                               "graph.schema().propertyKey('age').asInt().ifNotExist().create();"
                               "graph.schema().propertyKey('date').asDate().ifNotExist().create();"
                               "graph.schema().vertexLabel('personA').properties('name', 'age').primaryKeys('name')"
                               ".ifNotExist().create();"
                               "graph.schema().vertexLabel('personB').properties('name', 'date').primaryKeys('name')"
                               ".ifNotExist().create();"
                               "graph.schema().edgeLabel('linkA').sourceLabel('personA').targetLabel('personA')"
                               ".properties('date').ifNotExist().create();"
                               "graph.schema().edgeLabel('linkB').sourceLabel('personB').targetLabel('personB')"
                               ".properties('age').ttl(5000L).ifNotExist().create();"
                               "marko = graph.addVertex(T.label, 'personA', 'name', 'marko', 'age', 29);"
                               "peter = graph.addVertex(T.label, 'personA', 'name', 'peter', 'age', 25);"
                               "vadas = graph.addVertex(T.label, 'personB', 'name', 'vadas', 'date', '2020-02-02');"
                               "josh = graph.addVertex(T.label, 'personB', 'name', 'josh', 'date', '2020-02-03');"
                               "marko.addEdge('linkA', peter, 'date', '2020-02-04');"
                               "vadas.addEdge('linkB', josh, 'age', 99);")

        # 进行查询 线程休眠时间大于ttl的设置时间
        time.sleep(10)
        code, res = Gremlin().gremlin_post("g.E('S2:vadas>2>>S2:josh')")
        print(code, res)
        assert code == 200
        assert res['result']['data'] == []

    def test_ttl_edge_date_property(self):
        """
        gremlin接口创建图 + 边date属性的ttl功能
        """
        local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(local_time)
        query = "graph.schema().propertyKey('name').asText().ifNotExist().create();" \
                "graph.schema().propertyKey('age').asInt().ifNotExist().create();" \
                "graph.schema().propertyKey('date').asDate().ifNotExist().create();" \
                "graph.schema().vertexLabel('personA').properties('name', 'age').primaryKeys('name')" \
                ".ifNotExist().create();" \
                "graph.schema().vertexLabel('personB').properties('name', 'date').primaryKeys('name')" \
                ".ifNotExist().create();" \
                "graph.schema().edgeLabel('linkA').sourceLabel('personA').targetLabel('personA')" \
                ".properties('date').ttl(5000L).ttlStartTime('date').ifNotExist().create();" \
                "graph.schema().edgeLabel('linkB').sourceLabel('personB').targetLabel('personB')" \
                ".properties('age').ifNotExist().create();" \
                "marko = graph.addVertex(T.label, 'personA', 'name', 'marko', 'age', 29);" \
                "peter = graph.addVertex(T.label, 'personA', 'name', 'peter', 'age', 25);" \
                "vadas = graph.addVertex(T.label, 'personB', 'name', 'vadas', 'date', '2020-02-02');" \
                "josh = graph.addVertex(T.label, 'personB', 'name', 'josh', 'date', '2020-02-03');" \
                "marko.addEdge('linkA', peter, 'date', '%s');" \
                "vadas.addEdge('linkB', josh, 'age', 99);" % local_time

        # 插入设置ttl的数据
        Gremlin().gremlin_post(query)

        # 进行查询 线程休眠时间大于ttl的设置时间
        time.sleep(10)
        code, res = Gremlin().gremlin_post("g.E('S1:marko>1>>S1:peter')")
        print(code, res)
        assert code == 200
        assert res['result']['data'] == []


if __name__ == "__main__":
    pass

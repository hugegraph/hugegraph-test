 # -*- coding:utf-8 -*-
"""
author     : lxb
note       : gremlin api 测试
create_time:
"""
import os
import sys
import json

from src.common.server_api import Graph

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def test_get_graph_version():
    """
    查看图的版本信息
    仅限超级管理员操作
    """
    code, res = Graph().get_other_version(auth=auth)
    print(code, res)
    assert code == 200


def test_get_all_graphs():
    """
    列出数据库中全部的图

    """
    code, res = Graph().get_graphs(auth=auth)
    print(code, res)
    assert code == 200
    assert _cfg.graph_name in res['graphs']


def test_get_one_graph():
    """
    查看某个图的信息

    """
    code, res = Graph().get_one_graph(auth=auth)
    print(code, res)
    assert code == 200


def test_put_clear_graph():
    """
    清空某个图的全部数据，包括schema、vertex、edge和index等
    """
    body = {"action": "clear", "clear_schema": True}
    code, res = Graph().put_clear_graphs(json=body, auth=auth)
    print(code, res)
    assert code == 200


def test_get_conf():
    """
    查看某个图的配置
    """
    code, res = Graph().get_graphs_conf(auth=auth)
    print(code, res)
    assert code == 200


def test_get_graph_mode_merging():
    """
    查看某个图的模式    MERGING
    """
    # 修改图模式
    greph_mode_merging = "MERGING"
    code, res = Graph().put_graphs_mode(body=greph_mode_merging, auth=auth)
    print(code, res)
    assert code == 200

    # 查看某个图的模式
    code, res = Graph().get_graphs_mode(auth=auth)
    print(code, res)
    assert code == 200
    assert res['mode'] == "MERGING"


def test_graph_mode_restoring():
    """
       查看某个图的模式    restoring
    """
    # 修改图模式
    greph_mode_restoring = "RESTORING"
    code, res = Graph().put_graphs_mode(body=greph_mode_restoring, auth=auth)
    print(code, res)
    assert code == 200
    assert res == {"mode": "RESTORING"}

    # 查看某个图的模式
    code, res = Graph().get_graphs_mode(auth=auth)
    print(code, res)
    assert code == 200
    assert res['mode'] == "RESTORING"


def test_get_graph_mode_none():
    """
    查看某个图的模式 none
    """
    # 修改图模式
    greph_mode_merging = "NONE"
    code, res = Graph().put_graphs_mode(body=greph_mode_merging, auth=auth)
    print(code, res)
    assert code == 200

    # 查看某个图的模式
    code, res = Graph().get_graphs_mode(auth=auth)
    print(code, res)
    assert code == 200
    assert res['mode'] == "NONE"


def test_put_graph_mode():
    """
    设置图模式
    """
    greph_mode_merging = "MERGING"
    code, res = Graph().put_graphs_mode(body=greph_mode_merging, auth=auth)
    print(code, res)
    assert code == 200
    assert res == {"mode": "MERGING"}

    greph_mode_restoring = "RESTORING"
    code, res = Graph().put_graphs_mode(body=greph_mode_restoring, auth=auth)
    print(code, res)
    assert code == 200
    assert res == {"mode": "RESTORING"}

    greph_mode_none = "NONE"
    code, res = Graph().put_graphs_mode(body=greph_mode_none, auth=auth)
    print(code, res)
    assert code == 200
    assert res == {"mode": "NONE"}


def test_post_create_garph():
    """
    删除图+创建图
    """
    graph_name = 'hugegraph_tmp_lxb1'
    # create graphs
    body = {
      "gremlin.graph": "com.baidu.hugegraph.HugeFactory",
      "backend": "hstore",
      "serializer": "binary",
      "store": graph_name,
      "search.text_analyzer": "jieba",
      "search.text_analyzer_mode": "INDEX"
    }
    code, res = Graph().post_create_graph(body=body, auth=auth, graph=graph_name)
    print(code, res)
    assert code == 201
    assert res == {'name': 'hugegraph_tmp_lxb1', 'backend': 'hstore', 'description': ''}

    # delete graphs
    code, res = Graph().delete_graphs(auth=auth, graph=graph_name)
    print(code, res)
    assert code == 204


def test_get_graph_read_mode():
    """
    # 图的读模式
    """
    code, res = Graph().get_graph_read_mode(auth=auth)
    print(code, res)
    assert code == 200
    assert res['graph_read_mode'] == "OLTP_ONLY"


def test_put_graph_read_mode():
    """
    # 设置某个图的读模式
    """
    graph_read_mode = "ALL"
    code, res = Graph().put_graph_read_mode(body=graph_read_mode, auth=auth)
    print(code, res)
    assert code == 200
    assert res == {"graph_read_mode": "ALL"}

    graph_read_mode = "OLTP_ONLY"
    code, res = Graph().put_graph_read_mode(body=graph_read_mode, auth=auth)
    print(code, res)
    assert code == 200
    assert res == {"graph_read_mode": "OLTP_ONLY"}


if __name__ == "__main__":
    pass

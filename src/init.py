# -*- coding:utf-8 -*-
"""
author     : lxb
note       : tools 测试
create_time: 2020/4/22 5:17 下午
"""
import os
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../')

from src.common.server_api import Graph
from src.common.server_api import GraphSpace
from src.config import basic_config as _cfg

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password

gs_body = {
    "name": "",
    "description": "test graph space",
    "cpu_limit": 100,
    "memory_limit": 100,
    "compute_cpu_limit": 100,
    "compute_memory_limit": 100,
    "storage_limit": 100,
    "oltp_namespace": "ipipe",
    "olap_namespace": "ipipe",
    "operator_image_path": "",
    "internal_algorithm_image_url": "",
    "storage_namespace": "storage",
    "max_graph_number": 10,
    "max_role_number": 10,
    "auth": True,
    "configs": {}
}

g_body = {
    "backend": "hstore",
    "serializer": "binary",
    "store": "",
    "search.text_analyzer": "jieba",
    "search.text_analyzer_mode": "INDEX",
    "task.scheduler_type": _cfg.task_scheduler_type
}

if __name__ == '__main__':
    ### 初始化 server 的图配置 ###
    gs_body['name'] = _cfg.graph_space
    gs_body['nickname'] = "勿动_server自动化测试"
    gs_body['operator_image_path'] = _cfg.operator_image_path
    gs_body['internal_algorithm_image_url'] = _cfg.internal_algorithm_image_url
    code, res = GraphSpace().create_graph_space(body=gs_body, auth=auth)
    if code != 201 and res['message'] != "The graph space '%s' has existed" % _cfg.graph_space:
        print(code, res)
        print("_cfg.graph_space图空间创建接口报错！！！")
        os._exit(1)

    time.sleep(3)
    g_body['store'] = _cfg.graph_name
    g_body['nickname'] = "g_server"

    code, res = Graph().post_create_graph(space=_cfg.graph_space, graph=_cfg.graph_name, body=g_body, auth=auth)
    if code != 201 and res['message'] != "The graph '%s-%s' has existed" % (_cfg.graph_space, _cfg.graph_name):
        print(code, res)
        print("_cfg.graph_name图创建接口报错！！！")
        os._exit(1)

    ### 初始化tools的图配置
    gs_body['name'] = _cfg.tools_target_space
    gs_body['nickname'] = "勿动_tools自动化测试"
    code, res = GraphSpace().create_graph_space(body=gs_body, auth=auth)
    if code != 201 and res['message'] != "The graph space '%s' has existed" % _cfg.tools_target_space:
        print(code, res)
        print("_cfg.tools_target_space图空间创建接口报错！！！")
        os._exit(1)

    time.sleep(3)
    g_body['store'] = _cfg.tools_target_graph
    g_body['nickname'] = "g_tools"
    code, res = Graph().post_create_graph(
        space=_cfg.tools_target_space,
        graph=_cfg.tools_target_graph,
        body=g_body,
        auth=auth
    )
    if code != 201 and res['message'] != "The graph '%s-%s' has existed" % (
            _cfg.tools_target_space,
            _cfg.tools_target_graph
    ):
        print(code, res)
        print("_cfg.tools_target_graph图创建接口报错！！！")
        os._exit(1)

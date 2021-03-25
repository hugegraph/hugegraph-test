# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 
create_time:  
"""
import os
import sys
import subprocess

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../')
from src.config import basic_config as _cfg
from src.common.file_basic import is_match_re
from src.common.server_api import Gremlin

tools_name = is_match_re(_cfg.code_path + '/hugegraph-tools', "^hugegraph-tools-(\d).(\d{1,2}).(\d)$")
tools_path = _cfg.code_path + '/hugegraph-tools' + '/' + tools_name


def run_shell(cmd):
    """
    执行脚本
    :return:
    """
    ### source graph
    protocol = 'http'
    protocol_cmd = ""
    if _cfg.is_https:
        protocol = 'https'
        if _cfg.tools_store_file != "":
            protocol_cmd += " --trust-store-file " + _cfg.tools_store_file
        if _cfg.tools_store_password != "":
            protocol_cmd += " --trust-store-password " + _cfg.tools_store_password

    auth_cmd = ''
    if _cfg.is_auth:
        auth_cmd = ' --user admin --password %s ' % _cfg.admin_password['admin']
    url = protocol + '://' + _cfg.graph_host + ':' + str(_cfg.server_port)

    ### target graph
    run_cmd = ""
    if "migrate" in cmd:
        target_protocol = "http"
        target_protocol_cmd = ""
        if _cfg.tools_is_https:
            target_protocol = "https"
            if _cfg.tools_target_store_file != "":
                target_protocol_cmd += " --target-trust-store-file " + _cfg.tools_target_store_file
            if _cfg.tools_target_store_password != "":
                target_protocol_cmd += " --target-trust-store-password " + _cfg.tools_target_store_password

        target_auth_cmd = ''
        if _cfg.tools_is_auth:
            target_auth_cmd = ' --target-username admin --target-password %s ' % _cfg.tools_target_auth['admin']
        target_url = target_protocol + "://" + _cfg.tools_target_host + ":" + str(_cfg.tools_target_port)
        run_cmd = cmd % (url, _cfg.graph_name, protocol_cmd, auth_cmd,
                         target_url, _cfg.tools_target_graph, target_protocol_cmd, target_auth_cmd)
    else:
        print(cmd)
        run_cmd = cmd % (url, _cfg.graph_name, protocol_cmd, auth_cmd)

    print("run_cmd: " + run_cmd)
    res = subprocess.Popen('cd %s && %s' % (tools_path, run_cmd),
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    return res


def insert_data():
    """
    准备数据
    :return:
    """
    code, res = Gremlin().gremlin_post(
        "graph.schema().vertexLabel('person').useCustomizeStringId().create();"
        "graph.schema().edgeLabel('next').sourceLabel('person').targetLabel('person').create(); "
        "g.addV('person').property(id,'A').as('a')"
        ".addV('person').property(id,'B').as('b')"
        ".addV('person').property(id,'C').as('c')"
        ".addV('person').property(id,'D').as('d')"
        ".addV('person').property(id,'E').as('e')"
        ".addV('person').property(id,'F').as('f')"
        ".addE('next').from('a').to('b')"
        ".addE('next').from('b').to('c')"
        ".addE('next').from('b').to('d')"
        ".addE('next').from('c').to('d')"
        ".addE('next').from('c').to('e')"
        ".addE('next').from('d').to('e')"
        ".addE('next').from('e').to('f')"
        ".addE('next').from('f').to('d');")
    print(res)
    assert code == 200 and res['status']['code'] == 200


def tools_assert():
    """
    进行gremlin 查询
    :return:
    """
    if _cfg.is_auth:
        code_v, res_v = Gremlin().gremlin_post("g.V().count()", _cfg.admin_password)
        code_e, res_e = Gremlin().gremlin_post("g.E().count()", _cfg.admin_password)
        return res_v['result']["data"][0], res_e['result']["data"][0]
    else:
        code_v, res_v = Gremlin().gremlin_post("g.V().count()")
        code_e, res_e = Gremlin().gremlin_post("g.E().count()")
        return res_v['result']["data"][0], res_e['result']["data"][0]


def clear_graph():
    """
    清空图操作
    :return:
    """
    res = run_shell("./bin/hugegraph --url %s --graph %s %s %s graph-clear --confirm-message "
                    "\"I'm sure to delete all data\" ")
    stdout, stderr = res.communicate()
    print(' ---> ' + str(stdout) + ' === ' + str(stderr))
    assert res.returncode == 0 and \
           str(stdout, 'utf-8').startswith("Graph '%s' is cleared" % _cfg.graph_name)


def target_insert_data():
    """
    准备数据
    :return:
    """
    target_protocol = 'http'
    target_protocol_cmd = ""
    if _cfg.tools_is_https:
        target_protocol = 'https'
        if _cfg.tools_target_store_file != "":
            target_protocol_cmd += " --trust-store-file " + _cfg.tools_target_store_file
        if _cfg.tools_target_store_password != "":
            target_protocol_cmd += " --trust-store-password " + _cfg.tools_target_store_password

    target_auth_cmd = ''
    if _cfg.is_auth:
        target_auth_cmd = ' --user admin --password %s ' % _cfg.admin_password['admin']
    url = target_protocol + '://' + _cfg.tools_target_host + ':' + str(_cfg.tools_target_port)

    run_cmd = "./bin/hugegraph --url %s --graph %s %s %s gremlin-execute " \
              "--script \"graph.schema().propertyKey('name').asText().ifNotExist().create();" \
              "p = graph.schema().vertexLabel('p').properties('name').primaryKeys('name').ifNotExist().create();" \
              "k = graph.schema().edgeLabel('k').sourceLabel('p').targetLabel('p').ifNotExist().create();" \
              "marko = graph.addVertex(T.label, 'p', 'name', 'marko');" \
              "vadas = graph.addVertex(T.label, 'p', 'name', 'vadas');" \
              "marko.addEdge('k', vadas);\" " \
              % (url, _cfg.tools_target_graph, target_protocol_cmd, target_auth_cmd)
    print(run_cmd)
    res = subprocess.Popen('cd %s && %s' % (tools_path, run_cmd),
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout, stderr = res.communicate()
    print(' ---> ' + str(stdout) + ' === ' + str(stderr))
    assert res.returncode == 0


def target_clear_graph():
    """
    清空图操作
    :return:
    """
    target_protocol = 'http'
    target_protocol_cmd = ""
    if _cfg.tools_is_https:
        target_protocol = 'https'
        if _cfg.tools_target_store_file != "":
            target_protocol_cmd += " --trust-store-file " + _cfg.tools_target_store_file
        if _cfg.tools_target_store_password != "":
            target_protocol_cmd += " --trust-store-password " + _cfg.tools_target_store_password

    target_auth_cmd = ''
    if _cfg.is_auth:
        target_auth_cmd = ' --user admin --password %s ' % _cfg.admin_password['admin']
    url = target_protocol + '://' + _cfg.tools_target_host + ':' + str(_cfg.tools_target_port)

    run_cmd = "./bin/hugegraph --url %s --graph %s %s %s graph-clear --confirm-message " \
              "\"I'm sure to delete all data\" " \
              % (url, _cfg.tools_target_graph, target_protocol_cmd, target_auth_cmd)

    res = subprocess.Popen('cd %s && %s' % (tools_path, run_cmd),
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout, stderr = res.communicate()
    print(' ---> ' + str(stdout) + ' === ' + str(stderr))
    assert res.returncode == 0 and \
           str(stdout, 'utf-8').startswith("Graph '%s' is cleared" % _cfg.tools_target_graph)


if __name__ == "__main__":
    pass


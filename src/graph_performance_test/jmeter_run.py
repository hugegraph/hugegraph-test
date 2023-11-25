# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 相关测试配置项
create_time: 2022/11/14 5:17 下午
"""
import os
import time
import subprocess
import sys
import requests

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../')

from config import performance_config as p_cfg


def is_key(scene_json, scene_key):
    """
    判断 json 中是否存在key
    """
    if isinstance(scene_json, dict):
        if scene_key not in scene_json:
            for each in scene_json.items():
                flag = is_key(each[1], scene_key)
                if flag:
                    return True
            return False
        else:
            return True
    else:
        return False


def make_dir(path):
    """
    判断文件夹路径是否存在，不存在则创建
    :param path:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass


def exec_gremlin(query=None, space=None, graph=None, host=None, port=None):
    """
    执行gremlin语句
    """
    header = {"Authorization": "Basic YWRtaW46YWRtaW4=", "Content-Type": "application/json"}
    body = {
        "gremlin": query,
        "bindings": {},
        "language": "gremlin-groovy",
        "aliases": {"graph": "%s-%s" % (space, graph), "g": "__g_%s-%s" % (space, graph)}
    }
    url = "http://%s:%s/gremlin" % (host, port)
    res = requests.request('post', url, headers=header, json=body)
    print(res.status_code, res.content)
    assert (res.status_code == 200)


def run_cmd(cmd):
    """
    run jmeter
    :param cmd: 测试场景
    """
    time.sleep(10)
    try:
        res = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        res.communicate()
        assert (res.returncode == 0)
    except (SystemExit, KeyboardInterrupt):
        raise


def run_main(scene, need_pre=None):
    """
    程序主入口
    """
    # 准备环境
    if need_pre == 'yes':
        if is_key(scene, "gremlin"):
            gremlin_cmd = scene["pre_sence_env"]["gremlin"]
            if gremlin_cmd:
                print(gremlin_cmd)
                exec_gremlin(
                    query=gremlin_cmd,
                    space=p_cfg.graph_space,
                    graph=p_cfg.graph,
                    host=p_cfg.host,
                    port=p_cfg.port
                )

        if is_key(scene, "load_cmd"):
            load_cmd = scene["pre_sence_env"]["load_cmd"]
            if load_cmd:
                print(load_cmd)
                run_cmd(load_cmd)

    # 执行压测
    print(scene["jmeter_cmd"])
    run_cmd(scene["jmeter_cmd"])

    ### 分析压测报告
    # report_analysis(name, result_path + name + "/", result_path + "analysis_result.txt")


if __name__ == '__main__':
    # 创建存储压测结果的文件夹
    make_dir(p_cfg.result_path)

    print("测试场景如下:")
    print(p_cfg.scenes.keys())
    var_scene = input(
        "根据提示选择测试场景并说明是否需要执行前置条件[例如:insert_single_vertex,yes;select_vertex_byId,no]\n输入:")
    if var_scene:
        for each in var_scene.split(";"):
            if "," in each:
                each_scene = each.split(",")[0]
                need_pre = each.split(",")[1]
            else:
                each_scene = each
                need_pre = "yes"

            if each_scene in p_cfg.scenes.keys():
                run_main(p_cfg.scenes[each_scene], need_pre=need_pre)
            else:
                print("输入的测试场景: %s不存在, 请确认后重新执行" % each_scene)
    else:
        for each_scene in p_cfg.scenes.items():
            run_main(each_scene[1], need_pre='yes')

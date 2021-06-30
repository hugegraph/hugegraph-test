# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 图库测试
create_time: 2020/4/22 5:17 下午
"""
import sys
import os
import pytest

rootPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(rootPath)

from src.config import basic_config as _cfg


def test_cases(flag):
    """
    test cases
    :param flag: server、loader、hubble、tools、all
    :return:
    """
    dir_loader = '%s/src/graph_function_test/loader' % rootPath
    dir_tools = '%s/src/graph_function_test/tools' % rootPath
    dir_hubble = '%s/src/graph_function_test/hubble' % rootPath

    dir_basic = '%s/src/graph_function_test/server/basic_operation' % rootPath
    dir_ttl = '%s/src/graph_function_test/ttl' % rootPath
    dir_oltp = '%s/src/graph_function_test/server/algorithm_oltp' % rootPath
    run_list = [dir_basic, dir_ttl, dir_oltp]
    # olap算法
    if _cfg.graph_type == 'business':
        dir_olap = '%s/src/graph_function_test/server/algorithm_olap' % rootPath
        run_list.append(dir_olap)
    else:
        pass
    # 聚合属性
    if _cfg.server_backend == 'cassandra':
        dir_aggregate = '%s/src/graph_function_test/aggregate' % rootPath
        run_list.append(dir_aggregate)
    else:
        pass
    # 权限
    if _cfg.is_auth:
        dir_auth = '%s/src/graph_function_test/server/auth' % rootPath
        run_list.append(dir_auth)
    else:
        pass

    # run cases
    if flag == 'server':
        run_list.append("--html=server_test.html")
        run_list.append("--capture=tee-sys")
        pytest.main(
            run_list
        )
    elif flag == 'loader':
        pytest.main([dir_loader, "--html=loader_test.html", "--capture=tee-sys"])
    elif flag == 'tools':
        pytest.main([dir_tools, "--html=tools_test.html", "--capture=tee-sys"])
    elif flag == 'hubble':
        pytest.main([dir_hubble, "--html=hubble_test.html", "--capture=tee-sys"])
    else:
        run_list.append(dir_loader)
        run_list.append(dir_hubble)
        run_list.append(dir_tools)
        run_list.append("--html=all_test.html")
        run_list.append("--capture=tee-sys")
        pytest.main(
            run_list
        )


if __name__ == "__main__":
    param_size = len(sys.argv)
    if param_size == 2 and sys.argv[1] in ['server', 'hubble', 'tools', 'loader', 'all']:
        test_cases(sys.argv[1])
    else:
        print('---> 执行脚本参数无效,param为[server, loader, tools, hubble, all]')
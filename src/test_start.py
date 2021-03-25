# -*- coding:utf-8 -*-
"""
author     : lxb
note       : graph test
create_time: 2020/4/22 5:17 下午
"""
import sys
import os

rootPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(rootPath)

from src.config import basic_config as _cfg


def start_test(param):
    """
    start testing
    """
    if param == 'server':
        cmd_ttl = 'pytest %s/src/graph_test/ttl/ttl.py --html=ttl-test.html --capture=tee-sys' % rootPath
        os.system(cmd_ttl)

        cmd_olap = 'pytest %s/src/graph_test/server/algorithm_olap ' \
                   '--html=alg_olap-test.html ' \
                   '--capture=tee-sys' % rootPath
        os.system(cmd_olap)

        cmd_basic_operation = 'pytest %s/src/graph_test/server/basic_operation ' \
                              '--html=basic_operation-test.html ' \
                              '--capture=tee-sys' % rootPath
        os.system(cmd_basic_operation)

        # backend: cassandra, test aggregate_property
        if _cfg.server_backend == 'cassandra':
            cmd_aggregate = 'pytest %s/src/graph_test/aggregate/basic_operation ' \
                                  '--html=aggregate-test.html ' \
                                  '--capture=tee-sys' % rootPath
            os.system(cmd_aggregate)
        else:
            pass

        # test auth
        if _cfg.is_auth:
            cmd_auth = 'pytest  %s/src/graph_test/server/auth --html=auth-test.html --capture=tee-sys' % rootPath
            os.system(cmd_auth)
        else:
            pass

    elif param == 'loader':
        cmd = 'pytest %s/src/graph_test/loader/loader_test.py --html=loader-test.html --capture=tee-sys' % rootPath
        os.system(cmd)
    elif param == 'tools':
        cmd = 'pytest %s/src/graph_test/tools/tools_test.py --html=tools-test.html --capture=tee-sys' % rootPath
        os.system(cmd)
    elif param == 'hubble':
        cmd = 'pytest %s/src/graph_test/hubble/hubble_test.py --html=hubble-test.html --capture=tee-sys' % rootPath
        os.system(cmd)
    else:
        pass


if __name__ == "__main__":
    param_size = len(sys.argv)
    if param_size == 2 \
            and sys.argv[1] in ['server', 'loader', 'tools', 'hubble']:
        start_test(sys.argv[1])
    else:
        print('---> 执行脚本参数无效,param为[server,loader,tools,hubble]')

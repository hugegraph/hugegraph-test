# -*- coding:utf-8 -*-
"""
author     : lxb
note       : hugegraph 各组件部署
create_time: 2020/4/22 5:17 下午
"""
import sys
import os

rootPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(rootPath)

from src.common.deploy_graph import Deploy
from src.config import basic_config


def graph_deploy(param, conf_obj):
    """
    get package & install package
    :param conf_obj:
    :param param: all、server、toolchain
    """
    if param == 'server':
        Deploy.server(conf_obj)
    elif param == 'toolchain':
        Deploy.toolchain(conf_obj)
    elif param == 'pd':
        Deploy.pd(conf_obj)
    elif param == 'store':
        Deploy.store(conf_obj)
    elif param == 'hugegraph':
        Deploy.hugegraph(conf_obj)
    else:
        Deploy.pd(conf_obj)
        Deploy.store(conf_obj)
        Deploy.server(conf_obj)
        Deploy.toolchain(conf_obj)


if __name__ == "__main__":
    param_size = len(sys.argv)
    if param_size == 2 \
            and sys.argv[1] in ['all', 'server', 'toolchain', 'pd', 'store', 'hugegraph']:
        basic_config.server_backend = 'rocksdb'
        graph_deploy(sys.argv[1], basic_config)
    elif param_size == 3 \
            and sys.argv[1] in ['all', 'server', 'toolchain', 'pd', 'store', 'hugegraph']\
            and sys.argv[2] in ['hbase', 'hstore', 'cassandra', 'mysql', 'rocksdb', 'scylladb']:
        basic_config.server_backend = sys.argv[2]
        graph_deploy(sys.argv[1], basic_config)
    else:
        print('failed: 执行脚本参数为[all,server,toolchain, pd, store, hugegraph]')
        exit(1)

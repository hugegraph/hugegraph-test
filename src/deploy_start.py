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
    else:
        Deploy.server(conf_obj)
        Deploy.toolchain(conf_obj)


if __name__ == "__main__":
    param_size = len(sys.argv)
    if param_size == 2 \
            and sys.argv[1] in ['all', 'server', 'toolchain']:
        graph_deploy(sys.argv[1], basic_config)
    else:
        print('failed: 执行脚本参数为[all,server,toolchain]')
        exit(1)

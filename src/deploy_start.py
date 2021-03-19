# -*- coding:utf-8 -*-
"""
author     : lxb
note       : Component deployment begins
create_time: 2020/4/22 5:17 下午
"""
import sys
import os

rootPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(rootPath)

from src.graph_deploy.deploy_graph import Deploy
from src.config import basic_config


def graph_deploy(param, conf_obj):
    """
    get package & install package
    :param conf_obj:
    :param param: all、server、loader、tools、hubble
    """
    if param == 'server':
        Deploy.server(conf_obj)
    elif param == 'loader':
        Deploy.loader(conf_obj)
    elif param == 'tools':
        Deploy.tools(conf_obj)
    elif param == 'hubble':
        Deploy.hubble(conf_obj)
    else:
        Deploy.server(conf_obj)
        Deploy.loader(conf_obj)
        Deploy.tools(conf_obj)
        Deploy.hubble(conf_obj)


if __name__ == "__main__":
    param_size = len(sys.argv)
    if param_size == 2 \
       and sys.argv[1] in ['all', 'server', 'loader', 'tools', 'hubble']:
        graph_deploy(sys.argv[1], basic_config)
    else:
        print('---> 执行脚本参数为1个,param为[all,server,loader,tools,hubble]')

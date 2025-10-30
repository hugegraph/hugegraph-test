# -*- coding:utf-8 -*-
"""
author     : lxb
note       : hugegraph 各组件部署
create_time: 2020/4/22 5:17 下午
"""
import sys
import os
import re

rootPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
sys.path.append(rootPath)

from src.common.deploy_graph import Deploy
from src.config import basic_config

def validate_memory_param(param_name, value):
    try:
        memory_mb = int(value)
    except ValueError:
        raise ValueError(f"param {param_name} must be number，current: {value}")

    if memory_mb <= 0:
        raise ValueError(f"param {param_name} must greater than 0，current: {value}")

    if memory_mb > 32768:
        raise ValueError(f"param {param_name} can not exceed 32768MB (32GB)，current: {value}")
    
    return memory_mb

# 显示使用说明
def show_usage():
    """显示使用说明"""
    print("使用方法:")
    print("  python deploy_start.py [部署类型] [后端类型] [内存参数...]")
    print("  ")
    print("部署类型:")
    print("  all      : 部署所有组件")
    print("  server   : 部署服务器组件")
    print("  toolchain: 部署工具链组件")
    print("  pd       : 部署PD组件")
    print("  store    : 部署Store组件")
    print("  hugegraph: 部署完整的HugeGraph")
    print("  ")
    print("后端类型 (可选):")
    print("  hbase, cassandra, hstore, mysql, rocksdb, scylladb")
    print("  ")
    print("JVM内存参数 (可选):")
    print("  --server-xms=N    : 设置服务器组件初始堆内存(MB)，默认1024")
    print("  --server-xmx=N    : 设置服务器组件最大堆内存(MB)，默认2048")
    print("  --pd-xms=N        : 设置PD组件初始堆内存(MB)，默认512")
    print("  --pd-xmx=N        : 设置PD组件最大堆内存(MB)，默认1024")
    print("  --store-xms=N     : 设置Store组件初始堆内存(MB)，默认1024")
    print("  --store-xmx=N     : 设置Store组件最大堆内存(MB)，默认2048")
    print("  ")
    print("示例:")
    print("  python deploy_start.py hugegraph rocksdb --server-xms=2048 --server-xmx=4096")
    print("  python deploy_start.py server --server-xms=1024 --server-xmx=2048")
    print("  ")
    print("注意事项:")
    print("  - 内存参数值必须是大于0的整数")
    print("  - 推荐将最大堆内存设置为初始堆内存的2倍或更多")
    print("  - 请确保系统有足够的内存来支持设置的值")


def update_jvm_memory_config(args):
    updated_count = 0

    memory_param_pattern = re.compile(r'--(\w+)-(xms|xmx)=(\d+)')

    components = {'server', 'pd', 'store'}
    
    for arg in args:
        match = memory_param_pattern.match(arg)
        if match:
            component = match.group(1)
            param_type = match.group(2)
            value = match.group(3)

            if component not in components:
                raise ValueError(f"unsupported component: {component}，supported: {', '.join(components)}")

            valid_value = validate_memory_param(f"--{component}-{param_type}", value)

            config_attr = f"{component}_jvm_{param_type}"
            if hasattr(basic_config, config_attr):
                setattr(basic_config, config_attr, valid_value)
                print(f"update {component} component {param_type.upper()} to {valid_value}MB")
                updated_count += 1
            else:
                raise ValueError(f"unknown config: {config_attr}")
    
    return updated_count

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
        Deploy.server(conf_obj)
        Deploy.toolchain(conf_obj)


if __name__ == "__main__":
    try:
        param_size = len(sys.argv)

        if param_size >= 2 and sys.argv[1] in ['-h', '--help']:
            show_usage()
            exit(0)

        if param_size < 2 or sys.argv[1] not in ['all', 'server', 'toolchain', 'pd', 'store', 'hugegraph']:
            show_usage()
            exit(1)
        
        deploy_type = sys.argv[1]

        backend_arg_index = 2
        if param_size > 2 and sys.argv[2] in ['hbase', 'hstore', 'cassandra', 'mysql', 'rocksdb', 'scylladb']:
            basic_config.server_backend = sys.argv[2]
            print(f"set backend to: {sys.argv[2]}")
            backend_arg_index = 3
        else:
            print(f"use default backend: {basic_config.server_backend}")

        if param_size > backend_arg_index:
            memory_args = sys.argv[backend_arg_index:]
            updated_count = update_jvm_memory_config(memory_args)
            if updated_count > 0:
                print(f"update {updated_count} amount of JVM config")

        print("deploy start...")
        graph_deploy(deploy_type, basic_config)
        print("deploy complete!")
        
    except ValueError as e:
        print(f"wrong param: {str(e)}")
        print("use --help to check")
        exit(1)
    except Exception as e:
        print(f"error when deploy: {str(e)}")
        exit(1)

# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 相关测试配置项
create_time: 2020/4/22 5:17 下午
"""
import os.path

# local codebase
codebase_path = os.path.dirname(os.path.realpath(__file__)) + "/../../graph"

# apache release version
is_incubating = 'incubating-'
server_release_version = '1.5.0'
toolchain_release_version = '1.2.0'
server_local_repo = 'hugegraph'
toolchain_local_repo = 'hugegraph-toolchain'
server_gen_dir = f'hugegraph/hugegraph-server/apache-hugegraph-{is_incubating}{server_release_version}'
toolchain_gen_dir = f'hugegraph-toolchain/apache-hugegraph-toolchain-{is_incubating}{toolchain_release_version}'
toolchain_obj_template = 'apache-hugegraph-{tool_name}-' + is_incubating + f'{toolchain_release_version}'

server_path = os.path.join(codebase_path, server_local_repo)
toolchain_path = os.path.join(codebase_path, toolchain_local_repo)
loader_path = os.path.join(codebase_path, toolchain_gen_dir, toolchain_obj_template.format(tool_name='loader'))
hubble_path = os.path.join(codebase_path, toolchain_gen_dir, toolchain_obj_template.format(tool_name='hubble'))
tools_path = os.path.join(codebase_path, toolchain_gen_dir, toolchain_obj_template.format(tool_name='tools'))

# common
is_auth = False
is_https = False

# server
server_git = {
    'branch': '47aa8be8508293bbda76c93b461292efc84a75c7',
    'url': 'https://github.com/apache/hugegraph.git'
}
graph_type = 'open_source'  # open_source || business

server_port = 8080
server_backend = 'rocksdb'
gremlin_port = 8182
graph_host = '127.0.0.1'
graph_name = 'hugegraph'

# 测试使用的权限配置
admin_password = {'admin': 'admin'}
test_password = {'tester': '123456'}

# toolchain (includes loader, hubble, tools)
toolchain_git = {
    'branch': '8ce8b2bf7d6cc0b1f716e852fca03e38ce857682',
    'url': 'https://github.com/apache/hugegraph-toolchain.git'
}

# loader
loader_store_file = ""
loader_store_password = ""

# tools
tools_is_auth = False
tools_is_https = False

tools_target_host = ""
tools_target_port = None
tools_target_graph = ""

tools_store_file = ""
tools_store_password = ""
tools_target_store_file = ""
tools_target_store_password = ""
tools_target_auth = {}

# hubble
hubble_host = '127.0.0.1'
hubble_port = 8088
hubble_reuse_server_host = ''
hubble_reuse_server_port = ''
hubble_reuse_server_graph = ''

if __name__ == "__main__":
    pass

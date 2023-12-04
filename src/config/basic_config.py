# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 相关测试配置项
create_time: 2020/4/22 5:17 下午
"""
import os.path

# code_path = '/home/runner/work/hugegraph-test/hugegraph-test/graph'
code_path = os.path.dirname(os.path.realpath(__file__)) + "/../../graph"

is_auth = True
is_https = False

# server
server_git = {
    'branch': 'master',
    'url': 'https://github.com/apache/incubator-hugegraph.git'
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

# toolchain
toolchain_git = {
    'branch': 'master',
    'url': 'https://github.com/apache/incubator-hugegraph-toolchain.git'
}

# loader
loader_git = {'branch': 'master', 'url': 'https://github.com/hugegraph/hugegraph-loader.git'}
loader_store_file = ""
loader_store_password = ""

# tools
tools_git = {'branch': 'master', 'url': 'https://github.com/hugegraph/hugegraph-tools.git'}
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
hubble_git = {'branch': 'master', 'url': 'https://github.com/hugegraph/hugegraph-hubble.git'}
hubble_host = '127.0.0.1'
hubble_port = 8088
hubble_reuse_server_host = ''
hubble_reuse_server_port = ''
hubble_reuse_server_graph = ''

if __name__ == "__main__":
    pass

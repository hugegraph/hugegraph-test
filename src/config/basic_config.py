# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 相关测试配置项
create_time: 2020/4/22 5:17 下午
"""
import os.path

code_path = os.path.dirname(os.path.realpath(__file__)) + "/../../graph"

is_auth = False
is_https = False

# server
server_git = {
    # 'branch': 'master',
    'branch': '20d1e5228e39bd974079891fc713574fb14798c5',
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
    'branch': 'b066b805630ca591809cfee2da2aae1395fc6b42',
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

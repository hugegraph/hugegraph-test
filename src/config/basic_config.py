# -*- coding:utf-8 -*-
"""
author     : lxb
note       : properties
create_time: 2020/4/22 5:17 下午
"""
# hugegraph deploy
server_git = {'branch': 'master', 'url': 'https://github.com/hugegraph/hugegraph.git'}
hubble_git = {'branch': 'master', 'url': 'https://github.com/hugegraph/hugegraph-hubble.git'}
loader_git = {'branch': 'master', 'url': 'https://github.com/hugegraph/hugegraph-loader.git'}
tools_git = {'branch': 'master', 'url': 'https://github.com/hugegraph/hugegraph-tools.git'}
code_path = '/home'
mvn_path = '/usr/local/maven-3.6.3/bin/'  # 为空字符串的时候即已经配置mvn的环境变量
graph_host = '127.0.0.1'
server_port = 8080
server_backend = 'rocksdb'
gremlin_port = 8081
graph_name = 'hugegraph'
hubble_port = 8088
is_auth = False
admin_password = {}
is_https = False


# server_test_auth
test_password = {}

# loader_test_auth
loader_store_file = ""
loader_store_password = ""

# tools_test_auth_https
tools_is_auth = False
tools_is_https = False
tools_target_host = ""
tools_target_port = 8080
tools_target_graph = "hugegraph1"
tools_store_file = ""
tools_store_password = ""
tools_target_store_file = ""
tools_target_store_password = ""
tools_target_auth = {}

if __name__ == "__main__":
    pass

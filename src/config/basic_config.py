# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 相关测试配置项
create_time: 2020/4/22 5:17 下午
"""
import os

code_path = os.path.dirname(os.path.realpath(__file__)) + "/../../graph"

### server ###
# gremlin_port = 8515
server_backend = 'hstore'

is_auth = True
is_auth_divide = False
is_https = False
server_port = 8080
pd_peer = "10.xx.12.66:8386"
operator_image_path = "10.xx.12.61/kgs_bd/hugegraph-computer-operator:3.1.18"
internal_algorithm_image_url = "10.xx.12.61/kgs_bd/hugegraph-computer-algorithm:3.1.18"
graph_host = '10.xx.12.66'
graph_space = 'ipipe'
graph_name = 'ipipe_g1'
admin_password = {"admin": "admin"}
test_password = {"tester": "123456"}
task_scheduler_type = "distributed"
# auth
auth_graph = "ipipe_g2"

# loader
loader_store_file = ""
loader_store_password = ""

# tools
tools_is_auth = True
tools_is_https = False
tools_target_host = "10.xx.12.66"
tools_target_port = 8080
tools_target_space = 'ipipe'
tools_target_graph = "ipipe_g3"
tools_store_file = ""
tools_store_password = ""
tools_target_store_file = ""
tools_target_store_password = {}
tools_target_auth = {"admin": "admin"}

# hubble
hubble_host = ''
hubble_port = 8088


if __name__ == "__main__":
    pass

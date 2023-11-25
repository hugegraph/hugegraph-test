# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 性能测试相关测试配置
create_time: 2022/12/01 5:17 下午 
"""
import time

current_time = time.strftime("%Y%m%d%H%M")
# 图配置
host = "10.45.30.211"
port = "8080"
pd_url = "10.45.30.211:8686"
graph_space = "DEFAULT"
graph = "lxb1"
# jmx脚本路径
jmx_path = "/home/disk1/lxb/jmeter_3.6/hugegraph-integration/src/config/jmx"
# jmeter 路径
jmeter_path = "/home/disk1/lxb/apache-jmeter-5.4/bin/jmeter"
# 测试结果路径包含: jtl 和 测试报告
result_path = "/home/disk1/lxb/jmeter_3.6/hugegraph-integration/src/config/jmx/result"
# 数据集存储路径
data_path = "/home/disk1/test-dataset/api-dataset"
# loader 组件路径
load_path = "/home/disk1/lxb/hugegraph-loader-3.6.0-SNAPSHOT"
# 测试场景
scenes = {
    # 单条插入顶点
    "insert_single_vertex": {
        "pre_sence_env": {
            "gremlin": "graph.truncateBackend();"
                       "graph.schema().vertexLabel('node').useCustomizeNumberId().ifNotExist().create();"
        },
        "jmeter_cmd": "%s -n -t %s/single_add_vertex.jmx "
                      "-Jhost=%s "
                      "-Jport=%s "
                      "-JrequestType=POST "
                      "-Jurl=/graphspaces/%s/graphs/%s/graph/vertices  "
                      "-Jdata=%s/vertices "
                      "-JallThreads=1000 "
                      "-JstartThreads=900 "
                      "-JstepThreads=100 "
                      "-JstepTime=120  "
                      "-l %s/insert_single_vertex_%s.jtl "
                      "-e -o %s/insert_single_vertex_%s/" % (
                          jmeter_path,
                          jmx_path,
                          host,
                          port,
                          graph_space,
                          graph,
                          data_path,
                          result_path,
                          current_time,
                          result_path,
                          current_time
                      )
    },
    # 批量插入顶点
    "insert_batch_vertex": {
        "pre_sence_env": {
            "gremlin": "graph.truncateBackend();"
                       "graph.schema().vertexLabel('node').useCustomizeNumberId().ifNotExist().create();"
        },
        "jmeter_cmd": "%s -n -t %s/batch_add_vertex.jmx "
                      "-Jhost=%s "
                      "-Jport=%s "
                      "-JrequestType=POST "
                      "-Jurl=/graphspaces/%s/graphs/%s/graph/vertices/batch  "
                      "-Jdata=%s/vertexBatch "
                      "-JallThreads=1200 "
                      "-JstartThreads=200 "
                      "-JstepThreads=100 "
                      "-JstepTime=120  "
                      "-l %s/insert_batch_vertex_%s.jtl "
                      "-e -o %s/insert_batch_vertex_%s/" % (
                          jmeter_path,
                          jmx_path,
                          host,
                          port,
                          graph_space,
                          graph,
                          data_path,
                          result_path,
                          current_time,
                          result_path,
                          current_time
                      )
    },

    # # 批量插入带有属性顶点
    # "insert_batch_vertex_withProperty": {
    #     "pre_sence_env": {
    #         "gremlin": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # # 批量插入带有索引的顶点
    # "insert_batch_vertex_withSecondaryIndex": {
    #     "pre_sence_env": {
    #         "gremlin": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # # 单条插入边
    # "insert_single_edge": {
    #     "pre_sence_env": {
    #         "gremlin": "",
    #         "load_cmd": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # # 批量插入边
    # "insert_batch_edge": {
    #     "pre_sence_env": {
    #         "gremlin": "",
    #         "load_cmd": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # 根据ID查询顶点
    "select_vertex_byId": {
        "pre_sence_env": {
            "load_cmd": "%s/bin/hugegraph-loader.sh "
                        "-h %s "
                        "-p %s "
                        "--graphspace %s "
                        "-g %s "
                        "-f /home/disk1/lxb/twitter_14e/struct_twitter.json "
                        "-s /home/disk1/lxb/twitter_14e/schema_twitter.groovy "
                        "--print-progress false "
                        "--incremental-mode false "
                        "--batch-size 2000 "
                        "--batch-insert-threads 128 "
                        "--max-insert-errors 100000 "
                        "--retry-times 10 "
                        "--parallel-count 20 "
                        "--direct true "
                        "--use-prefilter true "
                        "--pd-peers %s "
                        "--clear-all-data true" % (load_path, host, port, graph_space, graph, pd_url)
        },
        "jmeter_cmd": "%s -n -t %s/get_vertex_by_id.jmx "
                      "-Jhost=%s "
                      "-Jport=%s "
                      "-JrequestType=GET "
                      "-Jurl=/graphspaces/%s/graphs/%s/graph/vertices  "
                      "-Jdata=%s/twitter/v.txt "
                      "-JallThreads=1300 "
                      "-JstartThreads=600 "
                      "-JstepThreads=100 "
                      "-JstepTime=120  "
                      "-l %s/get_vertex_by_id_%s.jtl "
                      "-e -o %s/get_vertex_by_id_%s/" % (
                          jmeter_path,
                          jmx_path,
                          host,
                          port,
                          graph_space,
                          graph,
                          data_path,
                          result_path,
                          current_time,
                          result_path,
                          current_time
                      )
    },
    # # 根据 id、direction、property、label 组合查询顶点
    # "select_vertex_by_more": {
    #     "pre_sence_env": {
    #         "gremlin": "",
    #         "load_cmd": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # # 根据ID查询边
    # "select_edge_byId": {
    #     "pre_sence_env": {
    #         "gremlin": "",
    #         "load_cmd": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # # 根据 id、direction、property、label 组合查询边
    # "select_edge_by_more": {
    #     "pre_sence_env": {
    #         "gremlin": "",
    #         "load_cmd": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # kout算法查询
    "k_out": {
        "pre_sence_env": {
            "load_cmd": ""
        },
        "jmeter_cmd": "%s -n -t %s/kout.jmx "
                      "-Jhost=%s "
                      "-Jport=%s "
                      "-JrequestType=GET "
                      "-Jurl=/graphspaces/%s/graphs/%s/traversers/kout  "
                      "-Jdata=%s/twitter/v.txt "
                      "-JallThreads=160 "
                      "-JstartThreads=40 "
                      "-JstepThreads=20 "
                      "-JstepTime=120  "
                      "-l %s/kout_%s.jtl "
                      "-e -o %s/kout_%s/" % (
                          jmeter_path,
                          jmx_path,
                          host,
                          port,
                          graph_space,
                          graph,
                          data_path,
                          result_path,
                          current_time,
                          result_path,
                          current_time
                      )
    },
    # # kneighbor算法查询
    # "k_neighbor": {
    #     "pre_sence_env": {
    #         "gremlin": "",
    #         "load_cmd": ""
    #     },
    #     "jmeter_cmd": ""
    # },
    # # kneighbor算法查询
    # "shortest_path": {
    #     "pre_sence_env": {
    #         "gremlin": "",
    #         "load_cmd": ""
    #     },
    #     "jmeter_cmd": ""
    # }
}

if __name__ == "__main__":
    print(current_time)
    print(scenes["insert_single_vertex"]["jmeter_cmd"])

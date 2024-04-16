# -*- coding:utf-8 -*-
"""
author     : lxb
note       : server的api请求
create_time: 2020/4/22 5:17 下午
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../..')

from src.config import basic_config as _cfg
from src.common.request_cls import Request


class Traverser:
    """
    oltp接口
    """
    def all_shortest_path(self, param=None, auth=None):
        """
        全最短路径
        :param param:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/allshortestpaths" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param)
        return code, res

    def get_k_out(self, param_json, auth=None):
        """
        通过get方法进行 k_out
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/kout" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_k_neighbor(self, param_json, auth=None):
        """
        通过get方法进行 k_neighbor
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/kneighbor" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_shortestPath(self, param_json, auth=None):
        """
        通过get方法进行 shortestPath
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/shortestpath" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_weighted_shortestPath(self, param_json, auth=None):
        """
        通过get方法进行 weighted shortestPath
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/weightedshortestpath" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_single_source_shortestPath(self, param_json, auth=None):
        """
        通过get方法进行 single source shortestPath
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/singlesourceshortestpath" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_template_paths(self, json, auth=None):
        """
        通过post方法进行 template paths
        :param json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/templatepaths" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=json)
        return code, res

    def post_multi_node_shortestPath(self, json, auth=None):
        """
        通过post方法进行 multi node shortest path
        :param json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/multinodeshortestpath" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=json)
        return code, res

    def get_paths(self, param_json, auth=None):
        """
        通过get方法获取两个点间的所有路径
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/paths" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_paths(self, body, auth=None):
        """
        通过post方法获取两个点间的所有路径
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/paths" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_customized_paths(self, json, auth=None):
        """
        通过post方法进行 customized paths
        :param json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/customizedpaths" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=json)
        return code, res

    def get_vertices(self, part_url, auth=None):
        """
        根据批量ID获取顶点
        :param auth:
        :param part_url:
        :return:
        """
        url = "/graphs/%s/traversers/vertices%s" % (_cfg.graph_name, part_url)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_edges(self, part_url, auth=None):
        """
        :param auth:
        :param part_url:
        :return:
        """
        url = "/graphs/%s/traversers/edges%s" % (_cfg.graph_name, part_url)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_rings(self, param_json, auth=None):
        """
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/rings" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_rays(self, param_json, auth=None):
        """
        根据起始顶点、方向、边的类型（可选）和最大深度等条件查找发散到边界顶点的路径
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/rays" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_crosspoints(self, param_json, auth=None):
        """
        根据起始顶点、目的顶点、方向、边的类型（可选）和最大深度等条件查找相交点
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/crosspoints" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_customized_crosspoints(self, body, auth=None):
        """
        根据一批起始顶点、多种边规则（包括方向、边的类型和属性过滤）和最大深度等条件查找符合条件的所有的路径终点的交集
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/customizedcrosspoints" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_fusiform_similarity(self, body, auth=None):
        """
        按照条件查询一批顶点对应的"梭形相似点"
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/fusiformsimilarity" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_vertex_shard(self, param_json, auth=None):
        """
        通过指定的分片大小split_size，获取顶点分片信息（可以与 Scan 配合使用来获取顶点）
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/vertices/shards" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_shard_vertex(self, param_json, auth=None):
        """
        通过指定的分片信息批量查询顶点
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/vertices/scan" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_edge_shard(self, param_json, auth=None):
        """
        通过指定的分片大小split_size，获取边分片信息（可以与 Scan 配合使用来获取边）
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/edges/shards" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_shard_edge(self, param_json, auth=None):
        """
        通过指定的分片信息批量查询边
        :param param_json:
        :param auth:
        :return:
        """
        url = "/graphs/%s/traversers/edges/scan" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res


class Task:
    """
    task接口
    """

    def get_task(self, id, auth=None):
        """
        查看某个异步任务
        :param auth:
        :param id: taskId
        :return:
        """
        url = "/graphs/%s/tasks/%d" % (_cfg.graph_name, id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_tasks(self, param, auth=None):
        """
        获取所有的异步任务
        :param auth:
        """
        url = "/graphs/%s/tasks" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=param)
        return code, res

    def put_task(self, task_id, auth=None):
        """
        验证:task写权限 (取消task)
        :return:
        """
        url = "/graphs/%s/tasks/%s?action=cancel" % (_cfg.graph_name, task_id)
        code, res = Request(auth=auth).request(method='put', path=url)
        return code, res

    def delete_task(self, task_id, auth=None):
        """
        验证:task 删除权限
        :return:
        """
        url = "/graphs/%s/tasks/%s" % (_cfg.graph_name, task_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res


class Schema:
    """
    schema 接口
    """
    def create_property(self, body, auth=None):
        """
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/propertykeys" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_all_properties(self, auth=None):
        """
        :param auth:
        """
        url = "/graphs/%s/schema/propertykeys" % _cfg.graph_name
        code, res = Request(auth=auth).request(method="get", path=url)
        return code, res

    def get_property_by_name(self, name, auth=None):
        """
        :param name:
        :param auth:
        """
        url = "/graphs/%s/schema/propertykeys/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method="get", path=url)
        return code, res

    def delete_property_by_name(self, name, auth=None):
        """
        :param name:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/propertykeys/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def deal_property_userdata(self, name, param, body, auth=None):
        """
        :param body:
        :param param:
        :param name:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/propertykeys/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(params=param, json=body, method='put', path=url)
        return code, res

    def create_vertexLabel(self, body, auth=None):
        """
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/vertexlabels" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_vertexLabel(self, property_name, param_json, body, auth=None):
        """
        :param param_json:
        :param property_name:
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/vertexlabels/%s" % (_cfg.graph_name, property_name)
        code, res = Request(auth=auth).request(method='put', params=param_json, path=url, json=body)
        return code, res

    def get_vertexLabel(self, auth=None):
        """
        查看所有 vertexLabel
        :return:
        """
        url = "/graphs/%s/schema/vertexlabels" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_vertexLabel_by_name(self, name, auth=None):
        """
        查看某个 vertexLabel
        :return:
        """
        url = "/graphs/%s/schema/vertexlabels/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_vertexLabel(self, name, auth=None):
        """
        删除VertexLabel
        :return:
        """
        url = "/graphs/%s/schema/vertexlabels/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def create_edgeLabel(self, body, auth=None):
        """
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/edgelabels" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_edgeLabel(self, property_name, param_json, body, auth=None):
        """
        :param property_name:
        :param param_json:
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/edgelabels/%s" % (_cfg.graph_name, property_name)
        code, res = Request(auth=auth).request(method='put', params=param_json, path=url, json=body)
        return code, res

    def get_edgeLabel(self, auth=None):
        """
        查看所有EdgeLabel
        :return:
        """
        url = "/graphs/%s/schema/edgelabels" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_edgeLabel_by_name(self, property_name, auth=None):
        """
        根据name查看EdgeLabel
        :return:
        """
        url = "/graphs/%s/schema/edgelabels/%s" % (_cfg.graph_name, property_name)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_edgeLabel(self, name, auth=None):
        """
        删除edgeLabel
        :return:
        """
        url = "/graphs/%s/schema/edgelabels/" % _cfg.graph_name + name
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def create_index(self, body, auth=None):
        """
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/schema/indexlabels" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_index(self, auth=None):
        """
        查看IndexLabel
        :return:
        """
        url = "/graphs/%s/schema/indexlabels" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_index_by_name(self, name, auth=None):
        """
        通过name查看IndexLabel
        :return:
        """
        url = "/graphs/%s/schema/indexlabels/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_index(self, name, auth=None):
        """
        删除indexLabel
        :return:
        """
        url = "/graphs/%s/schema/indexlabels/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res


class Gremlin:
    """
    gremlin 接口
    """

    def gremlin_post(self, query, host=None, port=None, protocol=None, auth=None):
        """
        同步的gremlin查询
        :param protocol:
        :param port:
        :param host:
        :param auth:
        :param query:
        :return:
        """
        body = {
            "gremlin": query,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s" % _cfg.graph_name, "g": "__g_%s" % _cfg.graph_name}
        }
        
        url = "/gremlin"
        code, res = Request(host=host, port=port, protocol=protocol, auth=auth)\
            .request(method='post', path=url, json=body)
        # print(code, res)
        return code, res

    def gremlin_job(self, query, auth=None):
        """
        异步的gremlin查询
        :param auth:
        :param query:
        :return:
        """
        body = {
            "gremlin": query,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {}
        }
        
        url = "/graphs/%s/jobs/gremlin" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def gremlin_get(self, param, auth=None):
        """
        同步的gremlin的get请求
        :param param: get的请求参数
        :param auth:
        :return:
        """
        url = "/gremlin"
        code, res = Request(auth=auth).request(method='get', path=url, params=param)
        return code, res


class Algorithm:
    """
    set algorithm
    """
    def post_count_vertex(self, body, auth=None):
        """
        统计顶点信息
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/count_vertex" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_count_edge(self, body, auth=None):
        """
        统计边信息
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/count_edge" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_degree_centrality(self, body, auth=None):
        """
        度中心性
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/degree_centrality" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_eigenvector_centrality(self, body, auth=None):
        """
        特征中心性
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/eigenvector_centrality" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_betweeness_centrality(self, body, auth=None):
        """
        中介中心性
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/betweenness_centrality" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_closeness_centrality(self, body, auth=None):
        """
        紧密中心性
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/closeness_centrality" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_triangle_count(self, body, auth=None):
        """
        三角形计数
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/triangle_count" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_cluster_coefficient(self, body, auth=None):
        """
        聚类系数
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/cluster_coefficient" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_lpa(self, body, auth=None):
        """
        lpa社区发现
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/lpa" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_louvain(self, body, auth=None):
        """
        louvain社区发现
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/louvain" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_kcore(self, body, auth=None):
        """
        kcore社区发现
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/k_core" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_fusiform_similarity(self, body, auth=None):
        """
        模型发现
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/fusiform_similarity" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_rings_detect(self, body, auth=None):
        """
        环路检测
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/rings" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_page_rank(self, body, auth=None):
        """
        顶点权重rank值
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/page_rank" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_weak_connected_component(self, body, auth=None):
        """
        弱联通子图
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/weak_connected_component" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_subgraph_stat(self, body, auth=None):
        """
        子图查询
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/subgraph_stat" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_stress_centrality(self, body, auth=None):
        """
        重力中心性
        :param auth:
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/stress_centrality" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res


class Auth:
    """
    权限接口
    """
    def post_targets(self, body, auth=None):
        """
        创建资源
        :return:
        """
        url = "/graphs/%s/auth/targets" % _cfg.graph_name
        # print(url)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_targets(self, auth=None):
        """
        查看资源
        :return:
        """
        url = "/graphs/%s/auth/targets" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_target(self, target_id, auth=None):
        """
        查看资源
        :return:
        """
        url = "/graphs/%s/auth/targets/%s" % (_cfg.graph_name, target_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_targets(self, target_id, auth=None):
        """
        删除资源
        :return:
        """
        url = "/graphs/%s/auth/targets/%s" % (_cfg.graph_name, target_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_targets(self, body, target_id, auth=None):
        """
        更新targets
        :return:
        """
        url = "/graphs/%s/auth/targets/%s" % (_cfg.graph_name, target_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_groups(self, body, auth=None):
        """
        创建组
        :return:
        """
        url = "/graphs/%s/auth/groups" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_groups(self, auth=None):
        """
        获取用户组
        :return:
        """
        url = "/graphs/%s/auth/groups" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_group(self, group_id, auth=None):
        """
        获取用户组
        :return:
        """
        url = "/graphs/%s/auth/groups/%s" % (_cfg.graph_name, group_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_groups(self, group_id, auth=None):
        """
        删除用户组
        :return:
        """
        url = "/graphs/%s/auth/groups/%s" % (_cfg.graph_name, group_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_groups(self, body, groups_id, auth=None):
        """
        更新groups
        :return:
        """
        url = "/graphs/%s/auth/groups/%s" % (_cfg.graph_name, groups_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_accesses(self, body, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/%s/auth/accesses" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_access(self, access_id, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/%s/auth/accesses/%s" % (_cfg.graph_name, access_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_accesses(self, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/%s/auth/accesses" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_accesses(self, access_id, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/%s/auth/accesses/%s" % (_cfg.graph_name, access_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_accesses(self, body, access_id, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/%s/auth/accesses/%s" % (_cfg.graph_name, access_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_users(self, body, auth=None):
        """
        创建用户
        :return:
        """
        url = "/graphs/%s/auth/users" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_users(self, user_id, auth=None):
        """
        删除用户
        :return:
        """
        url = "/graphs/%s/auth/users/%s" % (_cfg.graph_name, user_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def get_users_role(self, user_id, auth=None):
        """
        获取用户权限
        :return:
        """
        url = "/graphs/%s/auth/users/%s/role" % (_cfg.graph_name, user_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_users(self, auth=None):
        """
        验证:查看用户列表
        :return:
        """
        url = "/graphs/%s/auth/users" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_user(self, user_id, auth=None):
        """
        验证:查看用户列表
        :return:
        """
        url = "/graphs/%s/auth/users/%s" % (_cfg.graph_name, user_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def update_users(self, body, user_id, auth=None):
        """
        更新user
        :return:
        """
        url = "/graphs/%s/auth/users/%s" % (_cfg.graph_name, user_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_belongs(self, body, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphs/%s/auth/belongs" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_belongs(self, belong_id, auth=None):
        """
        删除 绑定组
        :return:
        """
        url = "/graphs/%s/auth/belongs/%s" % (_cfg.graph_name, belong_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def get_belongs(self, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphs/%s/auth/belongs" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_belong(self, belong_id, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphs/%s/auth/belongs/%s" % (_cfg.graph_name, belong_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def update_belongs(self, body, belong_id, auth=None):
        """
        更新 belong
        :return:
        """
        url = "/graphs/%s/auth/belongs/%s" % (_cfg.graph_name, belong_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res


class Graph:
    """
    图的基本接口
    """
    def get_graphs(self, auth=None):
        """
        列出数据库中全部的图
        :return:
        """
        url = "/graphs"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def put_graphs_mode(self, body, auth=None):
        """
        查看某个图的模式
        :return:
        """
        url = "/graphs/%s/mode" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def get_one_graph(self, auth=None):
        """
        查看某个图的模式
        :param auth:
        :return:
        """
        url = "/graphs/%s" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res


class Variable:
    """
    Variables可以用来存储有关整个图的数据，数据按照键值对的方式存取
    """
    def list_var(self, auth=None):
        """
        验证:var读
        :return:
        """
        url = "/graphs/%s/variables" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_var(self, key, auth=None):
        """
        验证:var读
        :return:
        """
        url = "/graphs/%s/variables/%s" % (_cfg.graph_name, key)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def put_var(self, body, name, auth=None):
        """
        验证:var写
        :return:
        """
        url = "/graphs/%s/variables/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def delete_var(self, name, auth=None):
        """
        验证:var 删除
        :return:
        """
        url = "/graphs/%s/variables/%s" % (_cfg.graph_name, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res


class Vertex:
    """
    vertex opertaion
    """
    def create_single_vertex(self, body, auth=None):
        """
        创建单个顶点
        :return:
        """
        url = "/graphs/%s/graph/vertices" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def create_batch_vertex(self, body, auth=None):
        """
        创建批量顶点
        :return:
        """
        url = "/graphs/%s/graph/vertices/batch" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_vertex_batch_property(self, body, auth=None):
        """
        批量更新顶点属性
        :return:
        """
        url = "/graphs/%s/graph/vertices/batch" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def update_vertex_property(self, v_id, action, body, auth=None):
        """
        删除||增加||更新 顶点属性
        :return:
        """
        url = "/graphs/%s/graph/vertices/%s" % (_cfg.graph_name, v_id)
        code, res = Request(auth=auth).request(method='put', path=url, params=action, json=body)
        return code, res

    def get_filter_vertex(self, condition=None, auth=None):
        """
        获取符合条件的顶点
        :return:
        """
        url = "/graphs/%s/graph/vertices" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=condition)
        return code, res

    def get_vertex_by_id(self, v_id, auth=None):
        """
        通过ID获取顶点
        :param v_id:
        :param auth:
        :return:
        """
        url = "/graphs/%s/graph/vertices/%s" % (_cfg.graph_name, v_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_vertex(self, v_id, label=None, auth=None):
        """
        通过顶点、顶点类型删除顶点
        :param v_id:
        :param label:
        :param auth:
        """
        url = "/graphs/%s/graph/vertices/%s" % (_cfg.graph_name, v_id)
        print(url)
        code, res = Request(auth=auth).request(method='delete', path=url, params=label)
        return code, res


class Edge:
    """
    edge operation
    """
    def create_single_edge(self, body, auth=None):
        """
        创建单条边
        :return:
        """
        url = "/graphs/%s/graph/edges" % _cfg.graph_name
        print(url)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def create_batch_edge(self, body, auth=None):
        """
        批量创建边
        :param body: 请求body
        :param auth: 权限
        :return:
        """
        url = "/graphs/%s/graph/edges/batch" % _cfg.graph_name
        print(url)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_edge_batch_property(self, body, auth=None):
        """
        批量更新属性
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/graph/edges/batch" % _cfg.graph_name
        print(url)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def change_edge_property(self, e_id, action, body, auth=None):
        """
        删除||更新||新增 边属性
        :param e_id: 边ID
        :param action:
        :param body:
        :param auth:
        :return:
        """
        url = "/graphs/%s/graph/edges/%s" % (_cfg.graph_name, e_id)
        print(url)
        code, res = Request(auth=auth).request(method='put', path=url, params=action, json=body)
        return code, res

    def get_filter_edge(self, condition=None, auth=None):
        """
        根据条件查询边
        :return:
        """
        url = "/graphs/%s/graph/edges" % _cfg.graph_name
        code, res = Request(auth=auth).request(method='get', path=url, params=condition)
        return code, res

    def get_edge_by_id(self, e_id, auth=None):
        """
        通过ID获取边
        :return:
        """
        url = "/graphs/%s/graph/edges/%s" % (_cfg.graph_name, e_id)
        print(url)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_edge(self, v_id, label=None, auth=None):
        """
        验证:edge 删除权限
        :return:
        """
        url = "/graphs/%s/graph/edges/%s" % (_cfg.graph_name, v_id)
        print(url)
        code, res = Request(auth=auth).request(method='delete', path=url, params=label)
        return code, res


if __name__ == "__main__":
    pass



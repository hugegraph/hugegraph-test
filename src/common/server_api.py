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

    def all_shortest_path(self, space=None, graph=None, param=None, auth=None):
        """
        全最短路径
        :param graph:
        :param space:
        :param param:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/allshortestpaths" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param)
        return code, res

    def get_k_out(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过get方法进行 k_out
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/kout" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_k_out(self, space=None, graph=None, body=None, auth=None):
        """
        通过post方法进行 k_out
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/kout" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_k_neighbor(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过get方法进行 k_neighbor
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/kneighbor" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_k_neighbor(self, space=None, graph=None, body=None, auth=None):
        """
        通过post方法进行 k_neighbor
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/kneighbor" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_shortestPath(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过get方法进行 shortestPath
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/shortestpath" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_weighted_shortestPath(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过get方法进行 weighted shortestPath
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/weightedshortestpath" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_single_source_shortestPath(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过get方法进行 single source shortestPath
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/singlesourceshortestpath" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_template_paths(self, space=None, graph=None, json=None, auth=None):
        """
        通过post方法进行 template paths
        :param graph:
        :param space:
        :param json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/templatepaths" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=json)
        return code, res

    def post_multi_node_shortestPath(self, space=None, graph=None, json=None, auth=None):
        """
        通过post方法进行 multi node shortest path
        :param graph:
        :param space:
        :param json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/multinodeshortestpath" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=json)
        return code, res

    def get_paths(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过get方法获取两个点间的所有路径
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/paths" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_paths(self, space=None, graph=None, body=None, auth=None):
        """
        通过post方法获取两个点间的所有路径
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/paths" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_customized_paths(self, space=None, graph=None, json=None, auth=None):
        """
        通过post方法进行 customized paths
        :param graph:
        :param space:
        :param json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/customizedpaths" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=json)
        return code, res

    def get_vertices(self, space=None, graph=None, part_url=None, auth=None):
        """
        根据批量ID获取顶点
        :param graph:
        :param space:
        :param auth:
        :param part_url:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/vertices%s" % (space, graph, part_url)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_edges(self, space=None, graph=None, part_url=None, auth=None):
        """
        :param graph:
        :param space:
        :param auth:
        :param part_url:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/edges%s" % (space, graph, part_url)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_rings(self, space=None, graph=None, param_json=None, auth=None):
        """
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/rings" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_rays(self, space=None, graph=None, param_json=None, auth=None):
        """
        根据起始顶点、方向、边的类型（可选）和最大深度等条件查找发散到边界顶点的路径
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/rays" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_crosspoints(self, space=None, graph=None, param_json=None, auth=None):
        """
        根据起始顶点、目的顶点、方向、边的类型（可选）和最大深度等条件查找相交点
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/crosspoints" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def post_customized_crosspoints(self, space=None, graph=None, body=None, auth=None):
        """
        根据一批起始顶点、多种边规则（包括方向、边的类型和属性过滤）和最大深度等条件查找符合条件的所有的路径终点的交集
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/customizedcrosspoints" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def post_fusiform_similarity(self, space=None, graph=None, body=None, auth=None):
        """
        按照条件查询一批顶点对应的"梭形相似点"
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/fusiformsimilarity" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_vertex_shard(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过指定的分片大小split_size，获取顶点分片信息（可以与 Scan 配合使用来获取顶点）
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/vertices/shards" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_shard_vertex(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过指定的分片信息批量查询顶点
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/vertices/scan" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_edge_shard(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过指定的分片大小split_size，获取边分片信息（可以与 Scan 配合使用来获取边）
        :param graph:
        :param space:
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/edges/shards" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res

    def get_shard_edge(self, space=None, graph=None, param_json=None, auth=None):
        """
        通过指定的分片信息批量查询边
        :param param_json:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/traversers/edges/scan" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param_json)
        return code, res


class Task:
    """
    task接口
    """

    def get_task(self, space=None, graph=None, id=None, auth=None):
        """
        查看某个异步任务
        :param graph:
        :param space:
        :param auth:
        :param id: taskId
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/tasks/%d" % (space, graph, id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_tasks(self, space=None, graph=None, param=None, auth=None):
        """
        获取所有的异步任务
        :param graph:
        :param space:
        :param auth:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/tasks" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param)
        return code, res

    def put_task(self, space=None, graph=None, task_id=None, auth=None):
        """
        验证:task写权限 (取消task)
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/tasks/%s?action=cancel" % (space, graph, task_id)
        code, res = Request(auth=auth).request(method='put', path=url)
        return code, res

    def delete_task(self, space=None, graph=None, task_id=None, auth=None):
        """
        删除task
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/tasks/%s" % (space, graph, task_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def compulsory_delete_task(self, space=None, graph=None, task_id=None, auth=None):
        """
        验证:task 删除权限
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/tasks/%s?force=true" % (space, graph, task_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res


class Schema:
    """
    schema 接口
    """

    def get_schema(self, space=None, graph=None, param=None, auth=None):
        """
        获取schema信息
        :param graph:
        :param space:
        :param param:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=param)
        return code, res

    def create_property(self, space=None, graph=None, body=None, auth=None):
        """
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/propertykeys" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_all_properties(self, space=None, graph=None, auth=None):
        """
        :param graph:
        :param space:
        :param auth:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/propertykeys" % (space, graph)
        code, res = Request(auth=auth).request(method="get", path=url)
        return code, res

    def get_property_by_name(self, space=None, graph=None, name=None, auth=None):
        """
        :param graph:
        :param space:
        :param name:
        :param auth:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/propertykeys/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method="get", path=url)
        return code, res

    def delete_property_by_name(self, space=None, graph=None, name=None, auth=None):
        """
        :param graph:
        :param space:
        :param name:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/propertykeys/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def deal_property_userdata(self, space=None, graph=None, name=None, param=None, body=None, auth=None):
        """
        :param body:
        :param param:
        :param name:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/propertykeys/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(params=param, json=body, method='put', path=url)
        return code, res

    def create_vertexLabel(self, space=None, graph=None, body=None, auth=None):
        """
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/vertexlabels" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_vertexLabel(self, space=None, graph=None, property_name=None, param_json=None, body=None, auth=None):
        """
        :param graph:
        :param space:
        :param param_json:
        :param property_name:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/vertexlabels/%s" % (space, graph, property_name)
        code, res = Request(auth=auth).request(method='put', params=param_json, path=url, json=body)
        return code, res

    def get_vertexLabel(self, space=None, graph=None, auth=None):
        """
        查看所有 vertexLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/vertexlabels" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_vertexLabel_by_name(self, space=None, graph=None, name=None, auth=None):
        """
        查看某个 vertexLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/vertexlabels/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_vertexLabel(self, space=None, graph=None, name=None, auth=None):
        """
        删除VertexLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/vertexlabels/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def create_edgeLabel(self, space=None, graph=None, body=None, auth=None):
        """
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/edgelabels" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_edgeLabel(self, space=None, graph=None, property_name=None, param_json=None, body=None, auth=None):
        """
        :param graph:
        :param space:
        :param property_name:
        :param param_json:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/edgelabels/%s" % (space, graph, property_name)
        code, res = Request(auth=auth).request(method='put', params=param_json, path=url, json=body)
        return code, res

    def get_edgeLabel(self, space=None, graph=None, auth=None):
        """
        查看所有EdgeLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/edgelabels" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_edgeLabel_by_name(self, space=None, graph=None, property_name=None, auth=None):
        """
        根据name查看EdgeLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/edgelabels/%s" % (space, graph, property_name)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_edgeLabel(self, space=None, graph=None, name=None, auth=None):
        """
        删除edgeLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/edgelabels/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def create_index(self, space=None, graph=None, body=None, auth=None):
        """
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/indexlabels" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_index(self, space=None, graph=None, auth=None):
        """
        查看IndexLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/indexlabels" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_index_by_name(self, space=None, graph=None, name=None, auth=None):
        """
        通过name查看IndexLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/indexlabels/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_index(self, space=None, graph=None, name=None, auth=None):
        """
        删除indexLabel
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/schema/indexlabels/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res


class Gremlin:
    """
    gremlin 接口
    """

    def gremlin_post(self, query, host=None, port=None, space=None, graph=None, protocol=None, auth=None):
        """
        同步的gremlin查询
        :param space:
        :param graph:gremlin_post
        :param protocol:
        :param port:
        :param host:
        :param auth:
        :param query:
        :return:
        """
        if graph is None:
            graph = _cfg.graph_name

        if space is None:
            space = _cfg.graph_space

        body = {
            "gremlin": query,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {"graph": "%s-%s" % (space, graph), "g": "__g_%s-%s" % (space, graph)}
        }

        url = "/gremlin"
        code, res = Request(host=host, port=port, protocol=protocol, auth=auth) \
            .request(method='post', path=url, json=body)
        return code, res

    def gremlin_job(self, space=None, graph=None, query=None, auth=None):
        """
        异步的gremlin查询
        :param graph:
        :param space:
        :param auth:
        :param query:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/jobs/gremlin" % (space, graph)
        body = {
            "gremlin": query,
            "bindings": {},
            "language": "gremlin-groovy",
            "aliases": {}
        }
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

    def post_cluster_coeffcient(self, body, auth=None):
        """
        聚类系数
        :param auth: 
        :param body:
        :return:
        """
        url = "/graphs/%s/jobs/algorithm/cluster_coeffcient" % _cfg.graph_name
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


class AuthGH:
    """
    权限接口
    """

    def post_targets(self, body, auth=None):
        """
        创建资源
        :return:
        """
        url = "/graphs/auth/targets"
        # print(url)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_targets(self, auth=None):
        """
        查看资源
        :return:
        """
        url = "/graphs/auth/targets"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_target(self, target_id, auth=None):
        """
        查看资源
        :return:
        """
        url = "/graphs/auth/targets/%s" % target_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_targets(self, target_id, auth=None):
        """
        删除资源
        :return:
        """
        url = "/graphs/auth/targets/%s" % target_id
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_targets(self, body, target_id, auth=None):
        """
        更新targets
        :return:
        """
        url = "/graphs/auth/targets/%s" % target_id
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_groups(self, body, auth=None):
        """
        创建组
        :return:
        """
        url = "/graphs/auth/groups"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_groups(self, auth=None):
        """
        获取用户组
        :return:
        """
        url = "/graphs/auth/groups"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_group(self, group_id, auth=None):
        """
        获取用户组
        :return:
        """
        url = "/graphs/auth/groups/%s" % group_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_groups(self, group_id, auth=None):
        """
        删除用户组
        :return:
        """
        url = "/graphs/auth/groups/%s" % group_id
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_groups(self, body, groups_id, auth=None):
        """
        更新groups
        :return:
        """
        url = "/graphs/auth/groups/%s" % groups_id
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_accesses(self, body, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/auth/accesses"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_access(self, access_id, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/auth/accesses/%s" % access_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_accesses(self, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/auth/accesses"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_accesses(self, access_id, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/auth/accesses/%s" % access_id
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_accesses(self, body, access_id, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphs/auth/accesses/%s" % access_id
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_users(self, body, auth=None):
        """
        创建用户
        :return:
        """
        url = "/graphs/auth/users"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_users(self, user_id, auth=None):
        """
        删除用户
        :return:
        """
        url = "/graphs/auth/users/%s" % user_id
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def get_users_role(self, user_id, auth=None):
        """
        获取用户权限
        :return:
        """
        url = "/graphs/auth/users/%s/role" % user_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_users(self, auth=None):
        """
        验证:查看用户列表
        :return:
        """
        url = "/graphs/auth/users"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_user(self, user_id, auth=None):
        """
        验证:查看用户列表
        :return:
        """
        url = "/graphs/auth/users/%s" % user_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def update_users(self, body, user_id, auth=None):
        """
        更新user
        :return:
        """
        url = "/graphs/auth/users/%s" % user_id
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_belongs(self, body, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphs/auth/belongs"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_belongs(self, belong_id, auth=None):
        """
        删除 绑定组
        :return:
        """
        url = "/graphs/auth/belongs/%s" % belong_id
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def get_belongs(self, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphs/auth/belongs"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_belong(self, belong_id, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphs/auth/belongs/%s" % belong_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def update_belongs(self, body, belong_id, auth=None):
        """
        更新 belong
        :return:
        """
        url = "/graphs/auth/belongs/%s" % belong_id
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_token(self, body, auth=None):
        """
        login token
        :return:
        """
        url = "/graphs/auth/login"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_verify(self, header, auth=None):
        """
        验证token
        :return:
        """
        url = "/graphs/auth/verify"
        print(header)
        code, res = Request(auth=auth).request(method='get', path=url, headers=header)
        return code, res


class AuthGHV3:
    """
    权限接口
    """

    def post_targets(self, body, graph_space=_cfg.graph_space, auth=None):
        """
        创建资源
        :return:
        """
        url = "/graphspaces/%s/auth/targets" % graph_space
        # print(url)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_targets(self, graph_space=_cfg.graph_space, auth=None):
        """
        查看资源
        :return:
        """
        url = "/graphspaces/%s/auth/targets" % graph_space
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_target(self, target_id, graph_space=_cfg.graph_space, auth=None):
        """
        查看资源
        :return:
        """
        url = "/graphspaces/%s/auth/targets/%s" % (graph_space, target_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_targets(self, target_id, graph_space=_cfg.graph_space, auth=None):
        """
        删除资源
        :return:
        """
        url = "/graphspaces/%s/auth/targets/%s" % (graph_space, target_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_targets(self, body, target_id, graph_space=_cfg.graph_space, auth=None):
        """
        更新targets
        :return:
        """
        url = "/graphspaces/%s/auth/targets/%s" % (graph_space, target_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_groups(self, body, graph_space=_cfg.graph_space, auth=None):
        """
        创建组
        :return:
        """
        url = "/graphspaces/%s/auth/groups" % graph_space
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_groups(self, graph_space=_cfg.graph_space, auth=None):
        """
        获取用户组
        :return:
        """
        url = "/graphspaces/%s/auth/groups" % graph_space
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_group(self, group_id, graph_space=_cfg.graph_space, auth=None):
        """
        获取用户组
        :return:
        """
        url = "/graphspaces/%s/auth/groups/%s" % (graph_space, group_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_groups(self, group_id, graph_space=_cfg.graph_space, auth=None):
        """
        删除用户组
        :return:
        """
        url = "/graphspaces/%s/auth/groups/%s" % (graph_space, group_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_groups(self, body, groups_id, graph_space=_cfg.graph_space, auth=None):
        """
        更新groups
        :return:
        """
        url = "/graphspaces/%s/auth/groups/%s" % (graph_space, groups_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_accesses(self, body, graph_space=_cfg.graph_space, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphspaces/%s/auth/accesses" % graph_space
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_access(self, access_id, graph_space=_cfg.graph_space, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphspaces/%s/auth/accesses/%s" % (graph_space, access_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_accesses(self, graph_space=_cfg.graph_space, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphspaces/%s/auth/accesses" % graph_space
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_accesses(self, access_id, graph_space=_cfg.graph_space, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphspaces/%s/auth/accesses/%s" % (graph_space, access_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def update_accesses(self, body, access_id, graph_space=_cfg.graph_space, auth=None):
        """
        创建group到target的连接 并给group赋权
        :return:
        """
        url = "/graphspaces/%s/auth/accesses/%s" % (graph_space, access_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_users(self, body, auth=None):
        """
        创建用户
        :return:
        """
        url = "/auth/users"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_users(self, user_id, auth=None):
        """
        删除用户
        :return:
        """
        url = "/auth/users/%s" % user_id
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def get_users_role(self, user_id, auth=None):
        """
        获取用户权限
        :return:
        """
        url = "/auth/users/%s/role" % user_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_users(self, auth=None):
        """
        验证:查看用户列表
        :return:
        """
        url = "/auth/users"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_user(self, user_id, auth=None):
        """
        验证:查看某个用户的信息
        :return:
        """
        url = "/auth/users/%s" % user_id
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def update_users(self, body, user_id, auth=None):
        """
        更新user
        :return:
        """
        url = "/auth/users/%s" % user_id
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_belongs(self, body, graph_space=_cfg.graph_space, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphspaces/%s/auth/belongs" % graph_space
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_belongs(self, belong_id, graph_space=_cfg.graph_space, auth=None):
        """
        删除 绑定组
        :return:
        """
        url = "/graphspaces/%s/auth/belongs/%s" % (graph_space, belong_id)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def get_belongs(self, graph_space=_cfg.graph_space, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphspaces/%s/auth/belongs" % graph_space
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_belong(self, belong_id, graph_space=_cfg.graph_space, auth=None):
        """
        用户绑定组
        :return:
        """
        url = "/graphspaces/%s/auth/belongs/%s" % (graph_space, belong_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def update_belongs(self, body, belong_id, graph_space=_cfg.graph_space, auth=None):
        """
        更新 belong
        :return:
        """
        url = "/graphspaces/%s/auth/belongs/%s" % (graph_space, belong_id)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def post_token(self, body, auth=None):
        """
        login token
        :return:
        """
        url = "/auth/login"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def get_verify(self, header, auth=None):
        """
        验证token
        :return:
        """
        url = "/auth/verify"
        print(header)
        code, res = Request(auth=auth).request(method='get', path=url, headers=header)
        return code, res


class Graph:
    """
    图的基本接口
    """

    def get_graphs(self, space=None, auth=None):
        """
        列出数据库中全部的图
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        url = "/graphspaces/%s/graphs" % space
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_one_graph(self, space=None, graph=None, auth=None):
        """
        查看某个图的信息
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_clear_graphs(self, params, auth=None):
        """
        清空图的数据(旧版本的api已经废弃)
        :return:
        """
        url = "/graphs/%s/clear" % _cfg.graph_name + params
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res

    def put_clear_graphs(self, space=None, graph=None, json=None, auth=None):
        """
        清空图的数据
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s" % (space, graph)
        print(url)
        code, res = Request(auth=auth).request(method='put', path=url, json=json)
        return code, res

    def get_graphs_conf(self, space=None, graph=None, auth=None):
        """
        查看某个图的配置
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/conf" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def put_graphs_mode(self, space=None, graph=None, body=None, auth=None):
        """
        设置某个图的模式
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/mode" % (space, graph)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def get_graphs_mode(self, space=None, graph=None, auth=None):
        """
        查看某个图的模式
        :param graph:
        :param space:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/mode" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_other_version(self, auth=None):
        """
        查看图的版本信息
        :param auth:
        :return:
        """
        url = "/versions"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def post_create_graph(self, space=None, graph=None, body=None, auth=None):
        """
        创建图
        :param space:
        :param graph:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_graphs(self, space=None, graph=None, auth=None):
        """
        删除图
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s" % (space, graph)
        code, res = Request(auth=auth).request(method='delete', path=url, headers={})
        return code, res

    def get_graph_read_mode(self, space=None, graph=None, auth=None):
        """
        查看某个图的读模式
        :param graph:
        :param space:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph_read_mode" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def put_graph_read_mode(self, space=None, graph=None, body=None, auth=None):
        """
        设置某个图的读模式
        :param graph:
        :param space:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph_read_mode" % (space, graph)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res


class GraphConfig:
    """
    图配置
    """
    def get_reset_config(self, space=None, auth=None):
        """

        :param space:
        :param auth:
        :return:
        """
        pass


class Variable:
    """
    Variables可以用来存储有关整个图的数据，数据按照键值对的方式存取
    """

    def list_var(self, space=None, graph=None, auth=None):
        """
        验证:var读
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/variables" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_var(self, space=None, graph=None, key=None, auth=None):
        """
        验证:var读
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/variables/%s" % (space, graph, key)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def put_var(self, space=None, graph=None, body=None, name=None, auth=None):
        """
        验证:var写
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/variables/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def delete_var(self, space=None, graph=None, name=None, auth=None):
        """
        验证:var 删除
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/variables/%s" % (space, graph, name)
        code, res = Request(auth=auth).request(method='delete', path=url)
        return code, res


class Vertex:
    """
    vertex opertaion
    """

    def create_single_vertex(self, space=None, graph=None, body=None, auth=None):
        """
        创建单个顶点
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/vertices" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def create_batch_vertex(self, space=None, graph=None, body=None, auth=None):
        """
        创建批量顶点
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/vertices/batch" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_vertex_batch_property(self, space=None, graph=None, body=None, auth=None):
        """
        批量更新顶点属性
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/vertices/batch" % (space, graph)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def update_vertex_property(self, space=None, graph=None, v_id=None, action=None, body=None, auth=None):
        """
        删除||增加||更新 顶点属性
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/vertices/%s" % (space, graph, v_id)
        code, res = Request(auth=auth).request(method='put', path=url, params=action, json=body)
        return code, res

    def get_filter_vertex(self, space=None, graph=None, condition=None, auth=None):
        """
        获取符合条件的顶点
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/vertices" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=condition)
        return code, res

    def get_vertex_by_id(self, space=None, graph=None, v_id=None, auth=None):
        """
        通过ID获取顶点
        :param graph:
        :param space:
        :param v_id:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/vertices/%s" % (space, graph, v_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_vertex(self, space=None, graph=None, v_id=None, label=None, auth=None):
        """
        通过顶点、顶点类型删除顶点
        :param graph:
        :param space:
        :param v_id:
        :param label:
        :param auth:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/vertices/%s" % (space, graph, v_id)
        print(url)
        code, res = Request(auth=auth).request(method='delete', path=url, params=label)
        return code, res


class Edge:
    """
    edge operation
    """

    def create_single_edge(self, space=None, graph=None, body=None, auth=None):
        """
        创建单条边
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/edges" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def create_batch_edge(self, space=None, graph=None, body=None, auth=None):
        """
        批量创建边
        :param graph:
        :param space:
        :param body: 请求body
        :param auth: 权限
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/edges/batch" % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def update_edge_batch_property(self, space=None, graph=None, body=None, auth=None):
        """
        批量更新属性
        :param graph:
        :param space:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/edges/batch" % (space, graph)
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def change_edge_property(self, space=None, graph=None, e_id=None, action=None, body=None, auth=None):
        """
        删除||更新||新增 边属性
        :param graph:
        :param space:
        :param e_id: 边ID
        :param action:
        :param body:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/edges/%s" % (space, graph, e_id)
        code, res = Request(auth=auth).request(method='put', path=url, params=action, json=body)
        return code, res

    def get_filter_edge(self, space=None, graph=None, condition=None, auth=None):
        """
        根据条件查询边
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/edges" % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=url, params=condition)
        return code, res

    def get_edge_by_id(self, space=None, graph=None, e_id=None, auth=None):
        """
        通过ID获取边
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/edges/%s" % (space, graph, e_id)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def delete_edge(self, space=None, graph=None, e_id=None, label=None, auth=None):
        """
        验证:edge 删除权限
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        url = "/graphspaces/%s/graphs/%s/graph/edges/%s" % (space, graph, e_id)
        code, res = Request(auth=auth).request(method='delete', path=url, params=label)
        return code, res


class Computer:
    """
    图计算 api
    """

    def create_computer_job(self, space=None, graph=None, body=None, auth=None):
        """
        创建图计算任务
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        part_url = '/graphspaces/%s/graphs/%s/jobs/computerdis' % (space, graph)
        code, res = Request(auth=auth).request(method='post', path=part_url, json=body)
        return code, res

    def get_computer_job_list(self, space=None, graph=None, param=None, auth=None):
        """
        查询图计算任务列表
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        part_url = '/graphspaces/%s/graphs/%s/jobs/computerdis' % (space, graph)
        code, res = Request(auth=auth).request(method='get', path=part_url, params=param)
        return code, res

    def get_computer_job(self, space=None, graph=None, job_id=None, auth=None):
        """
        查询图计算任务列表
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        part_url = '/graphspaces/%s/graphs/%s/jobs/computerdis/%d' % (space, graph, job_id)
        code, res = Request(auth=auth).request(method='get', path=part_url)
        return code, res

    def delete_computer_job(self, space=None, graph=None, job_id=None, auth=None):
        """
        删除图计算任务（停止正在执行的后台任务、并删除任务列表的数据）
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        part_url = '/graphspaces/%s/graphs/%s/jobs/computerdis/%d' % (space, graph, job_id)
        code, res = Request(auth=auth).request(method='delete', path=part_url)
        return code, res

    def cancle_computer_job(self, space=None, graph=None, job_id=None, auth=None):
        """
        取消图计算任务（停止正在执行的后台任务）
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        if graph is None:
            graph = _cfg.graph_name
        part_url = '/graphspaces/%s/graphs/%s/jobs/computerdis/%d' % (space, graph, job_id)
        code, res = Request(auth=auth).request(method='put', path=part_url)
        return code, res


class GraphSpace:
    """
    图空间的基本接口
    """
    def update_graph_space(self, space=None, body=None, auth=None):
        """
        设置某个图的模式
        :return:
        """
        url = "/graphspaces/%s" % space
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def get_graph_spaces(self, auth=None):
        """
        查看某个图的模式
        :param graph:
        :param space:
        :param auth:
        :return:
        """
        url = "/graphspaces"
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_one_graph_space(self, space=None, auth=None):
        """
        查看某个图的模式
        :param graph:
        :param space:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        url = "/graphspaces/%s" % space
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def create_graph_space(self, body=None, auth=None):
        """
        创建图
        :param space:
        :param graph:
        :param body:
        :param auth:
        :return:
        """
        url = "/graphspaces"
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_graph_space(self, space=None, auth=None):
        """
        删除图空间
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        url = "/graphspaces/%s" % space
        code, res = Request(auth=auth).request(method='delete', path=url, headers={})
        return code, res


class Service:
    """
    图服务的基本接口
    """
    def update_service(self, space=None, body=None, auth=None):
        """
        设置某个图的模式
        :return:
        """
        url = "/graphspaces/%s" % space
        code, res = Request(auth=auth).request(method='put', path=url, json=body)
        return code, res

    def get_service(self, space=None, auth=None):
        """
        查看某个图的模式
        :param graph:
        :param space:
        :param auth:
        :return:
        """
        url = "/graphspaces/%s/services" % space
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def get_one_service(self, space=None, service=None, auth=None):
        """
        查看某个图的模式
        :param service:
        :param space:
        :param auth:
        :return:
        """
        if space is None:
            space = _cfg.graph_space
        url = "/graphspaces/%s/services/%s" % (space, service)
        code, res = Request(auth=auth).request(method='get', path=url)
        return code, res

    def create_service(self, space=None, body=None, auth=None):
        """
        创建图
        :param space:
        :param graph:
        :param body:
        :param auth:
        :return:
        """
        url = "/graphspaces/%s/services" % space
        code, res = Request(auth=auth).request(method='post', path=url, json=body)
        return code, res

    def delete_service(self, space=None, service=None, param=None, auth=None):
        """
        删除图空间
        :return:
        """
        url = "/graphspaces/%s/services/%s" % (space, service)
        code, res = Request(auth=auth).request(method='delete', path=url, headers={}, params=param)
        return code, res


if __name__ == "__main__":
    pass

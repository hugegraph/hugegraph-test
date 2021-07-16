# -*- coding:utf-8 -*-
"""
author     : lxb
note       :
create_time:
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../..')

from src.common.request_cls import Request


class GraphConnection:
    """
    图链接接口
    """

    @staticmethod
    def add_graph_connect(body, auth=None):
        """
        添加图链接
        :param auth:
        :param body
        :return:
        """
        url = "/api/v1.2/graph-connections"
        code, res = Request().request(method="post", path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def get_graph_connect(param=None, auth=None):
        """
        查看图链接
        :param param:
        :param auth:
        :return:
        """
        url = '/api/v1.2/graph-connections'
        code, res = Request().request(method="get", path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def update_graph_connect(graph_id, body, auth=None):
        """
        修改图链接
        :param auth:
        :param graph_id:
        :param body:
        :return:
        """
        url = '/api/v1.2/graph-connections/%d' % graph_id
        code, res = Request().request(method="put", path=url, types="hubble", json=body)
        return code, res

    @staticmethod
    def delete_graph_connect(graph_id, auth=None):
        """
        删除全部图链接
        :param auth:
        :param graph_id:
        :return:
        """
        url = '/api/v1.2/graph-connections/%d' % graph_id
        code, res = Request().request(method="delete", path=url, types="hubble")
        return code, res


class Schema:
    """
    schema 接口,schema 样式接口
    """

    @staticmethod
    def create_property(body, graph_id, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/propertykeys" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def get_property(graph_id, auth=None):
        """
        :param graph_id:
        :param auth:
        """
        url = "/api/v1.2/graph-connections/%d/schema/propertykeys" % graph_id
        code, res = Request().request(method="get", path=url, types="hubble")
        return code, res

    @staticmethod
    def delete_property(graph_id, param=None, auth=None):
        """
        :param param:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/propertykeys" % graph_id
        code, res = Request().request(method='delete', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def create_vertexLabel(body, graph_id, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/vertexlabels" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def get_vertexLabel(graph_id, auth=None):
        """
        查看VertexLabel
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/vertexlabels" % graph_id
        code, res = Request().request(method='get', path=url, types="hubble")
        return code, res

    @staticmethod
    def delete_vertexLabel(graph_id, param=None, auth=None):
        """
        删除VertexLabel
        :param param: {}
        :param graph_id:
        :param auth:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/vertexlabels" % graph_id
        code, res = Request().request(method='delete', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def create_edgeLabel(body, graph_id, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/edgelabels" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def get_edgeLabel(graph_id, auth=None):
        """
        验证:EdgeLabel读权限
        :param graph_id:
        :param auth:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/edgelabels" % graph_id
        code, res = Request().request(method='get', path=url, types="hubble")
        return code, res

    @staticmethod
    def delete_edgeLabel(graph_id, param=None, auth=None):
        """
        删除edgeLabel
        :param param: {}
        :param graph_id:
        :param auth:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/edgelabels" % graph_id
        code, res = Request().request(method='delete', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def create_vertexLabelIndexLabel(body, graph_id, name, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :param name:顶点类型名称
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/vertexlabels/%s" % (graph_id, name)
        code, res = Request().request(method='put', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def create_edgeLabelIndexLabel(body, graph_id, name, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :param name:边类型名称
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/edgelabels/%s" % (graph_id, name)
        code, res = Request().request(method='put', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def get_PropertyIndex(graph_id, param, auth=None):
        """
        查看属性索引
        :param auth:
        :param graph_id:
        :param param:
        vertexLabelIndex:?page_no=1&page_size=10&is_vertex_label=true
        edgeLabelIndex:?page_no=1&page_size=10&is_vertex_label=false
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/propertyindexes" % graph_id
        code, res = Request().request(method='get', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def delete_vertexLabelIndexLabel(name, graph_id, body, auth=None):
        """
        删除顶点类型索引
        :param name:
        :param auth:
        :param graph_id:
        :param body:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/vertexlabels/%s" % (graph_id, name)
        code, res = Request().request(method='put', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def delete_edgeLabelIndexLabel(name, graph_id, body, auth=None):
        """
        删除边类型索引
        :param name:
        :param auth:
        :param graph_id:
        :param body:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/edgelabels/%s" % (graph_id, name)
        code, res = Request().request(method='put', path=url, json=body, types="hubble")
        return code, res


class ReuseSchema:
    """
    schema 复用接口
    """

    @staticmethod
    def reuse_property(body, graph_id, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/propertykeys/reuse" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def reuse_vertexLabel(body, graph_id, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/vertexlabels/reuse" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def reuse_edgeLabel(body, graph_id, auth=None):
        """
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/schema/edgelabels/reuse" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res


class Gremlin:
    """
    执行gremlin语句或任务
    """

    @staticmethod
    def gremlin_query(body, graph_id, auth=None):
        """
        执行GREMLIN查询
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/gremlin-query" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def gremlin_task(body, graph_id, auth=None):
        """
        执行GREMLIN任务
        :param body:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/gremlin-query/async-task" % graph_id
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res


class Task:
    """
    查看任务结果
    """

    @staticmethod
    def view_async_tasks_all(graph_id, param=None, auth=None):
        """
        查看所有异步任务
        :param param:
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/async-tasks" % graph_id
        code, res = Request().request(method='get', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def view_async_task_result(graph_id, async_task_id, auth=None):
        """
        查看异步任务结果
        :param auth:
        :param async_task_id:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/async-tasks/%d/result" % (graph_id, async_task_id)
        code, res = Request().request(method='get', path=url, types="hubble")
        return code, res

    @staticmethod
    def delete_async_task(graph_id, param, auth=None):
        """
        删除异步任务
        :param auth:
        :param param: 异步任务ID   单个:?ids=1    批量:?ids=1&ids=2
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/async-tasks" % graph_id
        code, res = Request().request(method='delete', path=url, params=param, types="hubble")
        return code, res


class Collection:
    """
    收藏功能
    """

    @staticmethod
    def collect_query_statement(body, graph_id, auth=None):
        """
        收藏语句
        :param auth:
        :param body:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/gremlin-collections" % graph_id
        code, res = Request().request(method='post', json=body, path=url, types="hubble")
        return code, res


class Load:
    """
    导入功能
    """

    @staticmethod
    def create_load_job(body, graph_id, auth=None):
        """
        创建导入任务
        :param auth:
        :param body:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager" % graph_id
        code, res = Request().request(method='post', json=body, path=url, types="hubble")
        return code, res

    @staticmethod
    def query_load_job(graph_id, auth=None):
        """
        查询导入任务，可返回ID
        :param auth:
        :param graph_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/" % graph_id
        code, res = Request().request(method='get', path=url, types="hubble")
        return code, res

    @staticmethod
    def update_load_job(body, graph_id, job_id, auth=None):
        """
        修改导入任务名称
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param body:需要修改的名称
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d" % (graph_id, job_id)
        code, res = Request().request(method='put', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def delete_load_job(graph_id, job_id, auth=None):
        """
        删除导入任务
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d" % (graph_id, job_id)
        code, res = Request().request(method='delete', path=url, types="hubble")
        return code, res

    @staticmethod
    def add_load_setting(body, graph_id, job_id, auth=None):
        """
        添加导入设置
        :param body:
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/load-parameter" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def start_load(graph_id, job_id, param, auth=None):
        """
        开始导入
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param param:url参数
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks/start" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def pause_load(graph_id, job_id, param, auth=None):
        """
        暂停导入
        :param auth:
        :param graph_id:
        :param param:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks/pause" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def stop_load(graph_id, job_id, param, auth=None):
        """
        停止导入
        :param auth:
        :param graph_id:
        :param param:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks/stop" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def resume_load(graph_id, job_id, param, auth=None):
        """
        继续导入
        :param auth:
        :param graph_id:
        :param param:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks/resume" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def retry_load(graph_id, job_id, param, auth=None):
        """
        重试导入
        :param auth:
        :param graph_id:
        :param param:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks/retry" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def query_all_load_tasks(graph_id, job_id, auth=None):
        """
        查询全部导入任务
        :param auth:
        :param graph_id:
        :param job_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks" % (graph_id, job_id)
        code, res = Request().request(method='get', path=url, types="hubble")
        return code, res

    @staticmethod
    def query_load_task(graph_id, job_id, param, auth=None):
        """
        根据任务ID查询导入任务
        :param auth:
        :param graph_id:
        :param job_id:
        :param param:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks" % (graph_id, job_id)
        code, res = Request().request(method='get', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def delete_load_task(graph_id, job_id, task_id, auth=None):
        """
        根据任务ID删除导入任务
        :param auth:
        :param graph_id:
        :param job_id:
        :param task_id:
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/load-tasks/%d" % (graph_id, job_id, task_id)
        code, res = Request().request(method='delete', path=url, types="hubble")
        return code, res


class File:
    """
    导入功能
    """

    @staticmethod
    def get_loadfile_token(graph_id, job_id, param=None, auth=None):
        """
        获取文件token
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param param:
        :return: ?names=movie.csv
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/upload-file/token" % (graph_id, job_id)
        code, res = Request().request(method='get', path=url, params=param, types="hubble")
        return code, res

    @staticmethod
    def upload_file(graph_id, job_id, files, param, auth=None):
        """
        上传文件
        :param auth:
        :param graph_id:
        :param files:需要上传一个字典   {"file": open("./add_data/finally.csv", 'rb')}
        :param job_id:导入任务ID
        :param param: total=1&index=1&name=finally.csv&token=
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/upload-file" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, params=param, files=files, types="hubble")
        return code, res

    @staticmethod
    def delete_file(graph_id, job_id, file_name, param, auth=None):
        """
        删除文件
        :param auth:
        :param graph_id:
        :param file_name:需要上传一个字典   {"file": open("./add_data/finally.csv", 'rb')}
        :param job_id:导入任务ID
        :param param: total=1&index=1&name=finally.csv&token=
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/upload-file" % (graph_id, job_id)
        code, res = Request().request(method='post', path=url, params=param, files=file_name, types="hubble")
        return code, res


class Mapping:
    """
    添加映射
    """

    @staticmethod
    def add_file_setting(body, graph_id, job_id, file_id, auth=None):
        """
        添加文件设置
        :param body:
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param file_id:文件ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/%d/file-setting" % \
              (graph_id, job_id, file_id)
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def add_vertex_mapping(body, graph_id, job_id, file_id, auth=None):
        """
        添加顶点映射
        :param body:
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param file_id:文件ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/%d/vertex-mappings" % (
            graph_id, job_id, file_id)
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def update_vertex_mapping(body, graph_id, job_id, file_id, vertex_id, auth=None):
        """
        修改顶点映射
        :param body:
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param file_id:文件ID
        :param vertex_id:顶点映射ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/%d/vertex-mappings/%s" % (
            graph_id, job_id, file_id, vertex_id)
        code, res = Request().request(method='put', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def delete_vertex_mapping(graph_id, job_id, file_id, vertex_id, auth=None):
        """
        删除顶点映射
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param file_id:文件ID
        :param vertex_id:顶点映射ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/%d/vertex-mappings/%s" % (
            graph_id, job_id, file_id, vertex_id)
        code, res = Request().request(method='delete', path=url, types="hubble")
        return code, res

    @staticmethod
    def add_edge_mapping(body, graph_id, job_id, file_id, auth=None):
        """
        添加边映射
        :param body:
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param file_id:文件ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/%d/edge-mappings" % (
            graph_id, job_id, file_id)
        code, res = Request().request(method='post', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def update_edge_mapping(body, graph_id, job_id, file_id, edge_id, auth=None):
        """
        修改边映射
        :param body:
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param file_id:文件ID
        :param edge_id:边映射ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/%d/edge-mappings/%s" % (
            graph_id, job_id, file_id, edge_id)
        code, res = Request().request(method='put', path=url, json=body, types="hubble")
        return code, res

    @staticmethod
    def delete_edge_mapping(graph_id, job_id, file_id, edge_id, auth=None):
        """
        删除边映射
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :param file_id:文件ID
        :param edge_id:边映射ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/%d/edge-mappings/%s" % (
            graph_id, job_id, file_id, edge_id)
        code, res = Request().request(method='delete', path=url, types="hubble")
        return code, res

    @staticmethod
    def query_all_file_mapping(graph_id, job_id, auth=None):
        """
        查看所有文件映射
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings" % (graph_id, job_id)
        code, res = Request().request(method='get', path=url, types="hubble")
        return code, res


class Step:
    """
    导入过程中会有下一步的操作
    """

    @staticmethod
    def upload_file_next_step(graph_id, job_id, auth=None):
        """
        上传文件完成，点击下一步
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/upload-file/next-step" % (graph_id, job_id)
        code, res = Request().request(method='put', path=url, types="hubble")
        return code, res

    @staticmethod
    def mapping_complete_next_step(graph_id, job_id, auth=None):
        """
        设置映射完成，点击下一步
        :param auth:
        :param graph_id:
        :param job_id:导入任务ID
        :return:
        """
        url = "/api/v1.2/graph-connections/%d/job-manager/%d/file-mappings/next-step" % (graph_id, job_id)
        code, res = Request().request(method='put', path=url, types="hubble")
        return code, res


class ID:
    """
    提供case需要的ID
    """

    @staticmethod
    def get_graph_id():
        """
        获取图ID
        """
        res = GraphConnection().get_graph_connect()
        graph_id = res[1]["data"]["records"][0]["id"]
        return graph_id

    @staticmethod
    def get_job_id():
        """
        获取图ID,和任务ID
        """
        res = GraphConnection().get_graph_connect()
        graph_id = res[1]["data"]["records"][0]["id"]
        res = Load.query_load_job(graph_id)
        job_id = res[1]['data']['records'][0]['id']
        return graph_id, job_id

    @staticmethod
    def get_file_id():
        """
        获取ID,任务ID和文件ID
        """
        res = GraphConnection().get_graph_connect()
        graph_id = res[1]["data"]["records"][0]["id"]
        res = Load.query_load_job(graph_id)
        job_id = res[1]['data']['records'][0]['id']
        res = Mapping.query_all_file_mapping(graph_id, job_id)
        file_id = res[1]['data']['records'][0]['id']
        return graph_id, job_id, file_id

    @staticmethod
    def get_task_id():
        """
        获取图ID,任务ID,文件ID和任务ID
        """
        id_list = []
        res = GraphConnection().get_graph_connect()
        graph_id = res[1]["data"]["records"][0]["id"]
        res = Load.query_load_job(graph_id)
        job_id = res[1]['data']['records'][0]['id']
        res = Mapping.query_all_file_mapping(graph_id, job_id)
        file_id = res[1]['data']['records'][0]['id']
        res = Load.query_all_load_tasks(graph_id, job_id)
        task_id = res[1]['data']['records'][0]['id']
        id_list.append(graph_id)
        id_list.append(job_id)
        id_list.append(file_id)
        id_list.append(task_id)
        return id_list

    @staticmethod
    def get_vertexMapping_id():
        """
        获取图ID,任务ID,文件ID和顶点映射ID
        """
        id_list = []
        res = GraphConnection().get_graph_connect()
        graph_id = res[1]["data"]["records"][0]["id"]
        res = Load.query_load_job(graph_id)
        job_id = res[1]['data']['records'][0]['id']
        res = Mapping.query_all_file_mapping(graph_id, job_id)
        file_id = res[1]['data']['records'][0]['id']
        res = Mapping.query_all_file_mapping(graph_id, job_id)
        vertex_mapping_id = res[1]['data']['records'][0]['vertex_mappings'][0]['id']
        id_list.append(graph_id)
        id_list.append(job_id)
        id_list.append(file_id)
        id_list.append(vertex_mapping_id)
        return id_list

    @staticmethod
    def get_edgeMapping_id():
        """
        获取图ID,任务ID,文件ID和边映射ID
        """
        id_list = []
        res = GraphConnection().get_graph_connect()
        graph_id = res[1]["data"]["records"][0]["id"]
        res = Load.query_load_job(graph_id)
        job_id = res[1]['data']['records'][0]['id']
        res = Mapping.query_all_file_mapping(graph_id, job_id)
        file_id = res[1]['data']['records'][0]['id']
        res = Mapping.query_all_file_mapping(graph_id, job_id)
        edge_mapping_id = res[1]['data']['records'][0]['edge_mappings'][0]['id']
        id_list.append(graph_id)
        id_list.append(job_id)
        id_list.append(file_id)
        id_list.append(edge_mapping_id)
        return id_list

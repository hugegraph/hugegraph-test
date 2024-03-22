# -*- coding: UTF-8 -*-
"""
Created by v_changshuai01 at 2021/5/18
"""
import os
import sys
import unittest
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg
from src.common.hubble_api import GraphConnection
from src.common.hubble_api import Mapping
from src.common.hubble_api import Load
from src.common.server_api import Gremlin
from src.common.hubble_api import File
from src.common.hubble_api import ID
from src.common.hubble_api import Step
from src.common.tools import clear_graph

auth = None
user = None
if _cfg.is_auth:
    auth = _cfg.admin_password
    user = _cfg.test_password


def init_graph():
    """
    对测试环境进行初始化操作
    """

    code, res = GraphConnection().get_graph_connect()
    assert code == 200
    connection_list = res['data']['records']
    for each in connection_list:
        each_id = each['id']
        each_graph = each['graph']
        each_host = each['host']
        each_port = each['port']
        # clear graph
        if _cfg.server_backend == 'cassandra':
            clear_graph(graph_name=each_graph, graph_host=each_host, graph_port=each_port)
        else:
            Gremlin().gremlin_post('graph.truncateBackend();')  # 使用 gremlin 语句进行 truncate 操作
        # delete graph_connection
        code, res = GraphConnection().delete_graph_connect(each_id)
        assert code == 200


class LoadTest(unittest.TestCase):
    """
    hubble 的导入模块 API
    """

    def setUp(self):
        """
        每条 case 的前提条件
        :return:
        """
        body = {
            "name": _cfg.graph_name + "_test1",
            "graph": _cfg.graph_name,
            "host": _cfg.graph_host,
            "port": _cfg.server_port
        }
        if _cfg.is_auth:
            body['username'] = 'admin'
            body['password'] = _cfg.admin_password.get('admin')
        init_graph()
        code, res = GraphConnection().add_graph_connect(body)
        print(code, res)
        assert code == 200
        query = {
            "content": "graph.schema().propertyKey('名称').asText().ifNotExist().create();"
                       "graph.schema().propertyKey('类型').asText().valueSet().ifNotExist().create();"
                       "graph.schema().propertyKey('发行时间').asDate().ifNotExist().create();"
                       "graph.schema().vertexLabel('电影').useCustomizeStringId().properties('名称', '类型', '发行时间')"
                       ".nullableKeys('类型','发行时间').ifNotExist().create();"
                       "graph.schema().vertexLabel('艺人').useCustomizeStringId().ifNotExist().create();"
                       "graph.schema().vertexLabel('类型').useCustomizeStringId().ifNotExist().create();"
                       "graph.schema().vertexLabel('年份').useCustomizeStringId().ifNotExist().create();"
                       "graph.schema().edgeLabel('导演').link('艺人', '电影').ifNotExist().create();"
                       "graph.schema().edgeLabel('演出').link('艺人', '电影').ifNotExist().create();"
                       "graph.schema().edgeLabel('属于').link('电影', '类型').properties('发行时间').ifNotExist().create();"
                       "graph.schema().edgeLabel('发行于').link('电影', '年份').ifNotExist().create();"
        }
        code, res = Gremlin().gremlin_post(query=query["content"], host=_cfg.graph_host, port=_cfg.server_port, auth=auth)
        print(code, res)
        assert code == 200

    def tearDown(self):
        """
        测试 case 结束
        :param self:
        :return:
        """
        pass

    def test_create_load_job(self):
        """
        创建导入任务
        """
        graph_id = ID.get_graph_id()
        body = {"job_name": "load_01", "job_remarks": "第一次导入"}
        code, res = Load.create_load_job(body=body, graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "创建导入任务状态码不正确")
        self.assertEqual(res['data']['job_name'], body['job_name'], "导入任务名称有误")
        self.assertEqual(res['data']['job_remarks'], body['job_remarks'], "任务备注有误")

    def test_upload_file(self):
        """
        上传文件
        """
        self.test_create_load_job()
        graph_id, job_id = ID.get_job_id()
        res = File.get_loadfile_token(graph_id=graph_id, job_id=job_id, param="names=movie.csv")
        token = res[1]["data"]["movie.csv"]
        param = "total=1&index=1&name=movie.csv&token=%s" % token
        files = {"file": open(current_path + "/../../../config/dataset/movie/movie.csv", 'rb')}
        code, res = File.upload_file(graph_id=graph_id, job_id=job_id, files=files, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "上传文件状态码不正确")
        self.assertEqual(res['data']['name'], "movie.csv", "上传文件有误")
        self.assertEqual(res['data']['status'], "SUCCESS", "上传文件失败")

    def test_add_file_setting(self):
        """
        添加文件设置
        """
        self.test_upload_file()
        graph_id, job_id, file_id = ID.get_file_id()
        # 点击下一步
        Step.upload_file_next_step(graph_id=graph_id, job_id=job_id)
        body = {
            "has_header": True,
            "delimiter": ",",
            "format": "CSV",
            "charset": "UTF-8",
            "date_format": "yyyy",
            "time_zone": "GMT+8",
            "skipped_line": "(^#^//).*"
        }
        code, res = Mapping.add_file_setting(body=body, graph_id=graph_id, job_id=job_id, file_id=file_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "文件设置状态码不正确")
        self.assertEqual(res['data']['file_setting']['has_header'], body['has_header'], "文件头设置有误")
        self.assertEqual(res['data']['file_setting']['delimiter'], body['delimiter'], "文件分隔符设置有误")
        self.assertEqual(res['data']['file_setting']['date_format'], body['date_format'], "文件时间格式设置有误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_add_vertex_mapping(self):
        """
        设置顶点映射
        """
        self.test_add_file_setting()
        graph_id, job_id, file_id = ID.get_file_id()
        vertex_movie = {
            "label": "电影",
            "id_fields": ["名称"],
            "field_mapping": [{
                "column_name": "发行时间",
                "mapped_name": "发行时间"
            }, {
                "column_name": "类型",
                "mapped_name": "类型"
            }],
            "value_mapping": [],
            "null_values": {
                "checked": ["NULL", "null"],
                "customized": []
            }
        }
        # 年份
        vertex_time = {
            "label": "年份",
            "id_fields": ["发行时间"],
            "field_mapping": [],
            "value_mapping": [],
            "null_values": {
                "checked": ["NULL", "null"],
                "customized": []
            },
        }
        code, res = Mapping.add_vertex_mapping(body=vertex_movie, graph_id=graph_id, job_id=job_id, file_id=file_id)
        Mapping.add_vertex_mapping(body=vertex_time, graph_id=graph_id, job_id=job_id, file_id=file_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "文件添加顶点映射状态码不正确")
        self.assertEqual(res['data']['vertex_mappings'][0]['label'], vertex_movie['label'], "映射的顶点类型有误")
        self.assertEqual(res['data']['vertex_mappings'][0]['id_fields'], vertex_movie['id_fields'], "ID 列有误")
        self.assertEqual(res['data']['vertex_mappings'][0]['field_mapping'], vertex_movie['field_mapping'],
                         "列映射错误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_add_edge_mapping(self):
        """
        设置边映射
        """
        self.test_add_vertex_mapping()
        graph_id, job_id, file_id = ID.get_file_id()
        # 发行于
        edge_issue = {
            "label": "发行于",
            "source_fields": ["名称"],
            "target_fields": ["发行时间"],
            "field_mapping": [],
            "value_mapping": [],
            "null_values": {
                "checked": ["NULL", "null"],
                "customized": []
            }
        }
        code, res = Mapping.add_edge_mapping(body=edge_issue, graph_id=graph_id, job_id=job_id, file_id=file_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "文件添加边映射状态码不正确")
        self.assertEqual(res['data']['edge_mappings'][0]['label'], edge_issue['label'], "映射的边类型有误")
        self.assertEqual(res['data']['edge_mappings'][0]['source_fields'], edge_issue['source_fields'], "起点映射有误")
        self.assertEqual(res['data']['edge_mappings'][0]['target_fields'], edge_issue['target_fields'], "终点映射有误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_add_load_setting(self):
        """
        设置导入参数
        """
        self.test_add_edge_mapping()
        graph_id, job_id = ID.get_job_id()
        body = {
            "check_vertex": False,
            "insert_timeout": 60,
            "max_parse_errors": 500,
            "max_insert_errors": 500,
            "retry_times": 3,
            "retry_interval": 10
        }
        # 点击下一步
        Step.mapping_complete_next_step(graph_id=graph_id, job_id=job_id)
        code, res = Load.add_load_setting(body=body, graph_id=graph_id, job_id=job_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "设置导入参数状态码不正确")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_start_load(self):
        """
        点击开始导入
        """
        self.test_add_load_setting()
        graph_id, job_id, file_id = ID.get_file_id()
        param = "file_mapping_ids=%d" % file_id
        code, res = Load.start_load(graph_id=graph_id, job_id=job_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "开始导入状态码不正确，开始导入失败")
        self.assertEqual(res['data'][0]['status'], 'RUNNING', "开始导入错误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_pause_load(self):
        """
        点击暂停导入
        """
        self.test_start_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        param = "task_id=%d" % task_id
        code, res = Load.pause_load(graph_id=graph_id, job_id=job_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "暂停导入状态码不正确，暂停导入失败")
        self.assertEqual(res['data']['status'], 'PAUSED', "暂停导入错误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_resume_load(self):
        """
        点击继续导入
        """
        self.test_pause_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        param = "task_id=%d" % task_id
        time.sleep(1)
        code, res = Load.resume_load(graph_id=graph_id, job_id=job_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "继续导入状态码不正确，继续导入失败")
        self.assertEqual(res['data']['status'], 'RUNNING', "继续导入错误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_stop_load(self):
        """
        点击停止导入
        """
        self.test_resume_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        param = "task_id=%d" % task_id
        code, res = Load.stop_load(graph_id=graph_id, job_id=job_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "停止导入状态码不正确，停止导入失败")
        self.assertEqual(res['data']['status'], 'STOPPED', "停止导入错误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_retry_load(self):
        """
        点击重试导入
        """
        self.test_stop_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        param = "task_id=%d" % task_id
        code, res = Load.retry_load(graph_id=graph_id, job_id=job_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "重试导入状态码不正确，重试导入失败")
        self.assertEqual(res['data']['status'], 'RUNNING', "重试导入错误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_get_load_task(self):
        """
        查询导入任务
        """
        self.test_stop_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        param = "task_id=%d" % task_id
        code, res = Load.query_load_task(graph_id=graph_id, job_id=job_id, param=param)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查询导入状态码不正确，查询导入任务失败")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_delete_load_task(self):
        """
        删除导入任务
        """
        self.test_stop_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        code, res = Load.delete_load_task(graph_id=graph_id, job_id=job_id, task_id=task_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除导入状态码不正确，删除导入任务失败")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_get_load_job(self):
        """
        查询任务
        """
        self.test_stop_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        code, res = Load.query_load_job(graph_id=graph_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "查询任务状态码不正确，查询任务失败")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_update_load_job(self):
        """
        修改导入任务名称和备注
        """
        self.test_get_load_job()
        graph_id, job_id = ID.get_job_id()
        body = {"job_name": "load_01_update", "job_remarks": "修改任务名称和备注"}
        code, res = Load.update_load_job(body=body, graph_id=graph_id, job_id=job_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "修改导入任务名称和备注状态码不正确，修改导入任务名称和备注失败")
        self.assertEqual(res['data']['job_name'], body['job_name'], "修改导入任务名称有误")
        self.assertEqual(res['data']['job_remarks'], body['job_remarks'], "修改导入任务备注有误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_delete_load_job(self):
        """
        删除任务
        """
        self.test_stop_load()
        graph_id, job_id, file_id, task_id = ID.get_task_id()
        code, res = Load.delete_load_job(graph_id=graph_id, job_id=job_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除任务状态码不正确，删除任务失败")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_update_vertex_mapping(self):
        """
        更新顶点映射
        """
        self.test_add_vertex_mapping()
        graph_id, job_id, file_id, vertex_id = ID.get_vertexMapping_id()
        vertex_movie = {
            "label": "电影",
            "id_fields": ["名称"],
            "field_mapping": [{
                "column_name": "发行时间",
                "mapped_name": "发行时间_更新"
            }, {
                "column_name": "类型",
                "mapped_name": "类型"
            }],
            "value_mapping": [],
            "null_values": {
                "checked": ["NULL", "null"],
                "customized": []
            }
        }
        code, res = Mapping.update_vertex_mapping(body=vertex_movie, graph_id=graph_id, job_id=job_id, file_id=file_id,
                                                  vertex_id=vertex_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "修改顶点映射状态码不正确")
        self.assertEqual(res['data']['vertex_mappings'][1]['field_mapping'][0]['mapped_name'],
                         vertex_movie['field_mapping'][0]['mapped_name'], "顶点映射修改有误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_update_edge_mapping(self):
        """
        更新边映射
        """
        self.test_add_edge_mapping()
        graph_id, job_id, file_id, edge_id = ID.get_edgeMapping_id()
        # 发行于
        edge_issue = {
            "label": "发行于",
            "source_fields": ["名称"],
            "target_fields": ["发行时间"],
            "field_mapping": [],
            "value_mapping": [],
            "null_values": {
                "checked": ["NULL", "null"],
                "customized": ["EMPTY"]
            }
        }
        code, res = Mapping.update_edge_mapping(body=edge_issue, graph_id=graph_id, job_id=job_id, file_id=file_id,
                                                edge_id=edge_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "修改边映射状态码不正确")
        self.assertEqual(res['data']['edge_mappings'][0]['label'], edge_issue['label'], "修改边映射有误")
        self.assertEqual(res['data']['edge_mappings'][0]['null_values']['customized'],
                         edge_issue['null_values']['customized'], "边映射空值列表修改有误")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_delete_vertex_mapping(self):
        """
        删除一个顶点映射
        """
        self.test_add_vertex_mapping()
        graph_id, job_id, file_id, vertex_id = ID.get_vertexMapping_id()

        code, res = Mapping.delete_vertex_mapping(graph_id=graph_id, job_id=job_id, file_id=file_id,
                                                  vertex_id=vertex_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除顶点映射状态码不正确")

    @unittest.skipIf(os.environ.get('CI') == 'github', "TODO: Skip it in GitHub CI now")
    def test_delete_edge_mapping(self):
        """
        删除单个边映射
        """
        self.test_add_edge_mapping()
        graph_id, job_id, file_id, edge_id = ID.get_edgeMapping_id()
        code, res = Mapping.delete_edge_mapping(graph_id=graph_id, job_id=job_id, file_id=file_id, edge_id=edge_id)
        self.assertEqual(code, 200, "响应状态码不正确")
        self.assertEqual(res['status'], 200, "删除边映射状态码不正确")


if __name__ == '__main__':
    unittest.main()

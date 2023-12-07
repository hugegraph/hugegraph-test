# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 给初始化的空图添加数据
create_time:  2020/10/27 20:20 下午
"""
import os
import sys
import subprocess

root_path = os.path.dirname(os.path.realpath(__file__)) + '/../../'
sys.path.append(root_path)

from src.common.server_api import Gremlin
from src.config import basic_config as _cfg

dataset_path = root_path + 'src/config/dataset/'


def gremlin_create_graph(file_name, auth=None):
    """
    读取文件 & 请求gremlin接口创建图
    """
    gremlin_str = ''
    n = 0
    with open(file_name, 'r') as f:
        for line in f:
            each_line = line.strip('\n')
            if line.startswith('graph'):
                Gremlin().gremlin_post(each_line, auth=auth)
            elif line.startswith('#') or line is None:
                pass
            else:
                if n == 200:
                    n = 0
                    gremlin_str += each_line
                    Gremlin().gremlin_post(gremlin_str, auth=auth)
                    gremlin_str = ''
                else:
                    n += 1
                    gremlin_str += each_line
            Gremlin().gremlin_post(gremlin_str, auth=auth)


class InsertData:
    """
    添加数据
    """
    def __init__(self, part_cmd=None, gremlin=None, schema=None, struct=None, dir=None):
        self.host = _cfg.graph_host
        self.port = _cfg.server_port
        self.graph = _cfg.graph_name
        self.is_https = _cfg.is_https
        self.is_auth = _cfg.is_auth
        self.auth = _cfg.admin_password

        if self.is_auth:
            self.auth_cmd = " --username admin  --token %s " % _cfg.admin_password['admin']
        else:
            self.auth_cmd = ""

        https = " --protocol https "
        if _cfg.loader_store_file != "":
            https += " --trust-store-file %s " % _cfg.loader_store_file
        else:
            pass
        if _cfg.loader_store_password != "":
            https += " --trust-store-password %s " % _cfg.loader_store_password
        else:
            pass

        self.https_cmd = https
        self.part_cmd = part_cmd
        self.gremlin = gremlin
        self.schema = schema
        self.struct = struct
        self.dir = dir

    def load_graph(self):
        """
        通过loader组件导入数据
        """
        struct_file = dataset_path + self.dir + '/' + self.struct
        if self.schema is None:
            loader_cmd = self.part_cmd % (_cfg.loader_path, self.host, self.port, self.graph, struct_file)
        else:
            schema_file = dataset_path + self.dir + '/' + self.schema
            loader_cmd = self.part_cmd % (_cfg.loader_path, self.host, self.port, self.graph, struct_file, schema_file)

        if self.is_https:
            loader_cmd += self.https_cmd

        if self.is_auth:
            loader_cmd += self.auth_cmd
        print('+++++++++++   cd %s && %s' % (dataset_path + self.dir, loader_cmd))

        res = subprocess.Popen('cd %s && %s' % (dataset_path + self.dir, loader_cmd),
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        return res

    def gremlin_graph(self):
        """
        gremlin接口批量执行file中的语句
        """
        if self.is_auth:
            gremlin_create_graph(dataset_path + self.gremlin, self.auth)
        else:
            gremlin_create_graph(dataset_path + self.gremlin)

    def loader_assert(self):
        """
        进行gremlin 查询
        :return:
        """
        if self.is_auth:
            code_v, res_v = Gremlin().gremlin_post("g.V().count()", auth=self.auth)
            code_e, res_e = Gremlin().gremlin_post("g.E().count()", auth=self.auth)
            return res_v['result']["data"][0], res_e['result']["data"][0]
        else:
            code_v, res_v = Gremlin().gremlin_post("g.V().count()")
            code_e, res_e = Gremlin().gremlin_post("g.E().count()")
            return res_v['result']["data"][0], res_e['result']["data"][0]


if __name__ == "__main__":
    pass

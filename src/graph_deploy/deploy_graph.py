# -*- coding:utf-8 -*-
"""
author     : lxb
note       : Component deployment begins
create_time: 2020/4/22 5:17 下午
"""
import os
import sys
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../')

from src.common.file_basic import is_match_re
from src.common.file_basic import is_exists_path
from src.common.file_basic import alter_properties


def get_code(pwd, git_obj, code_dir):
    """
    拉取graph组件的源码：如果本路径有代码库则更新即可；没有代码库则拉取最新代码
    :param pwd: 路径
    :param git_obj: git 配置
    :param code_dir:
    """
    if not is_match_re(pwd, code_dir):
        branch = git_obj['branch']
        url = git_obj['url']
        print('cd %s && git clone -b %s %s' % (pwd, branch, url))
        os.system('cd %s && git clone -b %s %s' % (pwd, branch, url))
    else:
        os.system('cd %s/%s && git pull' % (pwd, code_dir))


def compile_package(dir_code_path):
    """
    编译包
    :param dir_code_path: 本地代码库路径
    :return:
    """
    g_name = dir_code_path.split('/')[-1]
    if g_name == 'hugegraph-loader':
        os.system('cd %s && /usr/local/maven-3.6.3/bin/mvn install:install-file -Dfile=./assembly/static/lib/ojdbc8-12.2.0.1.jar -DgroupId=com.oracle -DartifactId=ojdbc8 -Dversion=12.2.0.1 -Dpackaging=jar && mvn clean package -Dmaven.test.skip=true | grep -v \"Downloading\|Downloaded\"' % dir_code_path)
    else:
        os.system('cd %s && /usr/local/maven-3.6.3/bin/mvn clean package -Dmaven.test.skip=true | grep -v \"Downloading\|Downloaded\"' % dir_code_path)

   
def copy_decompression(source_path, target_path, re_name):
    """
    复制包到目的路径并解压
    :param source_path: 源路径
    :param target_path: 目的路径
    :param re_name: 正则
    :return:
    """
    tar_name = is_match_re(source_path, re_name)
    if tar_name:
        os.system(
            'cp -rf %s %s && cd %s && tar xzvf %s' % (source_path, target_path, target_path, tar_name))
    else:
        print('compile_package is failed')


def set_server_properties(package_dir_path, host, server_port, gremlin_port):
    """
    修改server组件配置
    :return:
    """
    # 修改rest-server.properties文件
    rest_conf = package_dir_path + '/conf/rest-server.properties'
    alter_properties(rest_conf,
                     '127.0.0.1:8080',
                     '%s:%d' % (host, server_port))
    alter_properties(rest_conf,
                     '#gremlinserver.url=http://127.0.0.1:8182',
                     'gremlinserver.url=http://%s:%d' % (host, gremlin_port))
    # 修改gremlin-server.yaml文件
    gremlin_conf = package_dir_path + '/conf/gremlin-server.yaml'
    alter_properties(gremlin_conf,
                     '#host: 127.0.0.1',
                     'host: %s' % host)
    alter_properties(gremlin_conf,
                     '#port: 8182',
                     'port: %d' % gremlin_port)


def set_hubble_properties(package_dir_path, host, port):
    """
    修改hubble组件配置
    :return:
    """
    hubble_conf = package_dir_path + '/conf/hugegraph-hubble.properties'
    alter_properties(hubble_conf, 'server.host=localhost', 'server.host=%s' % host)
    alter_properties(hubble_conf, 'server.port=8088', 'server.port=%d' % port)


def start_graph(package_dir_path, graph_type):
    """
    启动graph包
    """
    if graph_type == 'server':
        os.system(
            'cd %s '
            '&& ./bin/stop-hugegraph.sh '
            '&& ./bin/init-store.sh '
            '&& ./bin/start-hugegraph.sh' % package_dir_path)
    else:
        os.system(
            'cd %s '
            '&& ./bin/stop-hubble '
            '&& ./bin/start-hubble' % package_dir_path)


class Deploy:
    """
    图库组件部署
    """
    def __init__(self, obj):
        self.graph_host = obj.graph_host
        self.server_port = obj.server_port
        self.gremlin_port = obj.gremlin_port
        self.hubble_port = obj.hubble_port
        self.deploy_path = obj.deploy_path
        self.code_path = obj.code_path
        self.server_git = obj.server_git
        self.loader_git = obj.loader_git
        self.tools_git = obj.tools_git
        self.hubble_git = obj.hubble_git

    @staticmethod
    def server(self):
        """
        :return:
        """
        code_dir = 'hugegraph'
        code_dir_path = self.code_path + '/' + code_dir
        re_dir = '^%s-(\d).(\d{1,2}).(\d)$' % code_dir
        re_tar = '^%s-(\d).(\d{1,2}).(\d).tar.gz$' % code_dir

        flag_deploy_path = is_exists_path(self.deploy_path)
        match_re = is_match_re(self.deploy_path, re_dir)
        if flag_deploy_path and match_re:
            # server组件已经存在
            start_graph(self.deploy_path + '/' + match_re, 'server')
        else:
            get_code(self.code_path, self.server_git, code_dir)
            compile_package(code_dir_path)
            copy_decompression(code_dir_path, self.deploy_path, re_tar)
            #  start graph_server
            package_dir_name = is_match_re(self.deploy_path, re_dir)
            package_dir_path = self.deploy_path + '/' + package_dir_name
            set_server_properties(package_dir_path, self.graph_host, self.server_port, self.gremlin_port)
            start_graph(package_dir_path, 'server')

    @staticmethod
    def hubble(self):
        """
        :return:
        """
        code_dir = 'hugegraph-hubble'
        code_dir_path = self.code_path + '/' + code_dir
        re_dir = '^%s-(\d).(\d{1,2}).(\d)$' % code_dir
        re_tar = '^%s-(\d).(\d{1,2}).(\d).tar.gz$' % code_dir

        flag_deploy_path = is_exists_path(self.deploy_path)
        match_re = is_match_re(self.deploy_path, re_dir)
        if flag_deploy_path and match_re:
            start_graph(self.deploy_path + '/' + match_re, 'hubble')
        else:
            get_code(self.code_path, self.hubble_git, code_dir)
            compile_package(code_dir_path)
            copy_decompression(code_dir_path, self.deploy_path, re_tar)
            # 修改配置并启动
            package_dir_name = is_match_re(self.deploy_path, re_dir)
            package_dir_path = self.deploy_path + '/' + package_dir_name
            set_hubble_properties(package_dir_path, self.graph_host, self.hubble_port)
            start_graph(package_dir_path, 'hubble')

    @staticmethod
    def loader(self):
        """
        :return:
        """
        code_dir = 'hugegraph-loader'
        code_dir_path = self.code_path + '/' + code_dir
        re_dir = '^%s-(\d).(\d{1,2}).(\d)$' % code_dir
        re_tar = '^%s-(\d).(\d{1,2}).(\d).tar.gz$' % code_dir

        flag_deploy_path = is_exists_path(self.deploy_path)
        match_re = is_match_re(self.deploy_path, re_dir)
        if flag_deploy_path and match_re:
            pass  # loader 组件已经存在
        else:
            get_code(self.code_path, self.loader_git, code_dir)
            compile_package(code_dir_path)
            copy_decompression(code_dir_path, self.deploy_path, re_tar)

    @staticmethod
    def tools(self):
        """
        :return:
        """
        code_dir = 'hugegraph-tools'
        code_dir_path = self.code_path + '/' + code_dir
        re_dir = '^%s-(\d).(\d{1,2}).(\d)$' % code_dir
        re_tar = '^%s-(\d).(\d{1,2}).(\d).tar.gz$' % code_dir

        flag_deploy_path = is_exists_path(self.deploy_path)
        match_re = is_match_re(self.deploy_path, re_dir)
        if flag_deploy_path and match_re:
            pass  # tools 组件已经存在
        else:
            get_code(self.code_path, self.tools_git, code_dir)
            compile_package(code_dir_path)
            copy_decompression(code_dir_path, self.deploy_path, re_tar)


if __name__ == "__main__":
    pass

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
from src.config import basic_config as _cfg


def get_code(pwd, git_obj, code_dir):
    """
    拉取graph组件的源码：如果本路径有代码库则更新即可；没有代码库则拉取最新代码
    :param pwd: 路径
    :param git_obj: git 配置
    :param code_dir:
    """
    branch = git_obj['branch']
    url = git_obj['url']
    if not is_match_re(pwd, code_dir):
        clone_cmd = 'cd %s && git clone %s && cd %s && git checkout %s' % (pwd, url, code_dir, branch)
        print('clone code cmd: ' + clone_cmd)
        os.system(clone_cmd)
    else:
        pull_cmd = 'cd %s/%s && git checkout %s && git pull' % (pwd, code_dir, branch)
        print('pull code cmd: ' + pull_cmd)
        os.system(pull_cmd)


def compile_package(dir_code_path):
    """
    编译包
    :param dir_code_path: 本地代码库路径
    :return:
    """
    g_name = dir_code_path.split('/')[-1]
    if g_name == 'hugegraph-loader':
        cmd = 'cd %s && ' \
              'mvn install:install-file ' \
              '-Dfile=./assembly/static/lib/ojdbc8-12.2.0.1.jar ' \
              '-DgroupId=com.oracle ' \
              '-DartifactId=ojdbc8 ' \
              '-Dversion=12.2.0.1 ' \
              '-Dpackaging=jar | grep -v \"Downloading\|Downloaded\" && ' \
              'mvn clean package -Dmaven.test.skip=true -q | grep \"tar.gz\"' % dir_code_path
        print(cmd)
        os.system(cmd)
    else:
        cmd = 'cd %s && mvn clean package -DskipTests' % dir_code_path
        print(cmd)
        os.system(cmd)


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

    if _cfg.is_auth is True:
        graph_conf = package_dir_path + f'/conf/graphs/{_cfg.graph_name}.properties'
        alter_properties(graph_conf,
                         'gremlin.graph=org.apache.hugegraph.HugeFactory'
                         'gremlin.graph=org.apache.hugegraph.auth.HugeFactoryAuthProxy')

        alter_properties(rest_conf,
                         '#auth.authenticator=',
                         'auth.authenticator=org.apache.hugegraph.auth.ConfigAuthenticator')

        # alter_properties(gremlin_conf,
        #                  )


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
            '&& ./bin/init-store.sh '
            '&& ./bin/start-hugegraph.sh' % package_dir_path
        )
    else:
        os.system(
            'cd %s '
            '&& ./bin/start-hubble.sh' % package_dir_path
        )


class Deploy:
    """
    图库组件部署
    """

    def __init__(self, obj):
        self.graph_host = obj.graph_host
        self.server_port = obj.server_port
        self.gremlin_port = obj.gremlin_port
        self.hubble_host = obj.hubble_host
        self.hubble_port = obj.hubble_port
        self.code_path = obj.code_path
        self.server_git = obj.server_git
        self.loader_git = obj.loader_git
        self.tools_git = obj.tools_git
        self.hubble_git = obj.hubble_git

    @staticmethod
    def server(conf):
        """
        :return:
        """
        code_dir = 'incubator-hugegraph'
        server_module = 'hugegraph-server'
        build_dir_prefix = 'apache-hugegraph-incubating'
        code_dir_path = os.path.join(conf.code_path, code_dir)
        server_module_path = os.path.join(code_dir_path, server_module)
        re_dir = '^%s-(\d).(\d{1,2}).(\d)$' % build_dir_prefix

        is_exists_path(conf.code_path)
        get_code(conf.code_path, conf.server_git, code_dir)
        compile_package(code_dir_path)
        # start graph_server
        package_dir_name = is_match_re(server_module_path, re_dir)
        package_dir_path = os.path.join(server_module_path, package_dir_name)
        set_server_properties(package_dir_path, conf.graph_host, conf.server_port, conf.gremlin_port)
        start_graph(package_dir_path, 'server')

    @staticmethod
    def toolchain(conf):
        code_dir = 'incubator-hugegraph-toolchain'
        code_dir_path = os.path.join(conf.code_path, code_dir)
        is_exists_path(conf.code_path)
        get_code(conf.code_path, conf.toolchain_git, code_dir)
        compile_package(code_dir_path)

        # set properties && start hubble
        hubble_package_dir_name = os.path.join(code_dir_path,
                                               'apache-hugegraph-toolchain-incubating-1.0.0',
                                               'apache-hugegraph-hubble-incubating-1.0.0')
        # set_hubble_properties(hubble_package_dir_name, conf.graph_host, conf.hubble_port)
        start_graph(hubble_package_dir_name, 'hubble')

    @staticmethod
    def hubble(self):
        """
        :return:
        """
        code_dir = 'hugegraph-hubble'
        code_dir_path = self.code_path + '/' + code_dir
        re_dir = '^%s-(\d).(\d{1,2}).(\d)$' % code_dir
        # # get code && compile
        # is_exists_path(self.code_path)
        # get_code(self.code_path, self.hubble_git, code_dir)
        # compile_package(code_dir_path)
        # wget tar
        is_exists_path(code_dir_path)
        os.system(
            'cd %s && '
            'wget https://github.com/hugegraph/hugegraph-hubble/releases/download/v1.5.0/hugegraph-hubble-1.5.0.tar.gz -q'
            '&& tar xzvf hugegraph-hubble-1.5.0.tar.gz' % code_dir_path
        )
        # set properties && start hubble
        package_dir_name = is_match_re(code_dir_path, re_dir)
        package_dir_path = code_dir_path + '/' + package_dir_name
        set_hubble_properties(package_dir_path, self.graph_host, self.hubble_port)
        start_graph(package_dir_path, 'hubble')

    @staticmethod
    def loader(conf):
        """
        :return:
        """
        code_dir = 'hugegraph-loader'
        code_dir_path = conf.code_path + '/' + code_dir
        is_exists_path(conf.code_path)
        get_code(conf.code_path, conf.loader_git, code_dir)
        compile_package(code_dir_path)

    @staticmethod
    def tools(self):
        """
        :return:
        """
        code_dir = 'hugegraph-tools'
        code_dir_path = self.code_path + '/' + code_dir
        is_exists_path(self.code_path)
        get_code(self.code_path, self.tools_git, code_dir)
        compile_package(code_dir_path)


if __name__ == "__main__":
    pass

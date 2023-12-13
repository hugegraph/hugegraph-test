# -*- coding:utf-8 -*-
"""
author     : lxb
note       : Component deployment begins
create_time: 2020/4/22 5:17 下午
"""
import os
import subprocess
import sys

from config.basic_config import admin_password

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../')

from src.common.file_basic import is_match_re, append_properties
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
        cmd = 'cd %s && mvn clean package -P stage -DskipTests -ntp' % dir_code_path
        print(cmd)
        os.system(cmd)


def change_hubble_permission(hubble_path):
    res = subprocess.run(['chmod', '-R', '755', hubble_path], shell=False, capture_output=True, text=True)
    assert res.returncode == 0


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

    if _cfg.is_https:
        alter_properties(rest_conf,
                         'restserver.url=http://127.0.0.1:8080',
                         'restserver.url=https://127.0.0.1:8080')

    if _cfg.is_auth is True:
        graph_conf = package_dir_path + f'/conf/graphs/{_cfg.graph_name}.properties'
        alter_properties(graph_conf,
                         'gremlin.graph=org.apache.hugegraph.HugeFactory',
                         'gremlin.graph=org.apache.hugegraph.auth.HugeFactoryAuthProxy')

        alter_properties(rest_conf,
                         '#auth.authenticator=',
                         'auth.authenticator=org.apache.hugegraph.auth.StandardAuthenticator')

        alter_properties(rest_conf,
                         '#auth.graph_store=hugegraph',
                         'auth.graph_store=hugegraph')

        append_properties(gremlin_conf, '''
authentication: {
  authenticator: org.apache.hugegraph.auth.StandardAuthenticator,
  authenticationHandler: org.apache.hugegraph.auth.WsAndHttpBasicAuthHandler,
  config: {tokens: conf/rest-server.properties}
}
''')


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
    pa = admin_password.get('admin')
    if graph_type == 'server':
        os.system(
            'cd %s '
            f'&& echo "{pa}" | ./bin/init-store.sh '
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
        is_exists_path(conf.codebase_path)
        get_code(conf.codebase_path, conf.server_git, conf.server_local_repo)
        compile_package(conf.server_path)

        gen_dir = os.path.join(conf.codebase_path, conf.server_gen_dir)
        # start graph_server
        set_server_properties(
            gen_dir,
            conf.graph_host,
            conf.server_port,
            conf.gremlin_port
        )
        start_graph(gen_dir, 'server')

    @staticmethod
    def toolchain(conf):
        is_exists_path(conf.codebase_path)
        get_code(conf.codebase_path, conf.toolchain_git, conf.toolchain_local_repo)
        compile_package(conf.toolchain_path)
        # hubble load need to write files
        change_hubble_permission(conf.hubble_path)

        # set properties && start hubble
        # set_hubble_properties(hubble_package_dir_name, conf.graph_host, conf.hubble_port)
        start_graph(conf.hubble_path, 'hubble')


if __name__ == "__main__":
    pass

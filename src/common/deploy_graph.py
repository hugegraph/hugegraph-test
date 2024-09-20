# -*- coding:utf-8 -*-
"""
author     : lxb
note       : Component deployment begins
create_time: 2020/4/22 5:17 下午
"""
import os
import shutil
import subprocess
import sys

from src.config.basic_config import admin_password

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../')

from src.common.file_basic import is_match_re, append_properties
from src.common.file_basic import is_exists_path
from src.common.file_basic import alter_properties
from src.config import basic_config as _cfg


def get_code(pwd, git_obj, code_dir):
    """
    拉取 graph 组件的源码：如果本路径有代码库则更新即可；没有代码库则拉取最新代码
    :param pwd: 路径
    :param git_obj: git 配置
    :param code_dir:
    """
    branch = git_obj['branch']
    url = git_obj['url']
    if not is_match_re(pwd, code_dir):
        clone_cmd = 'cd %s && git clone --depth 5 %s && cd %s && git checkout -b %s' % (pwd, url, code_dir, branch)
        print('clone code cmd: ' + clone_cmd)
        os.system(clone_cmd)
    else:
        pull_cmd = 'cd %s/%s && git checkout -b %s && git pull' % (pwd, code_dir, branch)
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
        subprocess.check_call(cmd, shell=True)
    else:
        cmd = 'cd %s && mvn clean package -P stage -DskipTests -ntp' % dir_code_path
        print(cmd)
        subprocess.check_call(cmd, shell=True)


def change_hubble_permission(dir_path):
    res = subprocess.run(['chmod', '-R', '755', dir_path], shell=False, capture_output=True, text=True)
    assert res.returncode == 0
    print(f'stdout: ', res.stdout)
    print(f'stderr: ', res.stderr)


def set_server_properties(package_dir_path, host, server_port, gremlin_port):
    """
    修改 server 组件配置
    :return:
    """
    # 修改 rest-server.properties 文件
    rest_conf = package_dir_path + '/conf/rest-server.properties'
    alter_properties(rest_conf,
                     '127.0.0.1:8080',
                     '%s:%d' % (host, server_port))
    alter_properties(rest_conf,
                     '#gremlinserver.url=http://127.0.0.1:8182',
                     'gremlinserver.url=http://%s:%d' % (host, gremlin_port))
    # 修改 gremlin-server.yaml 文件
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

def set_pd_properties(package_dir_path, host, grpc_port, rest_port, store_list, raft_port, raft_list):
    """
    修改 pd 组件配置
    :return:
    """
    # 修改 application 文件
    application_conf = package_dir_path + '/conf/application.yml'
    alter_properties(application_conf,
                     '8686',
                     '%d' % grpc_port)
    alter_properties(application_conf,
                     '8620',
                     '%d' % rest_port)
    new_store_list = ','.join([f"{host}:{port}" for port in store_list])
    alter_properties(application_conf,
                     'initial-store-list: 127.0.0.1:8500',
                     'initial-store-list: %s' % new_store_list)
    alter_properties(application_conf,
                     'address: 127.0.0.1:8610',
                     'address: %s:%d' % (host, raft_port))
    new_raft_list = ','.join([f"{host}:{port}" for port in raft_list])
    alter_properties(application_conf,
                     'peers-list: 127.0.0.1:8610',
                     'peers-list: %s' % new_raft_list)

def set_store_properties(package_dir_path, host, pd_list, grpc_port, raft_port, rest_port):
    application_conf = package_dir_path + '/conf/application.yml'
    new_pd_list = ','.join([f"{host}:{port}" for port in pd_list])
    alter_properties(application_conf,
                     'address: localhost:8686',
                     'address: %s' % new_pd_list)
    alter_properties(application_conf,
                     'port: 8500',
                     'port: %d' % grpc_port)
    alter_properties(application_conf,
                     'address: 127.0.0.1:8510',
                     'address: %s:%d' % (host, raft_port))
    alter_properties(application_conf,
                     'address: 127.0.0.1:8610',
                     'address: %s:%d' % (host, raft_port))
    alter_properties(application_conf,
                     'port: 8520',
                     'port: %d' % rest_port)


def set_hubble_properties(package_dir_path, host, port):
    """
    修改 hubble 组件配置
    :return:
    """
    hubble_conf = package_dir_path + '/conf/hugegraph-hubble.properties'
    alter_properties(hubble_conf, 'server.host=localhost', 'server.host=%s' % host)
    alter_properties(hubble_conf, 'server.port=8088', 'server.port=%d' % port)


def start_graph(package_dir_path, graph_type):
    """
    启动 graph 包
    """
    pa = admin_password.get('admin')
    if graph_type == 'server':
        os.system(
            'cd %s '
            f'&& echo "{pa}" | ./bin/init-store.sh '
            '&& ./bin/start-hugegraph.sh' % package_dir_path
        )
    elif graph_type == 'pd':
        os.system(
            'cd %s '
            '&& ./bin/start-hugegraph-pd.sh' % package_dir_path
        )
    elif graph_type == 'store':
        os.system(
            'cd %s '
            '&& ./bin/start-hugegraph-store.sh' % package_dir_path
        )
    else:
        os.system(
            f'chmod -R 755 {package_dir_path}'
            '&& cd %s '
            '&& ./bin/start-hubble.sh' % package_dir_path
        )

def unzip_targz(file_path, file_name):
    cmd = f'cd {file_path} && tar -zxvf {file_name}'
    subprocess.check_call(cmd, shell=True)

def update_backend_properties(file_path, target_path):
    if(os.path.exists(target_path)):
        os.remove(target_path)
    shutil.copy2(file_path, target_path)


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
        self.host = obj.host
        self.pd_grpc_port = obj.pd_grpc_port
        self.pd_rest_port = obj.pd_rest_port
        self.store_list = obj.store_list
        self.pd_raft_port = obj.pd_raft_port
        self.raft_list = obj.raft_list
        self.pd_list = obj.pd_list
        self.store_grpc_port = obj.store_grpc_port
        self.store_raft_port = obj.store_raft_port
        self.store_rest_port = obj.store_rest_port

    @staticmethod
    def server(conf):
        """
        :return:
        """
        is_exists_path(conf.codebase_path)
        get_code(conf.codebase_path, conf.server_git, conf.server_local_repo)
        compile_package(conf.project_path)
        unzip_targz(conf.server_path, conf.server_tar_path.split('/')[-1])

        gen_dir = os.path.join(conf.codebase_path, conf.server_gen_dir)
        # start graph_server
        set_server_properties(
            gen_dir,
            conf.graph_host,
            conf.server_port,
            conf.gremlin_port
        )
        config_file_path = os.path.dirname(os.path.realpath(__file__)) + "/../dist/" + conf.server_backend + ".properties"
        target_path = os.path.join(conf.codebase_path, conf.server_gen_dir + '/conf/graphs/hugegraph.properties')
        update_backend_properties(config_file_path, target_path)
        start_graph(gen_dir, 'server')

    @staticmethod
    def pd(conf):
        """
        :return:
        """
        is_exists_path(conf.codebase_path)
        get_code(conf.codebase_path, conf.server_git, conf.pd_local_repo)
        compile_package(conf.project_path)
        unzip_targz(conf.pd_path, conf.pd_tar_path.split('/')[-1])

        gen_dir = os.path.join(conf.codebase_path, conf.pd_gen_dir)
        # start graph_server
        set_pd_properties(
            gen_dir,
            conf.host,
            conf.pd_grpc_port,
            conf.pd_rest_port,
            conf.store_list,
            conf.pd_raft_port,
            conf.raft_list
        )
        start_graph(gen_dir, 'pd')

    @staticmethod
    def store(conf):
        """
        :return:
        """
        is_exists_path(conf.codebase_path)
        get_code(conf.codebase_path, conf.server_git, conf.store_local_repo)
        compile_package(conf.project_path)
        unzip_targz(conf.store_path, conf.store_tar_path.split('/')[-1])

        gen_dir = os.path.join(conf.codebase_path, conf.store_gen_dir)
        # start graph_server
        set_store_properties(
            gen_dir,
            conf.host,
            conf.pd_list,
            conf.store_grpc_port,
            conf.store_raft_port,
            conf.store_rest_port
        )
        start_graph(gen_dir, 'store')

    @staticmethod
    def toolchain(conf):
        is_exists_path(conf.codebase_path)
        get_code(conf.codebase_path, conf.toolchain_git, conf.toolchain_local_repo)
        compile_package(conf.toolchain_path)
        # hubble load need to write files
        # change_hubble_permission(conf.hubble_path)

        # set properties && start hubble
        # set_hubble_properties(hubble_package_dir_name, conf.graph_host, conf.hubble_port)
        start_graph(conf.hubble_path, 'hubble')

    @staticmethod
    def hugegraph(conf):
        is_exists_path(conf.codebase_path)
        get_code(conf.codebase_path, conf.server_git, 'incubator-hugegraph')
        compile_package(conf.project_path)

        unzip_targz(conf.pd_path, conf.pd_tar_path.split('/')[-1])
        unzip_targz(conf.store_path, conf.store_tar_path.split('/')[-1])
        unzip_targz(conf.server_path, conf.server_tar_path.split('/')[-1])

        pd_gen_dir = os.path.join(conf.codebase_path, conf.pd_gen_dir)
        # start graph_server
        set_pd_properties(
            pd_gen_dir,
            conf.host,
            conf.pd_grpc_port,
            conf.pd_rest_port,
            conf.store_list,
            conf.pd_raft_port,
            conf.raft_list
        )
        start_graph(pd_gen_dir, 'pd')

        store_gen_dir = os.path.join(conf.codebase_path, conf.store_gen_dir)
        # start graph_server
        set_store_properties(
            store_gen_dir,
            conf.host,
            conf.pd_list,
            conf.store_grpc_port,
            conf.store_raft_port,
            conf.store_rest_port
        )
        start_graph(store_gen_dir, 'store')

        server_gen_dir = os.path.join(conf.codebase_path, conf.server_gen_dir)
        # start graph_server
        set_server_properties(
            server_gen_dir,
            conf.graph_host,
            conf.server_port,
            conf.gremlin_port
        )
        config_file_path = os.path.dirname(os.path.realpath(__file__)) + "/../dist/" + conf.server_backend + ".properties"
        target_path = os.path.join(conf.codebase_path, conf.server_gen_dir + '/conf/graphs/hugegraph.properties')
        update_backend_properties(config_file_path, target_path)
        start_graph(server_gen_dir, 'server')



if __name__ == "__main__":
    pass

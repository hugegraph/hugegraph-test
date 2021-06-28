# -*- coding:utf-8 -*-
"""
author     : lxb
note       : tools 测试
create_time: 2020/4/22 5:17 下午
"""
import os
import sys
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../')

from src.common.tools import run_shell
from src.common.tools import tools_assert
from src.common.tools import insert_data
from src.common.tools import clear_graph
from src.common.tools import target_clear_graph
from src.common.tools import target_insert_data
from src.config import basic_config as _cfg


class Test_tools:
    """
    tools测试
    """

    def test_tools_get_task(self):
        """
        查看task列表
        :return:
        """
        cmd = "./bin/hugegraph --url %s --graph %s %s %s task-list"
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').startswith('Tasks:')

    def test_tools_get_task_limit(self):
        """
        查看task列表 (limit 限制)
        :return:
        """
        cmd = "./bin/hugegraph --url  %s  --graph %s %s %s task-list --limit 3 "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').startswith('Tasks:')

    def test_tool_get_task_success(self):
        """
        查看task列表 (状态为成功)
        :return:
        """
        cmd = "./bin/hugegraph --url  %s  --graph %s %s %s task-list  --status success "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').startswith('Tasks:')

    def test_tool_get_mode(self):
        """
        查看图模式
        :return:
        """
        cmd = "./bin/hugegraph --url %s --graph %s %s %s graph-mode-get "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').startswith('Graph mode: NONE')

    def test_tool_set_mode_restore(self):
        """
        设置图模式 RESTORING
        :return:
        """
        cmd = "./bin/hugegraph --url %s --graph %s %s %s graph-mode-set -m RESTORING "
        res_restore = run_shell(cmd)
        stdout, stderr = res_restore.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res_restore.returncode == 0
        assert str(stdout, 'utf-8').startswith("Set graph '%s' mode to 'RESTORING'" % _cfg.graph_name)

        # 清空图模式
        res0 = run_shell("./bin/hugegraph --url %s --graph %s %s %s graph-mode-set -m NONE ")
        res0.communicate()
        # stdout, stderr = res0.communicate()
        # print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        print('设置图模式 RESTORING - 测试case结束 - 清空图模式')

    def test_tool_set_mode_merge(self):
        """
        设置图模式 MERGING
        :return:
        """
        cmd = "./bin/hugegraph --url  %s --graph %s %s %s  graph-mode-set -m MERGING "
        res_merging = run_shell(cmd)
        stdout, stderr = res_merging.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res_merging.returncode == 0
        assert str(stdout, 'utf-8').startswith("Set graph '%s' mode to 'MERGING'" % _cfg.graph_name)

        # 清空图模式
        res0 = run_shell("./bin/hugegraph --url  %s --graph %s %s %s  graph-mode-set -m NONE ")
        res0.communicate()
        # stdout, stderr = res0.communicate()
        # print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        print('设置图模式 MERGING - 测试case结束 - 清空图模式')

    def test_tool_get_graph(self):
        """
        查看图信息
        :return:
        """
        cmd = "./bin/hugegraph --url %s --graph %s %s %s graph-list "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').startswith('Graphs:')

    def test_tool_clear_graph(self):
        """
        清理图 并进行二次确认
        :return:
        """
        cmd = "./bin/hugegraph --url %s --graph %s %s %s graph-clear --confirm-message " \
              " \"I'm sure to delete all data\" "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        res_v, res_e = tools_assert()
        assert res.returncode == 0
        assert str(stdout, 'utf-8').startswith("Graph '%s' is cleared" % _cfg.graph_name) and \
               res_v == 0 and \
               res_e == 0

    def test_tool_backup_all(self):
        """
        备份所有数据
        :return:
        """
        clear_graph()
        insert_data()
        # 开始case测试
        cmd = "./bin/hugegraph --url %s --graph %s %s %s backup -t all --directory ./backup" + str(
            int(time.time()))
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        print(str(stdout, 'utf-8').split('backup summary: ')[1].split('\ncost time(s)')[0])
        assert res.returncode == 0
        assert str(stdout, 'utf-8').split('backup summary: ')[1].split('\ncost time(s)')[0] == \
               "{\n" \
               "\tproperty key number: 0,\n" \
               "\tvertex label number: 1,\n" \
               "\tedge label number: 1,\n" \
               "\tindex label number: 0,\n" \
               "\tvertex number: 6,\n" \
               "\tedge number: 8,\n}"

    def test_tool_backup_vertex(self):
        """
        备份顶点数据
        :return:
        """
        clear_graph()
        insert_data()
        # 开始case测试
        cmd = "./bin/hugegraph --url %s --graph %s %s %s backup " \
              "-t vertex --directory ./backup_" + str(int(time.time()))
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').split('backup summary: ')[1].split('\ncost time(s)')[0] == \
               "{\n" \
               "\tproperty key number: 0,\n" \
               "\tvertex label number: 0,\n" \
               "\tedge label number: 0,\n" \
               "\tindex label number: 0,\n" \
               "\tvertex number: 6,\n" \
               "\tedge number: 0,\n}"

    def test_tool_backup_edge(self):
        """
        备份边数据
        :return:
        """
        clear_graph()
        insert_data()
        # 开始case测试
        cmd = "./bin/hugegraph --url  %s --graph %s %s %s backup " \
              "-t edge --directory ./backup_" + str(int(time.time()))
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').split('backup summary: ')[1].split('\ncost time(s)')[0] == \
               "{\n" \
               "\tproperty key number: 0,\n" \
               "\tvertex label number: 0,\n" \
               "\tedge label number: 0,\n" \
               "\tindex label number: 0,\n" \
               "\tvertex number: 0,\n" \
               "\tedge number: 8,\n}"

    def test_tool_backup_schema(self):
        """
        备份schema数据
        :return:
        """
        clear_graph()
        insert_data()
        # 开始case测试
        cmd = "./bin/hugegraph --url %s --graph %s %s %s backup " \
              "-t vertex_label,edge_label,property_key,index_label " \
              "--directory ./backup_" + str(int(time.time()))
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').split('backup summary: ')[1].split('\ncost time(s)')[0] == \
               "{\n" \
               "\tproperty key number: 0,\n" \
               "\tvertex label number: 1,\n" \
               "\tedge label number: 1,\n" \
               "\tindex label number: 0,\n" \
               "\tvertex number: 0,\n" \
               "\tedge number: 0,\n}"

    def test_tool_restore(self):
        """
        恢复数据
        :return:
        """
        dir_data = "backup_" + str(int(time.time()))
        clear_graph()
        insert_data()
        ### 数据备份
        backup_cmd = "./bin/hugegraph --url %s --graph %s %s %s backup -t all --directory ./" + dir_data
        backup_res = run_shell(backup_cmd)
        backup_res.communicate()
        ### 清空数据
        clear_graph()
        ### 设置图模式
        mode_cmd = "./bin/hugegraph --url  %s --graph %s %s %s  graph-mode-set -m RESTORING "
        res_mode = run_shell(mode_cmd)
        res_mode.communicate()
        ### 恢复数据
        restore_cmd = "./bin/hugegraph --url %s --graph %s %s %s restore  -t all --directory ./" + dir_data
        restore_res = run_shell(restore_cmd)
        restore_res.communicate()
        res_v, res_e = tools_assert()
        assert backup_res.returncode == 0
        assert res_mode.returncode == 0
        assert restore_res.returncode == 0
        assert res_v == 6
        assert res_e == 8
        ### 恢复图模式
        mode_none = "./bin/hugegraph --url  %s --graph %s %s %s  graph-mode-set -m NONE "
        res_none = run_shell(mode_none)
        res_none.communicate()

    def test_tool_execute_gremlin(self):
        """
        执行gremlin语句
        :return:
        """
        clear_graph()
        insert_data()
        # 测试 case
        cmd = "./bin/hugegraph --url  %s --graph %s %s %s  " \
              "gremlin-execute --script 'g.V().count()' "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0 and str(stdout, 'utf-8').startswith('Run gremlin script\n6\n')

    def test_tool_execute_gremlin_job(self):
        """
        执行gremlin任务
        :return:
        """
        clear_graph()
        insert_data()
        ### 执行gremlin的job任务
        gremlin_cmd = "./bin/hugegraph --url %s --graph %s %s %s " \
                      "gremlin-schedule --script 'g.V().count()' "
        gremlin_res = run_shell(gremlin_cmd)
        stdout, stderr = gremlin_res.communicate()
        print(' ---> ' + str(stdout, 'utf-8') + str(stderr, 'utf-8'))
        ### 查看task内容
        time.sleep(60)
        task_id = str(stdout, 'utf-8').split('\n')[1].split(': ')[1]
        task_cmd = "./bin/hugegraph --url %s --graph %s %s %s task-get --task-id " + str(task_id)
        task_res = run_shell(task_cmd)
        task_stdout, task_stderr = task_res.communicate()
        print(' ---> ' + str(task_stdout, 'utf-8') + str(task_stderr, 'utf-8'))
        assert gremlin_res.returncode == 0
        assert task_res.returncode == 0
        assert str(task_stdout, 'utf-8').split('task_result=')[1].startswith('[6]')

    def test_tool_graph_migrate(self):
        """
        图迁移  需要两个server
        :return:
        """
        # 清空图模式
        res0 = run_shell("./bin/hugegraph --url  %s --graph %s %s %s  graph-mode-set -m NONE ")
        res0.communicate()

        clear_graph()
        insert_data()
        target_clear_graph()

        cmd = "./bin/hugegraph --url %s --graph %s %s %s migrate " \
              "--target-url %s " \
              "--target-graph %s " \
              "%s " \
              "%s " \
              "--graph-mode RESTORING "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').split('restore summary: ')[1].split('\ncost time(s)')[0] == \
               "{\n\tproperty key number: 0,\n" \
               "\tvertex label number: 1,\n" \
               "\tedge label number: 1,\n" \
               "\tindex label number: 0,\n" \
               "\tvertex number: 6,\n" \
               "\tedge number: 8,\n}"

    def test_tool_graph_merge(self):
        """
        合并图 需要两个server
        :return:
        """
        # 清空图模式
        res0 = run_shell("./bin/hugegraph --url  %s --graph %s %s %s  graph-mode-set -m NONE ")
        res0.communicate()

        clear_graph()
        insert_data()
        target_clear_graph()
        target_insert_data()
        ### 开始测试case
        cmd = "./bin/hugegraph --url %s --graph %s %s %s migrate " \
              "--target-url %s " \
              "--target-graph %s " \
              "%s " \
              "%s " \
              "--graph-mode MERGING "
        res = run_shell(cmd)
        stdout, stderr = res.communicate()
        print(' ---> ' + str(stdout) + ' === ' + str(stderr))
        assert res.returncode == 0
        assert str(stdout, 'utf-8').split('restore summary: ')[1].split('\ncost time(s)')[0] == \
               "{\n\tproperty key number: 0,\n" \
               "\tvertex label number: 1,\n" \
               "\tedge label number: 1,\n" \
               "\tindex label number: 0,\n" \
               "\tvertex number: 6,\n" \
               "\tedge number: 8,\n}"


if __name__ == "__main__":
    pass

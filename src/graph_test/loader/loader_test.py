# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 
create_time: 2020/11/06 15:17 下午
"""
import pytest
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../')
from src.common.loader import InsertData


@pytest.mark.caseL1
def test_load_1():
    """
    movie数据集 清空图导入
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true "
    res = InsertData(part_cmd=cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(str(stdout) + '\n' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_2():
    """
    movie数据集 导入前检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--check-vertex true "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(' ---> ' + str(stdout) + ' === ' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 22190
    assert res_assert[1] > 500  # 多进程导入点、边 边导入的数量不定


@pytest.mark.caseL0
def test_load_3():
    """
    movie数据集 导入时候发生特定异常进行重试次数设置
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--retry-times 10 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_4():
    """
    movie数据集 重试时间间隔（s）
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "x  " \
          "--retry-times 10 " \
          "--retry-interval 10 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_5():
    """
    movie数据集 最大插入错误条数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--max-insert-errors 5000 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_6():
    """
    movie数据集 最大解析错误条数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--max-parse-errors 5000 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_7():
    """
    movie数据集 插入最大条数限制
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--max-read-lines 10000000 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_8():
    """
    movie数据集 导入每个批次包含的条数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--batch-size 500 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_9():
    """
    movie数据集  只解析不导入模式
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--dry-run true "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 0
    assert res_assert[1] == 0


@pytest.mark.caseL0
def test_load_10():
    """
    movie数据集  设置批量导入并发数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--batch-insert-threads 50 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_11():
    """
    movie数据集  设置单条导入并发数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--single-insert-threads 5 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_12():
    """
    hlm数据集 导入时候发生特定异常进行重试次数设置
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--retry-times 10 "
    res = InsertData(cmd, schema='schema_hlm.groovy', struct='struct_hlm.json', dir='hlm').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 41
    assert res_assert[1] == 51


@pytest.mark.caseL0
def test_load_13():
    """
    hlm数据集 最大插入错误条数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--max-insert-errors 5000 "
    res = InsertData(cmd, schema='schema_hlm.groovy', struct='struct_hlm.json', dir='hlm').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 41
    assert res_assert[1] == 51


@pytest.mark.caseL0
def test_load_14():
    """
    hlm数据集 最大解析错误条数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--max-parse-errors 5000 "
    res = InsertData(cmd, schema='schema_hlm.groovy', struct='struct_hlm.json', dir='hlm').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 41
    assert res_assert[1] == 51


@pytest.mark.caseL0
def test_load_15():
    """
    hlm数据集 插入最大条数限制
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--max-read-lines 10000000 "
    res = InsertData(cmd, schema='schema_hlm.groovy', struct='struct_hlm.json', dir='hlm').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 41
    assert res_assert[1] == 51


@pytest.mark.caseL0
def test_load_16():
    """
    hlm数据集  设置批量导入并发数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--batch-insert-threads 50 "
    res = InsertData(cmd, schema='schema_hlm.groovy', struct='struct_hlm.json', dir='hlm').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 41
    assert res_assert[1] == 51


@pytest.mark.caseL0
def test_load_17():
    """
    hlm数据集 清空图导入 & 检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--check-basic_operation true "
    res = InsertData(cmd, schema='schema_hlm.groovy', struct='struct_hlm.json', dir='hlm').load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(str(stdout) + '\n' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 41
    assert res_assert[1] == 51


@pytest.mark.caseL0
def test_load_retry_times():
    """
    network数据集 导入时候发生特定异常进行重试次数设置
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--retry-times 10 "
    res = InsertData(cmd, schema='schema_network-1000.groovy', struct='struct_network-1000.json', dir='network') \
        .load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 1000
    assert res_assert[1] == 15156


@pytest.mark.caseL0
def test_load_set_insert_errors():
    """
    network数据集 最大插入错误条数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--max-insert-errors 5000 "
    res = InsertData(cmd, schema='schema_network-1000.groovy', struct='struct_network-1000.json', dir='network') \
        .load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 1000
    assert res_assert[1] == 15156


@pytest.mark.caseL0
def test_load_set_parse_errors():
    """
    network数据集 最大解析错误条数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--max-parse-errors 5000 "
    res = InsertData(cmd, schema='schema_network-1000.groovy', struct='struct_network-1000.json', dir='network') \
        .load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 1000
    assert res_assert[1] == 15156


@pytest.mark.caseL0
def test_load_set_max_lines():
    """
    network数据集 插入最大条数限制
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--max-read-lines 10000000 "
    res = InsertData(cmd, schema='schema_network-1000.groovy', struct='struct_network-1000.json', dir='network') \
        .load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 1000
    assert res_assert[1] == 15156


@pytest.mark.caseL0
def test_load_set_batch_concurrent():
    """
    network数据集  设置批量导入并发数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--batch-insert-threads 50 "
    res = InsertData(cmd, schema='schema_network-1000.groovy', struct='struct_network-1000.json', dir='network') \
        .load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 1000
    assert res_assert[1] == 15156


@pytest.mark.caseL0
def test_load_check_vertex():
    """
    network数据集 清空图导入 & 检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--check-basic_operation true "
    res = InsertData(cmd, schema='schema_network-1000.groovy', struct='struct_network-1000.json', dir='network') \
        .load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(str(stdout) + '\n' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 1000
    assert res_assert[1] == 15156


@pytest.mark.caseL0
def test_load_set_single_concurrent():
    """
    network数据集  设置单条导入并发数
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--single-insert-threads 5 "
    res = InsertData(cmd, schema='schema_network-1000.groovy', struct='struct_network-1000.json', dir='network') \
        .load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 1000
    assert res_assert[1] == 15156


@pytest.mark.caseL0
def test_load_error_file_reload():
    """
    movie数据集 进行错误文件导入
    """
    # 进行导入错误文件的生成
    cmd_error = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
                "--clear-all-data true  " \
                "--check-basic_operation true "
    res_error = InsertData(cmd_error, schema='schema_movie.groovy', struct='struct_movie.json',
                           dir='movie').load_graph()
    res_error.communicate()

    # 进行错误文件的导入
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--check-basic_operation true " \
          "--failure-mode true"
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json',
                     dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] > 500
    assert res_assert[1] > 500


@pytest.mark.caseL0
def test_load_breakpoint_continue():
    """
    movie数据集 断点续传
    """
    # 进行导入错误停止错误停止
    cmd_error = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
                "--clear-all-data true  " \
                "--check-vertex true "
    res_error = InsertData(cmd_error, schema='schema_movie.groovy', struct='struct_movie.json',
                           dir='movie').load_graph()
    res_error.communicate()

    # 进行断点续传
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--incremental-mode true "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015


@pytest.mark.caseL0
def test_load_close_print():
    """
    movie数据集 关闭动态打印信息
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true " \
          "--print-progress false "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    # res.communicate()
    stdout, stderr = res.communicate()
    print(str(stdout) + '\n' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert str(stdout, 'utf-8').split('\n')[1] == 'count metrics'
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


@pytest.mark.caseL0
def test_load_help_message():
    """
    movie数据集 查看help信息
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--help "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    # res.communicate()
    stdout, stderr = res.communicate()
    print(str(stdout) + '\n' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert str(stdout, 'utf-8').startswith("Usage: <main class> [options]")


if __name__ == "__main__":
    pass

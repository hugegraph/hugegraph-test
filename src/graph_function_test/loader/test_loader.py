# -*- coding:utf-8 -*-
"""
author     : lxb
note       : loader 测试
create_time: 2020/11/06 15:17 下午
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../')

from src.common.loader import InsertData


def test_load_clear_all_data():
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


def test_load_movie_check_data_null_error():
    """
    movie数据集 导入前检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--check-vertex true "
    res = InsertData(cmd, schema='schema_movie_01.groovy', struct='struct_movie_01.json', dir='movie').load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(' ---> ' + str(stdout) + ' === ' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49036
    assert res_assert[1] == 3011  # 加上check vertex时有bug：因为movie数据集中的不同顶点类型的ID会覆盖，导致边导入的时候会报错。


def test_load_movie_check_data_customizeId_error():
    """
    movie数据集 导入前检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--check-vertex true "
    res = InsertData(cmd, schema='schema_movie_01.groovy', struct='struct_movie_01.json', dir='movie').load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(' ---> ' + str(stdout) + ' === ' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49036
    assert res_assert[1] != 117356  # 加上check vertex时有bug：因为movie数据集中的不同顶点类型的ID会覆盖，导致边导入的时候会报错。


def test_load_check_vertex():
    """
    movie数据集 导入前检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--check-vertex true " \
          "--batch-insert-threads 1 " \
          "--single-insert-threads 1 " \
          "--max-parse-errors 1 " \
          "--max-insert-errors 1"
    res = InsertData(
        cmd,
        schema='schema_checkVertex.groovy',
        struct='struct_checkVertex.json',
        dir='check_vertex_data'
    ).load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(' ---> ' + str(stdout) + ' === ' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 22
    assert res_assert[1] == 9


def test_load_movie_retry_times():
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


def test_load_retry_interval():
    """
    movie数据集 重试时间间隔（s）
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--retry-times 10 " \
          "--retry-interval 10 "
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json', dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


def test_load_movie_max_insert_errors():
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


def test_load_movie_max_parse_errors():
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


def test_load_movie_max_read_lines():
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


def test_load_batch_size():
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


def test_load_dry_run():
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


def test_load_movie_batch_insert_threads():
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


def test_load_single_insert_threads():
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


def test_load_hlm_retry_times():
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


def test_load_hlm_max_insert_errors():
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


def test_load_hlm_max_parse_errors():
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


def test_load_hlm_max_read_lines():
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


def test_load_hlm_batch_insert_threads():
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


# TODO "--check-basic_operation true "
# Was passed main parameter '--check-basic_operation' but no main parameter was defined in your arg class
def test_load_check_basic_operation():
    """
    hlm数据集 清空图导入 & 检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  "
    res = InsertData(cmd, schema='schema_hlm.groovy', struct='struct_hlm.json', dir='hlm').load_graph()
    res.communicate()
    # stdout, stderr = res.communicate()
    # print(str(stdout) + '\n' + str(stderr))
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    assert res_assert[0] == 41
    assert res_assert[1] == 51


def test_load_network_retry_times():
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


# TODO "--check-basic_operation true "
def test_load_network_check_vertex():
    """
    network数据集 清空图导入 & 检查顶点
    """
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true"
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


# TODO "--check-basic_operation true "
def test_load_error_file_reload():
    """
    movie数据集 进行错误文件导入
    """
    # 进行导入错误文件的生成
    cmd_error = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
                "--clear-all-data true"
    res_error = InsertData(cmd_error, schema='schema_movie.groovy', struct='struct_movie.json',
                           dir='movie').load_graph()
    res_error.communicate()

    # 进行错误文件的导入
    cmd = "%s/bin/hugegraph-loader.sh -h %s  -p %d  -g %s -f %s -s %s " \
          "--clear-all-data true  " \
          "--failure-mode true"
    res = InsertData(cmd, schema='schema_movie.groovy', struct='struct_movie.json',
                     dir='movie').load_graph()
    res.communicate()
    res_assert = InsertData().loader_assert()
    print(res_assert)
    assert res.returncode == 0
    # TODO
    # assert res_assert[0] > 500
    # assert res_assert[1] > 500


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
    # todo exist warning msg in JDK11
    # assert str(stdout, 'utf-8').split('\n')[1] == 'count metrics'
    assert 'count metrics' in str(stdout, 'utf-8')
    assert res_assert[0] == 49015
    assert res_assert[1] == 117356


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
    # todo warning msg in JDK11
    # assert str(stdout, 'utf-8').startswith("Usage: <main class> [options]")
    assert "Usage: <main class> [options]" in str(stdout, 'utf-8')


if __name__ == "__main__":
    pass

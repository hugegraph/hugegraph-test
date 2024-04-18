# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 通过异步任务获取执行结果
create_time:  
"""
import os
import sys
import json
import time

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../..')

from src.common.server_api import Task
from src.common.server_api import Computer


def get_task_res(id, time_out, auth=None):
    """
    获取某个异步任务的最终执行结果
    :param time_out: 最终执行结果的超时时间
    :param id: 任务ID
    :param auth: 权限
    :return:
    """
    code, res = Task().get_task(id=id, auth=auth)
    for i in range(0, int(time_out / 5)):
        if code == 200:
            if res["task_status"] == "failed":
                print(' +++ get task filed +++ ' + str(res))
                assert 0
            elif res["task_status"] == "success":
                print(res)
                if "task_result" in res:
                    result = json.loads(res["task_result"])
                    if result is None:
                        return 1
                    else:
                        return result
                else:
                    return 1
            else:
                time.sleep(5)
                code, res = Task().get_task(id=id, auth=auth)
        else:
            print('通过ID获取异步任务接口报错！')


def get_algorithm_job(job_id, auth=None):
    """
    获取异步算法任务的结果
    """
    code, res = Computer().get_computer_job(job_id=job_id, auth=auth)
    print(code, res)
    if code == 200:
        if res["task_status"] == "running":
            time.sleep(8)
            get_algorithm_job(job_id, auth=auth)
        elif res["task_status"] == "success":
            assert 1
            return 1
        else:
            print(' +++ get task filed +++ ' + str(res))
            assert 0
    else:
        print('通过ID获取异步任务接口报错！')
        assert 0


if __name__ == "__main__":
    pass

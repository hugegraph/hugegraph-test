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


def get_task_res(id, time_out, auth=None):
    """
    获取某个异步任务的最终执行结果
    :param time_out: 最终执行结果的超时时间
    :param id: 任务ID
    :param auth: 权限
    :return:
    """
    code, res = Task().get_task(id, auth)
    for i in range(0, int(time_out / 5)):
        if code == 200:
            if res["task_status"] == "failed":
                print(' +++ get task filed +++ ' + str(res))
                return res
            elif res["task_status"] == "success":
                result = json.loads(res["task_result"])
                return result
            else:
                time.sleep(5)
                code, res = Task().get_task(id, auth)
        else:
            print('通过ID获取异步任务接口报错！')


if __name__ == "__main__":
    pass


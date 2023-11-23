# -*- coding:utf-8 -*-
"""
author     : lxb
note       : get_kout
time       : 2021/8/17 17:03
"""
import random
import requests

# graph12_url = 'http://xx-scylladb01.yq01.xxx.com:8585/graphs/hugegraph/traversers/kout?source=%d&direction=BOTH&max_depth=3'
# graph11_url = 'http://xx-scylladb01.yq01.xxx.com:8761/graphs/hugegraph/traversers/kout?source=%d&direction=BOTH&max_depth=3'
# data_list = [55, 10, 15, 20, 25, 30, 35, 40, 45, 50, 9972, 3172, 6239, 624, 11728, 4035, 8726, 2693, 14063, 3330]

# total_time = 0
# for v_id in data_list:
#     res = get_kout(graph11_url, v_id)
#     total_time += res[1]
#     print(res)
# print(total_time)


graph_dict = {
    'graph12': 'xx-scylladb01.yq01.xxx.com:8585',
    'graph11': 'xx-scylladb01.yq01.xxx.com:8761'
}


def get_kout(url):
    """
    函数
    :param mark: 标记
    :param url: 请求 request 的 url
    """
    res = requests.get(url)
    amount = len(res.json()['vertices'])
    request_time = res.elapsed.microseconds / 1000
    return amount, request_time


if __name__ == "__main__":
    # total_time_12 = 0
    # total_time_11 = 0
    # for i in range(1, 100):
    #     v_id = random.randint(1, 10000000)
    #     for k, v in graph_dict.items():
    #         mark = k + '_' + str(v_id)
    #         url = "http://%s/graphs/hugegraph/traversers/kout?source=%d&direction=BOTH&max_depth=3" % (v, v_id)
    #         res = get_kout(mark, url)
    #         print(res)
    #         if k == 'graph12':
    #             total_time_12 += res[2]
    #         else:
    #             total_time_11 += res[2]
    # print('graph12: ' + str(total_time_12))
    # print('graph11: ' + str(total_time_11))

    f = open('./kout-3-temp.txt', 'a')
    for i in range(1, 500000):
        v_id = random.randint(1, 10000000)
        f.write(str(v_id) + '\n')
    f.close()

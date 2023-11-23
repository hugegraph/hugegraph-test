# -*- coding:utf-8 -*-
"""
author  : lxb
note    : create_dataset_100w
time    : 2022/6/7 下午 4:38
"""
import requests
import random

host = "xx.xx.139.6"
port = 8080
space = "DEFAULT"
graph = "lxb"
read_file = "./tmp.txt"
write_file = "./tmp1.txt"


def get_kout(url):
    """
    函数
    :param url: 请求 request 的 url
    """
    headers = {
        'Authorization': 'Basic YWRtaW46YWRtaW4='
    }
    res = requests.request("GET", url, headers=headers, timeout=60)
    if res.status_code == 200:
        res_list = res.json()['vertices']
        # print(url)
        # print(res_list)
        if len(res_list) > 0:
            return res_list
        else:
            print("warn: result is null, %s" % url)
    else:
        print("error: %s, %s" % (res.text, url))


if __name__ == "__main__":
    f = open(read_file, 'r')
    f_w = open(write_file, 'a')
    n = 0
    for i in f.readlines():
        v_id = i.split(',')[0]
        url = "http://%s:%d/graphspaces/%s/graphs/%s/traversers/kout?source=\"%s\"&direction=OUT&max_depth=3" % (
            host,
            port,
            space,
            graph,
            v_id
        )
        n += 1
        if n > 8100:
            print(url)
            v_list = get_kout(url)
            if v_list is not None:
                v_res = random.choice(v_list)
                f_w.write(str(v_id) + "," + str(v_res) + "\n")
                if n % 1000 == 0:
                    print("写入：%d条" % n)
                if n > 1000000:
                    break

    print("写入：%d条" % n)
    f.close()
    f_w.close()


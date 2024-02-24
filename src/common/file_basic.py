# -*- coding:utf-8 -*-
"""
author     : lxb
note       : 文件的基本操作
create_time: 2021/03/12
"""
import re
import os


def alter_properties(file, old_str, new_str):
    """
    替换文件中的内容
    :param file: 修改的文件
    :param old_str: 修改前的内容
    :param new_str: 修改后的内容
    :return:
    """
    with open(file, "r", encoding="utf-8") as f1, open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            f2.write(re.sub(old_str, new_str, line))
        os.remove(file)
        os.rename("%s.bak" % file, file)


def append_properties(file, add_content):
    with open(file, mode='a', encoding='utf-8') as f:
        f.write(add_content)


def is_match_re(dir_path, re_rule):
    """
    正则匹配
    """
    names = os.listdir(dir_path)
    res = None
    for name in names:
        match_obj = re.match(r'%s' % re_rule, name)
        if match_obj is not None:
            res = name
            break
    return res


def is_exists_path(dir_name):
    """
    判断是否存在文件夹，不存在则创建
    :param dir_name: 文件夹名称
    :return: True || False
    """
    if os.path.exists(dir_name):
        return True
    else:
        os.makedirs(dir_name)
        return False


if __name__ == "__main__":
    pass


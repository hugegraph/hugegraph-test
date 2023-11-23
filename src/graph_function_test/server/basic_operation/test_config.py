# -*- coding:utf-8 -*-
"""
author  : lxb
note    : test_config
time    : 2022/6/2 下午3:12
"""
import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path + '/../../../../')

from src.config import basic_config as _cfg
from src.common.server_api import GraphConfig

auth = None
if _cfg.is_auth:
    auth = _cfg.admin_password


def test_set_rest_config():
    """
    设置 rest配置
    :return:
    """
    pass


def test_get_rest_config():
    """
    获取 rest配置
    :return:
    """



def test_set_one_service_rest_config():
    """
    设置一个服务的rest配置
    :return:
    """
    pass


def test_get_one_service_rest_config():
    """
    获取一个服务的rest配置
    :return:
    """
    pass


def test_delete_one_service_rest_config():
    """
    删除一个服务的rest配置
    :return:
    """
    pass


def test_delete_one_service_rest_config_one_key():
    """
    删除一个服务的rest某一个配置项
    :return:
    """
    pass


def test_set_one_service_gremlin_config():
    """
    设置gremlin配置
    :return:
    """
    pass


def test_get_one_service_gremlin_config():
    """
    获取rest配置
    :return:
    """
    pass
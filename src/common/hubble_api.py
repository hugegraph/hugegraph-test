# -*- coding:utf-8 -*-
"""
author     : lxb
note       : hubble api
create_time:  
"""


class TestClass:
    """
    不想访问类变量和实例变量，可以用静态方法
    只想访问类内变量，不想访问实例变量用类方法
    即想访问类变量，也想访问实例变量用实例方法
    函数与静态方法相同，只是静态方法的作用域定义在类内
    """
    def __init__(self, a, b):
        self.name = a
        self.age = b

    def __del__(self):
        """
        析构方法在对象被销毁时被自动调用，建议不要在对象销毁时做任何事情，因为销毁的时间难以确定
        :return:
        """
        pass

    @staticmethod
    def test1(c, d):
        """
        静态方法
        :param c:
        :param d:
        :return:
        """
        return c + d

    @classmethod
    def test2(cls, e):
        """
        类方法
        :param d:
        :return:
        """
        cls.name = e
        return cls.name + "欢迎回来"

    def test3(self, f, g):
        """
        :param f:
        :param g:
        :return:
        """
        return f + g


def test_founction(a, b):
    """
    函数
    :param a:
    :param b:
    :return:
    """
    return a + b


if __name__ == "__main__":
    pass


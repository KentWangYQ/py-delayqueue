# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    @abstractmethod
    def keys(self, name):
        """
        从持久化介质获取集合中的所有keys
        :param name:
        :return: 返回keys的list
        """

    @abstractmethod
    def values(self, name):
        """
        从持久化介质获取集合中所有的values
        :param name:
        :return: 返回values的list
        """

    @abstractmethod
    def length(self, name):
        """
        持久化介质中name集合中的元素数量
        :param name:
        :return: 返回元素数量
        """

    @abstractmethod
    def get(self, name, key):
        """
        从持久化介质获取key对应的value
        :param name:
        :param key:
        :return: value object
        """

    @abstractmethod
    def m_get(self, name, keys):
        """
        从持久化介质获取“keys” list 中所有key对应的value
        :param name:
        :param keys:
        :return: 返回顺序与keys相同的value的list
        """

    @abstractmethod
    def get_all(self, name):
        """
        从持久化介质获取name下所有的kv
        :param name:
        :return: 返回kv的dict
        """

    @abstractmethod
    def set(self, name, key, value):
        """
        持久化kv对
        :param name: 集合名称
        :param key: 键
        :param value: 值
        :return: 成功返回1，失败返回0
        """

    @abstractmethod
    def m_set(self, name, mapping):
        """
        将“mapping” dict中的kv持久化
        :param name:
        :param mapping:
        :return: 成功返回True，失败返回False
        """

    @abstractmethod
    def delete(self, name, *keys):
        """
        从持久化介质删除keys list 中的key
        :param name:
        :param keys:
        :return: 成功返回1，失败返回0
        """

    @abstractmethod
    def exist(self, name, key):
        """
        查询key是否存在于持久化介质中
        :param name:
        :param key:
        :return: 存在返回True，不存在返回False
        """

    @abstractmethod
    def delete_collection(self, *names):
        """
        删除整个实体
        :param names:
        :return:
        """

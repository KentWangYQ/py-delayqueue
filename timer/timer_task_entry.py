# -*- coding: utf-8 -*-

import json
import uuid

from persist import PersistClient

_persist_client = PersistClient()
_persist_name = 'timer_task_entry'


class TimerTaskEntry(object):
    """
    延时任务
    支持任务列表链表结构
    """
    # 前驱任务
    prev = None
    # 后继任务
    next = None

    def __init__(self, expiration, task, *args, **kwargs):
        """
        初始化延时任务
        :param expiration: 过期时间
        :param task: 任务
        :param args:
        :param kwargs:
        """
        self.uuid = uuid.uuid1()
        self.expiration = expiration  # 过期时间
        self.__task = task  # 任务
        self.args = args
        self.kwargs = kwargs
        self.cancelled = False  # 任务取消

        _persist_client.set(_persist_name, self.uuid, self.__repr__())

    def __repr__(self):
        """
        序列化对象
        :return:
        """
        return json.dumps({'uuid': self.uuid,
                           'expiration': self.expiration,
                           'args': self.args,
                           'kwargs': self.kwargs})

    def run(self, *args, **kwargs):
        """
        运行task
        :param args:
        :param kwargs:
        :return:
        """
        # 运行task
        self.__task(*args, **kwargs)
        # task成功执行后，删除持久化数据
        _persist_client.delete(_persist_name, (self.uuid,))

    def cancel(self):
        """
        取消任务
        :return:
        """
        self.cancelled = True
        # 任务成功取消后，删除持久化数据
        _persist_client.delete(_persist_name, (self.uuid,))

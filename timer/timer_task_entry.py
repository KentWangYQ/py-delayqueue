# -*- coding: utf-8 -*-

import json
import uuid

from persist import PersistClient
from common import time_util

_persist_client = PersistClient()
PERSIST_NAME = 'timer_task_entry'


class TimerTaskEntry(object):
    """
    延时任务
    支持任务列表链表结构
    """

    @property
    def guid(self):
        return self._guid

    # 前驱任务
    prev = None
    # 后继任务
    next = None

    def __init__(self, expiration, task, guid=str(uuid.uuid1()), persist=True, *args, **kwargs):
        """
        初始化延时任务
        :param expiration: 过期时间
        :param task: 任务
        :param args:
        :param kwargs:
        """
        self._guid = guid
        self.expiration = expiration  # 过期时间
        self.__created = time_util.utc_now_timestamp_ms()  # 任务创建时间，用于持久化恢复
        self.__task = task  # 任务
        self.args = args
        self.kwargs = kwargs
        self.cancelled = False  # 任务取消
        self.__persist = persist
        if self.__persist:
            _persist_client.set(PERSIST_NAME, self.guid, self.__repr__())

    def __repr__(self):
        """
        序列化对象
        :return:
        """
        return json.dumps({'guid': self.guid,
                           'expiration': self.expiration,
                           'created': self.__created,
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

        if self.__persist:
            # task成功执行后，删除持久化数据
            _persist_client.delete(PERSIST_NAME, self.guid)

    def cancel(self):
        """
        取消任务
        :return:
        """
        self.cancelled = True

        if self.__persist:
            # 任务成功取消后，删除持久化数据
            _persist_client.delete(PERSIST_NAME, self.guid)

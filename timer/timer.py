# coding: utf-8

from multiprocessing import Lock
import json

from common import time_util
from persist import PersistClient
from .timer_task_entry import TimerTaskEntry, PERSIST_NAME as TTE_PERSIST_NAME
from .timing_wheel import TimingWheel
from .delay_queue import DelayQueue

TW_PERSIST_NAME = 'timing_wheel'


class Timer(object):
    """
    定时器
    支持延时和定时执行任务，任务列表右timing wheel管理，通过delay queue来驱动timing wheel.
    """
    __lock = Lock()

    __persist_client = PersistClient()

    # 延时队列
    delay_queue = DelayQueue()
    # 任务计数器
    task_counter = 0

    def __init__(self, tick_ms=1000, wheel_size=100, start_ms=time_util.utc_now_timestamp_ms()):
        self.timing_wheel = TimingWheel(tick_ms=tick_ms, wheel_size=wheel_size, start_ms=start_ms)

    def recover(self, task):
        """
        从上一次停止中恢复
        恢复timer状态和未执行的task
        :param task:
        :return:
        """
        # 获取timing_wheel的持久化数据
        start_ms, tick_ms, wheel_size, current_time = map(lambda v: int(v) if v else None,
                                                          self.__persist_client.m_get(TW_PERSIST_NAME,
                                                                                      ['start_ms', 'tick_ms',
                                                                                       'wheel_size',
                                                                                       'current_time']))
        if start_ms is None or tick_ms is None or wheel_size is None or current_time is None:
            # 未找到TimingWheel持久化数据，退出恢复过程。
            print('Recover: Do NOT find TimingWheel persist data!')
            return

        # 恢复timing_wheel的tick_ms和wheel_size
        self.timing_wheel.tick_ms = tick_ms
        self.timing_wheel.wheel_size = wheel_size

        # 获取timer_tasks的持久化数据
        timer_tasks = self.__persist_client.get_all(TTE_PERSIST_NAME)
        if timer_tasks is None or not isinstance(timer_tasks, dict):
            # 未找到Timer Tasks持久化数据，退出恢复过程
            print('Recover: Do NOT find timer tasks persist data!')
            return

        # 恢复timer_tasks
        for entry in timer_tasks.values():
            obj = json.loads(entry)
            # 计算新的expiration
            obj['expiration'] = max(obj.get('created') + (obj.get('expiration') or 0) - self.timing_wheel.start_ms, 0)
            # 重新向timer注册task
            self.add(TimerTaskEntry(expiration=obj.get('expiration'), task=task, guid=obj.get('guid'), *obj.get('args'),
                                    **obj.get('kwargs')))

    def persist(self):
        """
        持久化timer当前状态
        :return:
        """
        result = self.__persist_client.m_set(TW_PERSIST_NAME, {
            'start_ms': self.timing_wheel.start_ms,
            'tick_ms': self.timing_wheel.tick_ms,
            'wheel_size': self.timing_wheel.wheel_size,
            'current_time': self.timing_wheel.current_time
        })
        assert result, Exception('TimingWheel persist failed!')

    def add(self, timer_task_entry):
        """
        添加任务
        :param timer_task_entry:
        :return:
        """
        with self.__lock:
            # 向时间轮添加任务
            bucket, expiration_updated = self.timing_wheel.add(timer_task_entry)
            if bucket and expiration_updated:
                # 任务列表过期时间更新，向延时队列注册任务列表
                self.delay_queue.offer(bucket.expiration - self.timing_wheel.current_time, self.advance_clock, bucket)

    def advance_clock(self, bucket):
        """
        推进时间轮
        将时间轮推进到当前bucket的过期时间
        :param bucket:
        :return:
        """
        if bucket:
            # 推进时间轮
            self.timing_wheel.advance_clock(time_ms=bucket.expiration)
            # 刷新任务列表
            bucket.flush(self.add)

    def start(self):
        """
        启动Timer
        :return:
        """
        self.delay_queue.start()

    def shutdown(self):
        """
        关闭Timer
        :return:
        """
        self.delay_queue.shutdown()

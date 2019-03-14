# -*- coding: utf-8 -*-

import pydash as _
from kafka_util import consumer, producer

from timer.timer import Timer
from timer.timer_task_entry import TimerTaskEntry


def main():
    # 初始化
    timer = Timer()
    kafka_producer = producer.Producer()
    kafka_consumer = consumer.Consumer()

    # 到期callback
    def on_expired(message):
        print('Task expired!')
        target_topic = _.get(message, 'target_topic')
        if target_topic:
            kafka_producer.send(topic=target_topic, value=message)
            kafka_producer.flush()
        else:
            print('Enqueue: target_topic is missing in enqueue message!')

    # 订阅原始消息
    @kafka_consumer.event_emitter.on('message')
    def on_message(message):
        print('Receive delay task!')
        timer.add(
            TimerTaskEntry(expiration=(_.get(message, 'value.delay') or 0), task=on_expired, message=message.value))

    # 恢复上一次停机前状态
    timer.recover(task=on_expired)
    # 持久化当前状态
    timer.persist()
    # 启动Timer
    timer.start()
    # 启动原始消息订阅
    kafka_consumer.tail()


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

import pydash as _
from kafka_util import consumer, producer

from timer.timer import Timer
from timer.timer_task_entry import TimerTaskEntry


def main():
    timer = Timer()
    kafka_producer = producer.Producer()
    kafka_consumer = consumer.Consumer()

    @kafka_consumer.event_emitter.on('message')
    def on_message(message):
        timer.add(TimerTaskEntry(expiration=_.get(message, 'value.delay'), task=on_expired, message=message))

    def on_expired(message):
        target_topic = _.get(message, 'value.target_topic')
        if target_topic:
            kafka_producer.send(topic=target_topic, value=_.get(message, 'value'))
        else:
            print('Enqueue: target_topic is missing in enqueue message!')

    kafka_consumer.tail()


if __name__ == '__main__':
    main()
# TODO 启动时从持久化介质恢复数据，start_time和task_entry

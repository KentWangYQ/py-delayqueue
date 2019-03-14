# -*- coding: utf-8 -*-

import time
from json import loads
from kafka import KafkaConsumer

from config import settings
from common.event_emitter import EventEmitter


class Consumer(KafkaConsumer):
    def configure(self, **configs):
        pass

    def set_topic_partitions(self, *topics):
        pass

    def fetch_messages(self):
        pass

    def get_partition_offsets(self, topic, partition, request_time_ms, max_num_offsets):
        pass

    def offsets(self, group=None):
        pass

    def task_done(self, message):
        pass

    @property
    def topic_prefix(self):
        return settings.KAFKA.get('topic_prefix')

    @property
    def event_emitter(self):
        return self.__event_emitter

    def __init__(self):
        self.__event_emitter = EventEmitter()
        super().__init__(
            'dq_538cf_test2',
            bootstrap_servers=settings.KAFKA.get('hosts'),
            client_id=settings.KAFKA.get('client_id'),
            group_id=self.topic_prefix,
            # key_deserializer=lambda m: loads(m.decode('utf-8')),
            value_deserializer=lambda m: loads(m.decode('utf-8')),
            enable_auto_commit=True,
            auto_offset_reset='latest',
            session_timeout_ms=30000)
        # self.subscribe(pattern=('^%s*' % self.topic_prefix))

    def tail(self):
        while True:
            for message in self:
                try:
                    self.event_emitter.emit('message', message)
                except Exception as e:
                    self.event_emitter.emit('error', e)
            time.sleep(1)

# -*- coding: utf-8 -*-

from json import dumps
from kafka import KafkaProducer
from config import settings


class Producer(KafkaProducer):
    _topic_prefix = settings.KAFKA.get('topic_prefix') or ''

    def __init__(self):
        super().__init__(bootstrap_servers=settings.KAFKA.get('hosts'),
                         client_id=settings.KAFKA.get('client_id'),
                         # key_serializer=lambda m: dumps(m).encode('utf-8'),
                         value_serializer=lambda m: dumps(m).encode('utf-8'),
                         acks='all',
                         compression_type='gzip',
                         max_request_size=4194304)

    # def send(self, topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
    #     topic = self._topic_prefix + topic
    #     return super().send(topic, value, key, headers, partition, timestamp_ms)

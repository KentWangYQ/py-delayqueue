# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False
    KAFKA = {
        'hosts': [
            '172.16.1.2:9092',
            '172.16.1.3:9092'
        ],
        'topic_prefix': 'dq_4064a_',  # 'delay_queue'做sha256取后五位
        'client_id': 'delay_queue',
        'group_id': 'delay_queue_group'
    }
    REDIS = {
        'hosts': '127.0.0.1',
        'port': 6379,
        'db': 2,
        'expires': 0
    }
    REDIS_KEY = {
        'delay_queue': 'delay_queue'
    }
    PERSIST = {
        'client': 'redis'
    }

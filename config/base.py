# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False
    KAFKA = {
        'hosts': [
        ],
        'topic_prefix': 'dq_538cf_',  # 'delayqueue'做sha256取后五位
        'client_id': 'delay_queue'
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

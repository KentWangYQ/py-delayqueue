# -*- coding: utf-8 -*-

import unittest
from config import settings
from kafka_util.producer import Producer


class KafkaUtilTest(unittest.TestCase):
    def test_producer_send(self):
        producer = Producer()
        result = producer.send(settings.KAFKA.get('topic_prefix') + 'test2',
                               value={'delay': 5000, 'target_topic': 'dq_test1'})
        producer.flush()
        print(result.args)

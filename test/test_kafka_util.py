# -*- coding: utf-8 -*-

import unittest
from kafka_util.producer import Producer


class KafkaUtilTest(unittest.TestCase):
    def test_producer_send(self):
        producer = Producer()
        result = producer.send('dq_538cf_test2', value={'delay': 5800, 'target_topic': 'dq_538cf_test1'})
        producer.flush()
        print(result.args)

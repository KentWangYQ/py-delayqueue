# -*- coding: utf-8 -*-

import unittest
import uuid

from persist import PersistClient


class RedisClientTest(unittest.TestCase):
    def test_persist_client(self):
        name = str(uuid.uuid1())
        client = PersistClient()

        length = client.length(name)
        self.assertEqual(0, length, 'The keys length is NOT 0!')

        key, value = 'first', 'This is the first value'
        result = client.set(name, key, value)
        self.assertEqual(1, result, 'The set operate failed!')

        result = client.exist(name, key)
        self.assertTrue(result, 'The key exist by return False!')

        result = client.get(name, key)
        self.assertEqual(value, result, 'The result is NOT match with saved!')

        result = client.delete(name, key)
        self.assertEqual(1, result, 'The delete operate fai')

        result = client.exist(name, key)
        self.assertFalse(result, 'The key NOT exist by return True!')

        result = client.length(name)
        self.assertEqual(0, result, 'The keys length is NOT 0 after delete!')

        mapping = {
            'second': 'This is second key',
            'third': 'This is third key',
            '4th': '4th'
        }

        keys = list(mapping.keys())
        values = list(mapping.values())

        result = client.m_set(name, mapping)
        self.assertTrue(result, 'The m_set operate failed!')

        result = client.length(name)
        self.assertEqual(len(keys), result, 'The result is NOT match expect keys length!')

        result = client.m_get(name, keys[:-1])
        self.assertEqual(values[:-1], result, 'The result returned by m_get(...) is NOT match expect values!')

        result = client.get_all(name)
        self.assertEqual(mapping, result, 'The result returned by get_all(...) is NOT match expect values!')

        result = client.keys(name)
        self.assertEqual(keys, result, 'The result returned by keys(...) is NOT match expect keys list!')

        result = client.values(name)
        self.assertEqual(values, result, 'The result returned by values(...) is NOT match expect values list!')

        result = client.delete(name, *keys)
        self.assertEqual(len(keys), result, 'The delete(...) operate failed!')

        result = client.length(name)
        self.assertEqual(0, result, 'The length of keys is NOT 0 after delete all keys!')

        result = client.delete_collection(name)
        self.assertEqual(0, result, 'The delete_collection(..) operate failed!')

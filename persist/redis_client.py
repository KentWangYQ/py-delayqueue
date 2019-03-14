# -*- coding: utf-8 -*-

import redis

from .base import Base
from config import settings


class RedisClient(Base):
    def __init__(self):
        self.__name = ''
        self.__client = redis.Redis(host=settings.REDIS.get('host'), port=settings.REDIS.get('port'),
                                    db=settings.REDIS.get('db'), decode_responses=True)

    def keys(self, name):
        return self.__client.hkeys(name)

    def values(self, name):
        return self.__client.hvals(name)

    def length(self, name):
        return self.__client.hlen(name)

    def get(self, name, key):
        return self.__client.hget(name, key)

    def m_get(self, name, keys):
        return self.__client.hmget(name, keys)

    def get_all(self, name):
        return self.__client.hgetall(name)

    def set(self, name, key, value):
        return self.__client.hset(name, key, value)

    def m_set(self, name, mapping):
        return self.__client.hmset(name, mapping)

    def delete(self, name, *keys):
        return self.__client.hdel(name, *keys)

    def exist(self, name, key):
        return self.__client.hexists(name, key)

    def delete_collection(self, *names):
        return self.__client.delete(*names)

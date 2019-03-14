# -*- coding: utf-8 -*-

from config import settings
from .redis_client import RedisClient

__clients = {
    'redis': RedisClient
}

PersistClient = __clients[settings.PERSIST.get('client') or 'redis']

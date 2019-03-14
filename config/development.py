# -*- coding: utf-8 -*-

from .base import Config


class Development(Config):
    def __init__(self):
        self.KAFKA['hosts'] = [
            '172.16.100.60:9092',
            '172.16.100.61:9092']

# -*- coding: utf-8 -*-

from os import getenv

from . import base, development

DQ_DEBUG = str.lower(getenv('DQ_DEBUG') or '') == 'true'  # default: False
DQ_ENV = str.lower(getenv('DQ_ENV') or 'development')  # default: development

__config = {
    'base': base.Config(),
    'development': development.Development()
}

settings = __config[DQ_ENV]

app_info = {
    'name': 'py-delayqueue',
    'version': '0.0.1'
}

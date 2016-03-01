# -*- coding: utf-8 -*-
__author__ = 'Warlock'

from logger import logger

def handle_exception(func):
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            logger.fatal('{0}. {1}'.format(func.__name__, ex))

    return wrapped
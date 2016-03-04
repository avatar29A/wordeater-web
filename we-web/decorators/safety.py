# -*- coding: utf-8 -*-

import errors

from functools import wraps
from logger import error

__author__ = 'Glebov Boris'


def safety(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as ex:
            error(f.__name__, ex)
            return errors.ServerErrors.internal_server_error([])

    return decorated
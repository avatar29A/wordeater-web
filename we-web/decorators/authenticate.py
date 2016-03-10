# coding=utf-8
import json
import config
import errors

from flask import request, session, redirect
from functools import wraps

from services.service_locator import ServiceLocator
from logger import logger


__author__ = 'Glebov Boris'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return json.dumps({'access': False})


def allow_debug_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not config.IS_DEBUG:
            return errors.SignErrors.access_denided([])

        return f(*args, **kwargs)
    return decorated


def expose(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        if not ss.check():
            return authenticate()

        return f(*args, **kwargs)
    return decorated

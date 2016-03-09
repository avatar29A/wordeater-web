# coding=utf-8
import json

from flask import request, session, redirect
from functools import wraps
from logger import logger


__author__ = 'Glebov Boris'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return json.dumps({'access': False})


def expose(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get('user')

        if user is None:
            return authenticate()

        return f(*args, **kwargs)
    return decorated

# coding=utf-8
import uuid
import json

from flask import request, session, redirect
from functools import wraps
from logger import logger

from services.service_locator import ServiceLocator

from domain.model import db


__author__ = 'Glebov Boris'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return json.dumps({'access': False})


def expose(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get('user')

        if user is None:
            return redirect('/')

        return f(*args, **kwargs)
    return decorated


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = session.get('user')

        if user is None:
            user_service = ServiceLocator.resolve(ServiceLocator.USERS)
            la_service = ServiceLocator.resolve(ServiceLocator.LOGIN_AUDIT)

            new_user = user_service.create(u"user_{0}".format(unicode(uuid.uuid4())), u'en', u'it')
            la_service.create(new_user.login, unicode(request.remote_addr))

            session['user'] = {
                'id': str(new_user.id),
                'login': new_user.login,
                'remote_addr': unicode(request.remote_addr)
            }

        return f(*args, **kwargs)
    return decorated
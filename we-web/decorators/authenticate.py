# coding=utf-8
__author__ = 'Warlock'

from flask import request, session, redirect
from functools import wraps
from logger import logger

from services.users import UserService
from services.login_audits import LoginAutits

from domain.model import db

import uuid

import json

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
            user_service = UserService(db)
            new_user = user_service.create(u"user_{0}".format(unicode(uuid.uuid4())), u'en', u'it')

            session['user'] = {
                'id': str(new_user.id),
                'login': new_user.login
            }

            try:
                la = LoginAutits(db)
                la.create(new_user.login, unicode(request.remote_addr))
            except Exception as ex:
                logger.error(ex.message)

        return f(*args, **kwargs)
    return decorated
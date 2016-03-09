# coding=utf-8

from config import API_PATH
from decorators.authenticate import expose
from logger import logger
from flask.ext.restplus import Resource
from flask import session, request
from app import api


__author__ = 'Glebov Boris'

users_ns = api.namespace(name='Users', description="Requests related with users", path=API_PATH)


@users_ns.route('/users/auth/', endpoint='users/auth/')
class UserAuthAPI(Resource):
    def post(self):
        u"""
        Return groups by user.
        :return:
        """
        return {
            'data': '3434'
        }


#
#
# CHECK API
CHECK_PARAMS = {
    'username': 'User name',
    'email': "User's email",
}


@users_ns.route('/users/auth/check/', endpoint='users/auth/check/')
class UserCheckAPI(Resource):
    @api.doc(params=CHECK_PARAMS)
    def get(self):
        return {
            'username': True,
            'email': None
        }

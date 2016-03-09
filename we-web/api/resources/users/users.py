# coding=utf-8

from flask.ext.restplus import Resource
from flask import session, request
from cerberus import Validator

from config import API_PATH, ENVELOPE_DATA
from utils.wordeater_api import ApiResponse
from app import api

from models import CHECK_PARAMS, \
    user_schema, user_fields, user_input_fields, user_signin_fields, user_signin_schema,\
    check_user_fields
from logger import logger


__author__ = 'Glebov Boris'

users_ns = api.namespace(name='Users', description="Requests related with users", path=API_PATH)


#
#
# SIGNIN API


@users_ns.route('/user/sigin/', endpoint='user/sigin/')
class UserSignInAPI(Resource):
    @api.doc(body=user_signin_fields)
    @api.marshal_with(user_fields, envelope=ENVELOPE_DATA, code=200)
    def post(self):
        v = Validator(user_signin_schema)
        args = v.validate(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        return {
            u'id': u'123-34-343',
            u'username': u'Warlock',
            u'email': u'Example',
            u'auth_token': u'34llsadsf'
        }


#
#
# SIGNUP API

@users_ns.route('/user/signup/', endpoint='user/signup/')
class UserSignUpAPI(Resource):
    @api.doc(body=user_input_fields)
    @api.marshal_with(user_fields, envelope=ENVELOPE_DATA, code=201)
    def post(self):
        v = Validator(user_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        return {
            u'id': u'123-34-343',
            u'username': u'Warlock',
            u'email': u'Example',
            u'auth_token': u'34llsadsf'
        }

#
#
# CHECK API


@users_ns.route('/users/check/', endpoint='users/check/')
class UsersCheckAPI(Resource):
    @api.doc(params=CHECK_PARAMS)
    @api.marshal_with(check_user_fields, envelope=ENVELOPE_DATA, as_list=False)
    def get(self):
        return {
            'username': True,
            'email': None
        }

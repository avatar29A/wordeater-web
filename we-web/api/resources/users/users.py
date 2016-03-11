# coding=utf-8

import errors

from flask.ext.restplus import Resource
from flask import session, request
from cerberus import Validator

from config import API_PATH, ENVELOPE_DATA
from utils.wordeater_api import ApiResponse
from app import api

from models import user_schema, user_fields, user_input_fields, user_list_fields, user_signin_fields, user_signin_schema,\
    user_sigin_response_fields, check_user_fields, check_params_schema, check_user_input_fields

from services.service_locator import ServiceLocator
from services.exceptions import LoginAlreadyExists, EmailAlreadyExists
from decorators.authenticate import allow_debug_only

from logger import error


__author__ = 'Glebov Boris'

users_ns = api.namespace(name='Users', description="Requests related with users", path=API_PATH)


@users_ns.route('/users/', endpoint='users/')
class UsersAPI(Resource):
    @allow_debug_only
    @api.marshal_with(user_list_fields, envelope=ENVELOPE_DATA, as_list=True)
    def get(self):
        """
        Returns list of users
        :return: list of users
        """

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        users = list(us.list())

        return users

#
#
# SIGNIN API


@users_ns.route('/user/signin/', endpoint='user/signin/')
class UserSignInAPI(Resource):
    @api.doc(body=user_signin_fields)
    @api.marshal_with(user_sigin_response_fields, envelope=ENVELOPE_DATA, code=200)
    def post(self):
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        v = Validator(user_signin_schema)

        args = v.validated(request.get_json())
        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        login = args.get(u'login')
        password = args.get(u'password')

        user = us.sign_in(login, password)
        if user is None:
            return ApiResponse(status=4001, errors=errors.SignErrors.login_or_password_wrong(['login', 'password']))

        token = us.make_auth_token(user)

        # Save the user to session
        ss.create(user, token)

        user[u'auth_token'] = token

        return user

#
#
# SIGNUP API


@users_ns.route('/user/signup/', endpoint='user/signup/')
class UserSignUpAPI(Resource):
    @api.doc(body=user_input_fields)
    @api.marshal_with(user_fields, envelope=ENVELOPE_DATA, code=201)
    def post(self):
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        v = Validator(user_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        login = args.get('login')
        email = args.get('email')
        password = args.get('password')

        first_name = args.get('first_name')
        last_name = args.get('last_name')

        try:
            us.check(login, email)

            user = us.create(login, email, password, first_name=first_name, last_name=last_name)

            # Create session
            token = us.make_auth_token(user)
            ss.create(user, token)

            user['auth_token'] = token

            return user
        except LoginAlreadyExists as ex:
            error(u'UserService.signup({0})'.format(login), ex)

            return ApiResponse(status=4001, errors=errors.SignErrors.login_already_exists(['login']))
        except EmailAlreadyExists as ex:
            error(u'UserService.signup({0})'.format(email), ex)

            return ApiResponse(status=4001, errors=errors.SignErrors.email_already_exists(['email']))
        except Exception as ex:
            error(u'UserSignUpAPI -> us.create({0})'.format(login), ex)

            return ApiResponse(status=500, errors=errors.ServerErrors.internal_server_error([]))

#
#
# CHECK API


@users_ns.route('/users/check/', endpoint='users/check/')
class UsersCheckAPI(Resource):
    @api.doc(body=check_user_input_fields)
    @api.marshal_with(check_user_fields, envelope=ENVELOPE_DATA, as_list=False)
    def post(self):
        us = ServiceLocator.resolve(ServiceLocator.USERS)

        v = Validator(check_params_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        try:
            login = args.get('login', None)
            email = args.get('email', None)

            login_result = login and us.check_login(login)
            email_result = email and us.check_email(email)

            return {
                'login': login_result,
                'email': email_result
            }

        except Exception as ex:
            error(u'UsersCheckAPI.post', ex)

            return {
                'login': None,
                'email': None
            }

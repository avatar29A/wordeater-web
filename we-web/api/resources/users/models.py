# coding=utf-8
from app import api
from flask.ext.restplus import fields
from validators import validate_user_login
from utils.cerberus_utils import get_input_model_from_cerberus_schema


user_schema = {
    'username': {'type': 'string', 'required': True, 'nullable': False, 'empty': False, 'validator': validate_user_login},
    'password': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    'email': {'type': 'string', 'required': True, 'nullable': False, 'empty': False}
}


user_fields = api.model(u'User', {
    u'id': fields.String,
    u'auth_token': fields.String,
    u'username': fields.String,
    u'email': fields.String
})

user_input_fields = get_input_model_from_cerberus_schema(user_schema, 'UserInput')

#
# Sign In
user_signin_schema = {
    'username': {'type': 'string', 'required': True, 'nullable': False, 'empty': False, 'validator': validate_user_login},
    'password': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
}

user_signin_fields = api.model(u'UserSigIn', {
    u'username': fields.String,
    u'password': fields.String
})


#
#
# CHECK API

CHECK_PARAMS = {
    'username': 'User name',
    'email': "User's email",
}

check_user_fields = api.model(u'CheckUserModel', {
    u'username': fields.Boolean,
    u'email': fields.Boolean
})

# coding=utf-8
from app import api
from flask.ext.restplus import fields
from validators import validate_user_login
from utils.cerberus_utils import get_input_model_from_cerberus_schema


user_schema = {
    'login': {'type': 'string', 'required': True, 'nullable': False, 'empty': False, 'validator': validate_user_login},
    'password': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    'email': {'type': 'string', 'required': True, 'nullable': False, 'empty': False}
}


user_fields = api.model(u'User', {
    u'auth_token': fields.String,
    u'login': fields.String,
    u'first_name': fields.String,
    u'last_name': fields.String,
    u'foreign_lng': fields.String,
    u'native_lng': fields.String
})


user_input_fields = get_input_model_from_cerberus_schema(user_schema, 'UserInput')

#
# Sign In
user_signin_schema = {
    'login': {'type': 'string', 'required': True, 'nullable': False, 'empty': False, 'validator': validate_user_login},
    'password': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
}

user_sigin_response_fields = api.model(u'UserSiginResponseModel', {
    u'first_name': fields.String,
    u'last_name': fields.String,
    u'auth_token': fields.String,
    u'foreign_lng': fields.String,
    u'native_lng': fields.String
})

user_signin_fields = api.model(u'UserSigIn', {
    u'login': fields.String,
    u'password': fields.String
})


#
#
# CHECK API

CHECK_PARAMS = {
    u'login': u'User name',
    u'email': u"User's email",
}

check_user_fields = api.model(u'CheckUserModel', {
    u'login': fields.Boolean,
    u'email': fields.Boolean
})

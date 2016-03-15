# coding=utf-8

from app import api
from flask.ext.restplus import fields
from utils.cerberus_utils import get_input_model_from_cerberus_schema

__author__ = 'Warlock'

card_schema = {
    u'foreign': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    u'native': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    u'transcription': {'type': 'string', 'required': False, 'nullable': True, 'empty': True},
    u'context': {'type': 'string', 'required': False, 'nullable': True, 'empty': True},
    u'image_url': {'type': 'string', 'required': False, 'nullable': True, 'empty': True}
}

card_input_fields = get_input_model_from_cerberus_schema(card_schema, 'CardInput')

card_list_fields = api.model(u'CardList', {
    u'id': fields.String,
    u'user_id': fields.String,
    u'group_id': fields.String,
    u'foreign': fields.String,
    u'native': fields.String,
    u'transcription': fields.String,
    u'context': fields.String,
    u'image_url': fields.String,
    u'is_studying': fields.Boolean,
    u'is_done': fields.Boolean
})

card_fields = card_list_fields

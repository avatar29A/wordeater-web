# coding=utf-8

from app import api
from flask.ext.restplus import fields
from utils.cerberus_utils import get_input_model_from_cerberus_schema


picture_schema = {
    u'text': {'type': 'string', 'required': True, 'nullable': False, 'empty': False}
}

picture_input_fields = get_input_model_from_cerberus_schema(picture_schema, u'GroupInput')

picture_fields = api.model(u'TranslationModel', {
    u'id': fields.String,
    u'text': fields.String
})
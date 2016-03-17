# coding=utf-8

from app import api
from flask.ext.restplus import fields
from utils.cerberus_utils import get_input_model_from_cerberus_schema


translation_schema = {
    u'text': {'type': 'string', 'required': True, 'nullable': False, 'empty': False}
}

translation_input_fields = get_input_model_from_cerberus_schema(translation_schema, u'GroupInput')

translation_fields = api.model(u'TranslationModel', {
    u'text': fields.String,
    u'direction': fields.String,
    u'variations': fields.List(fields.String)
})

translation_detect_fields = api.model(u'TranslationDetectModel', {
    u'lang': fields.String
})

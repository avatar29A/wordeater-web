# coding=utf-8

from app import api
from flask.ext.restplus import fields
from utils.cerberus_utils import get_input_model_from_cerberus_schema


vocabularity_schema = {
    u'text': {'type': 'string', 'required': True, 'nullable': False, 'empty': False}
}

vocabularity_input_context_fields = get_input_model_from_cerberus_schema(vocabularity_schema, u'GroupInput')

vocabularity_context_fields = api.model(u'TranslationModel', {
    u'text': fields.String,
    u'context': fields.String
})

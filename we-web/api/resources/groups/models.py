# coding=utf-8

from app import api
from flask.ext.restplus import fields
from utils.cerberus_utils import get_input_model_from_cerberus_schema
from api.resources.cards.models import card_fields

group_schema = {
    u'name': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    u'description': {'type': 'string', 'required': False, 'nullable': True, 'empty': True}
}

group_input_fields = get_input_model_from_cerberus_schema(group_schema, u'GroupInput')

# Group
group_fields = api.model(u'GroupModel', {
    u'id': fields.String,
    u'name': fields.String,
    u'description': fields.String,
    u'cards_count': fields.Integer,
    u'cards_studying_count': fields.Integer
})

# Group with cards
group_fields_ext = api.model(u'GroupExtModel', {
    u'id': fields.String,
    u'name': fields.String,
    u'description': fields.String,
    u'cards_count': fields.Integer,
    u'cards_studying_count': fields.Integer,
    u'cards': fields.List(fields.Nested(card_fields))
})

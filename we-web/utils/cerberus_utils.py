# coding=utf-8
from cerberus import Validator
from flask import request, current_app
from flask.ext.restplus import fields
from flask.ext.restplus.utils import merge
from app import api

base_fields_mapping = {str: fields.String,
                       bool: fields.Boolean,
                       int: fields.Integer,
                       float: fields.Float
                       }

schema_fields_mapping = {'string': fields.String,
                         'boolean': fields.Boolean,
                         'integer': fields.Integer,
                         'float': fields.Float
                         }


def get_input_model_from_parser(parser, model_name, fields_mapping=base_fields_mapping):
    new_model = api.model(model_name, {arg.name: fields_mapping[arg.type] for arg in parser.args})
    return new_model


def get_field_type_from_schema(arg_name, schema, model_name, fields_mapping):
    if schema['type'] == 'dict':
        if 'schema' not in schema and 'anyof' in schema:
            return fields.Nested(get_input_model_from_cerberus_schema(schema['anyof'][0]['schema'],
                                                                      '{model_name}_{arg_name}'.format(
                                                                          model_name=model_name,
                                                                          arg_name=arg_name),
                                                                      fields_mapping))
        else:
            return fields.Nested(get_input_model_from_cerberus_schema(schema['schema'],
                                                                      '{model_name}_{arg_name}'.format(
                                                                          model_name=model_name,
                                                                          arg_name=arg_name),
                                                                      fields_mapping))
    if schema['type'] == 'list':
        return fields.List(get_field_type_from_schema(arg_name, schema['schema'], model_name, fields_mapping))
    else:
        return fields_mapping[schema['type']]


def get_input_model_from_cerberus_schema(schema, model_name, fields_mapping=schema_fields_mapping):
    model = {arg_name: get_field_type_from_schema(arg_name, arg_schema, model_name, fields_mapping)
             for arg_name, arg_schema in schema.items()}
    return api.model(model_name, model)


def validate_json(json, schema):
    v = Validator(schema)
    if json is None \
            or 'data' not in json \
            or not isinstance(json['data'], dict) \
            or not v.validate(json['data']):
        return False, v.errors
    return True, {}


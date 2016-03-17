# coding=utf-8

from flask.ext.restplus import Resource
from flask import request
from app import api
from utils.wordeater_api import ApiResponse
from cerberus import Validator

from config import API_PATH, ENVELOPE_DATA

from services.service_locator import ServiceLocator
from decorators.authenticate import expose
from models import vocabularity_schema, vocabularity_input_context_fields, vocabularity_context_fields

from errors import ServerErrors
from logger import error

__author__ = 'Glebov Boris'

translations_ns = api.namespace(name='Vocabularity', description="Requests related with pictures", path=API_PATH)


class VocubularityResource(Resource):
    def __init__(self, api, *args, **kwargs):
        Resource.__init__(self, api, *args, **kwargs)
        self.vs = ServiceLocator.resolve(ServiceLocator.VOCABULARITY)


@translations_ns.route('/vocubularity/context/', endpoint='context')
class VocubularityContextAPI(VocubularityResource):
    @expose
    @api.doc(body=vocabularity_input_context_fields)
    @api.marshal_with(vocabularity_context_fields, envelope=ENVELOPE_DATA, code=200)
    def post(self):
        """
        Translate text
        :return:
        """

        v = Validator(vocabularity_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        text = args.get(u'text')

        try:
            context = self.vs.get_context(text)

            return {
                u'text': text,
                u'context': context
            }
        except Exception as ex:
            error(u'PicturesRandomAPI.post(text={0})'.format(text), ex)

            return ApiResponse(status=500, errors=ServerErrors.internal_server_error([]))

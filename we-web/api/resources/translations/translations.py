# coding=utf-8

from flask.ext.restplus import Resource
from flask import request
from app import api
from utils.wordeater_api import ApiResponse
from cerberus import Validator

from config import API_PATH, ENVELOPE_DATA

from services.service_locator import ServiceLocator
from decorators.authenticate import expose
from models import translation_schema, translation_fields, translation_input_fields, translation_detect_fields

from logger import error

__author__ = 'Glebov Boris'

translations_ns = api.namespace(name='Translations', description="Requests related with translations", path=API_PATH)


class TranslationResource(Resource):
    def __init__(self, api, *args, **kwargs):
        Resource.__init__(self, api, *args, **kwargs)
        self.ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)
        self.ts = ServiceLocator.resolve(ServiceLocator.TRANSLATIONS)


@translations_ns.route('/translations/translate/', endpoint='translate')
class TranslationsTranslateAPI(TranslationResource):
    @expose
    @api.doc(body=translation_input_fields)
    @api.marshal_with(translation_fields, envelope=ENVELOPE_DATA, code=200)
    def post(self):
        """
        Translate text
        :return:
        """

        v = Validator(translation_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        text = args.get(u'text')
        user = self.ss.get_user()

        try:
            translation = self.ts.translate(text, user.direction)
            return translation
        except Exception as ex:
            error(u'TranslationsAPI.post(text={0}, dir={1})'.format(text, user.direction), ex)


@translations_ns.route('/translations/detect/', endpoint='detect')
class TranslationsDetectAPI(TranslationResource):
    @expose
    @api.doc(body=translation_input_fields)
    @api.marshal_with(translation_detect_fields, envelope=ENVELOPE_DATA, code=200)
    def post(self):
        """

        :return:
        """

        v = Validator(translation_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        text = args.get(u'text')
        lang = self.ts.detect(text)

        return {
            u'lang': lang
        }

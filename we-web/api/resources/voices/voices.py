# coding=utf-8

from flask.ext.restplus import Resource
from flask import request, Response
from app import api
from utils.wordeater_api import ApiResponse
from cerberus import Validator

from config import API_PATH, ENVELOPE_DATA

from services.service_locator import ServiceLocator
from decorators.authenticate import expose
from models import voice_fields, voice_input_fields, voice_schema

from errors import ServerErrors, VoicesErrors
from logger import error

__author__ = 'Glebov Boris'

voices_ns = api.namespace(name='Voices', description="Requests related with voices", path=API_PATH)


class VoiceResource(Resource):
    def __init__(self, api, *args, **kwargs):
        Resource.__init__(self, api, *args, **kwargs)
        self.ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)
        self.vs = ServiceLocator.resolve(ServiceLocator.VOICES)
        self.bs = ServiceLocator.resolve(ServiceLocator.BLUEMIX)


@voices_ns.route('/voices/', endpoint='voices')
class VoicesAPI(VoiceResource):
    @expose
    @api.doc(body=voice_input_fields)
    @api.marshal_with(voice_fields, envelope=ENVELOPE_DATA, code=200)
    def post(self):
        """
        Translate text
        :return:
        """

        v = Validator(voice_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        text = args.get(u'text')

        try:
            voice = self.vs.get(text)
            if voice:
                return voice

            return self.vs.add(text, self.bs.synthesize(text))
        except Exception as ex:
            error(u'PicturesRandomAPI.post(text={0})'.format(text), ex)

            return ApiResponse(status=500, errors=ServerErrors.internal_server_error([]))


@voices_ns.route('/voice/<string:text>/', endpoint='voice')
class VoiceAPI(VoiceResource):
    @expose
    def get(self, text):
        """
        Returns voice entity
        :param text:
        :return:
        """

        voice = self.vs.get(text)
        if voice is None:
            return ApiResponse(status=404, errors=VoicesErrors.picture_doesnt_exists(['text']))

        return Response(voice.fs.content, mimetype='audio/wav')

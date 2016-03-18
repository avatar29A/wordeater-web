# coding=utf-8

from flask.ext.restplus import Resource
from flask import request, Response
from app import api
from utils.wordeater_api import ApiResponse
from cerberus import Validator

from config import API_PATH, ENVELOPE_DATA

from services.service_locator import ServiceLocator
from decorators.authenticate import expose
from models import picture_schema, picture_input_fields, picture_fields

from errors import ServerErrors, PicturesErrors
from logger import error

__author__ = 'Glebov Boris'

translations_ns = api.namespace(name='Pictures', description="Requests related with pictures", path=API_PATH)


class PictureResource(Resource):
    def __init__(self, api, *args, **kwargs):
        Resource.__init__(self, api, *args, **kwargs)
        self.ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)
        self.ps = ServiceLocator.resolve(ServiceLocator.PICTURES)
        self.gs = ServiceLocator.resolve(ServiceLocator.GIPHY)


@translations_ns.route('/pictures/random/', endpoint='random')
class PicturesRandomAPI(PictureResource):
    @expose
    @api.doc(body=picture_input_fields)
    @api.marshal_with(picture_fields, envelope=ENVELOPE_DATA, code=200)
    def post(self):
        """
        Translate text
        :return:
        """

        v = Validator(picture_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        text = args.get(u'text')

        try:
            picture = self.ps.get(text)
            if picture:
                return picture

            return self.ps.add(text, self.gs.random(text))
        except Exception as ex:
            error(u'PicturesRandomAPI.post(text={0})'.format(text), ex)

            return ApiResponse(status=500, errors=ServerErrors.internal_server_error([]))


@translations_ns.route('/picture/<string:text>/', endpoint='picture')
class PictureAPI(PictureResource):
    @expose
    def get(self, text):
        """
        Returns picture entity
        :param picture_id:
        :return:
        """

        picture = self.ps.get(text)
        if picture is None:
            return ApiResponse(status=404, errors=PicturesErrors.picture_doesnt_exists(['text']))

        return Response(picture.fs.content, mimetype='image/gif')

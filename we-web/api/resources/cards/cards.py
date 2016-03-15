# coding=utf-8

from flask import request
from flask.ext.restplus import Resource
from utils.wordeater_api import ApiResponse
from app import api

from config import API_PATH, ENVELOPE_DATA
from cerberus import Validator

from services.service_locator import ServiceLocator
from models import card_list_fields, card_schema, card_input_fields
from decorators.authenticate import expose

from errors import ServerErrors

__author__ = 'Warlock'

cards_ns = api.namespace(name='Cards', description="Requests for page words", path=API_PATH)


@cards_ns.route('/cards/', endpoint='cards')
class CardsAPI(Resource):
    def __init__(self, api, *args, **kwargs):
        Resource.__init__(self, api, *args, **kwargs)
        self.ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)
        self.cs = ServiceLocator.resolve(ServiceLocator.CARDS)
        self.gs = ServiceLocator.resolve(ServiceLocator.GROUPS)

    @expose
    @api.marshal_with(card_list_fields, envelope=ENVELOPE_DATA, as_list=True)
    def get(self):
        u"""
        Get all user's cards
        :return:
        """

        user = self.ss.get_user()

        cards = self.cs.list(user)

        return cards

    @expose
    @api.doc(body=card_input_fields)
    @api.marshal_with(card_input_fields, envelope=ENVELOPE_DATA, code=201)
    def post(self):
        u"""
        Creates new card and adds it to group.
        :return: Card
        """

        v = Validator(card_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        foreign = args.get(u'foreign')
        native = args.get(u'native')
        transcription = args.get(u'transcription', u'')
        context = args.get(u'context', u'')
        image_url = args.get(u'image_url', u'')

        user = self.ss.get_user()
        group = self.gs.pick_up(user)

        card = self.cs.create(user, group, foreign, native, transcription, context, image_url)
        if card is None:
            return ApiResponse(status=500, errors=ServerErrors.internal_server_error([]))

        return card


@cards_ns.route('/card/<string:id>/')
class CardApi(Resource):
    def get(self):
        u"""

        :return:
        """

    def patch(self):
        u"""

        :return:
        """

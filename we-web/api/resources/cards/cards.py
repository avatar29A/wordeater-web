# coding=utf-8

from flask import request
from flask.ext.restplus import Resource
from utils.wordeater_api import ApiResponse
from app import api
from mongokit import ObjectId

from config import API_PATH, ENVELOPE_DATA
from cerberus import Validator

from services.service_locator import ServiceLocator
from models import card_list_fields, card_schema, card_fields, card_input_fields
from decorators.authenticate import expose

from errors import ServerErrors, CardsErrors
from logger import error

__author__ = 'Warlock'

cards_ns = api.namespace(name='Cards', description="Requests for page words", path=API_PATH)


class CardsResource(Resource):
    def __init__(self, api, *args, **kwargs):
        Resource.__init__(self, api, *args, **kwargs)
        self.ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)
        self.cs = ServiceLocator.resolve(ServiceLocator.CARDS)
        self.gs = ServiceLocator.resolve(ServiceLocator.GROUPS)


@cards_ns.route('/cards/', endpoint='cards')
class CardsAPI(CardsResource):
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

        exists_card = self.cs.exists(user, foreign, user.foreign_lng)
        if exists_card:
            return ApiResponse(status=409, errors=CardsErrors.card_already_exists(foreign, [u'foreign']))

        card = self.cs.create(user, group, foreign, native, transcription, context, image_url)
        if card is None:
            return ApiResponse(status=500, errors=ServerErrors.internal_server_error([]))

        return card


@cards_ns.route('/card/<string:card_id>/')
class CardApi(CardsResource):
    @expose
    @api.marshal_with(card_fields)
    def get(self, card_id):
        u"""
        Returns card entity by id
        :param card_id: card's id
        :return: card entity
        """

        user = self.ss.get_user()

        card = self.cs.get(user, ObjectId(card_id))
        if card is None:
            return ApiResponse(status=404, errors=CardsErrors.card_dont_exists([]))

        return card

    @expose
    @api.doc(body=card_input_fields)
    @api.marshal_with(card_input_fields, envelope=ENVELOPE_DATA, code=200)
    def put(self, card_id):
        u"""
        Update card entity
        :param card_id: card's id
        :return: updated card
        """

        v = Validator(card_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        user = self.ss.get_user()

        card = self.cs.get(user, ObjectId(card_id))
        if card is None:
            return ApiResponse(status=404, errors=CardsErrors.card_dont_exists([]))

        foreign = args.get(u'foreign')
        native = args.get(u'native')
        transcription = args.get(u'transcription', card.transcription)
        context = args.get(u'context', card.context)
        image_url = args.get(u'image_url', card.image_url)

        duplicate_card = self.cs.single(user, foreign, user.foreign_lng)
        if duplicate_card.id != card.id:
            return ApiResponse(status=409, errors=CardsErrors.card_already_exists(foreign, [u'foreign']))

        try:
            card.foreign = foreign
            card.native = native
            card.transcription = transcription
            card.context = context
            card.image_url = image_url

            card.save()
        except Exception as ex:
            error(u'CardApi.patch(card_id={0})'.format(card_id), ex)

            return ApiResponse(status=500, errors=ServerErrors.internal_server_error([]))

    def delete(self, card_id):
        """
        Remove card
        :param card_id: Card ID
        :return:
        """

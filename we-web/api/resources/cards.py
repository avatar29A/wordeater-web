# coding=utf-8
from flask.ext.restplus import Resource
from app import api
from config import API_PATH

from services.cards import CardService

__author__ = 'Warlock'

cards_ns = api.namespace(name='Cards', description="Requests for page words", path=API_PATH)

@cards_ns.route('/list/', endpoint='cards')
class CardsAPI(Resource):
    def get(self):
        u"""
        Get viewmodel for Words page
        :return:
        """

        return {
            'data': [{'id':'123', 'name': '12'}]
        }


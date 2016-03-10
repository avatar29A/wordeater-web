# coding=utf-8

from flask.ext.restplus import Resource
from app import api
from config import API_PATH
from decorators.authenticate import expose

__author__ = 'Warlock'

entities_ns = api.namespace(name='Entities', description="Requests for page groups", path=API_PATH)


@entities_ns.route('/entities/', endpoint='entities')
class EntityAPI(Resource):
    @expose
    def get(self):
        u"""
        Return groups by user.
        :return:
        """
        return {
            'data': '3434'
        }
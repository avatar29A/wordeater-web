# coding=utf-8

import json
import datetime

from flask.ext.restplus import Resource
from flask import session, request
from app import api
from config import API_PATH
from decorators.authenticate import expose
from logger import logger

__author__ = 'Glebov Boris'

groups_ns = api.namespace(name='Groups', description="Requests for page groups", path=API_PATH)


@groups_ns.route('/learn/groups/', endpoint='groups_for_learns')
class GroupsForLearnAPI(Resource):
    def get(self):
        u"""
        Return groups by user.
        :return:
        """

        return {
            'data': True
        }


@groups_ns.route('/learn/group/<group_id>/', endpoint='group_for_learn')
class GroupForLearnAPI(Resource):
    def get(self, group_id):

        return {
            'data': group_id
        }

    def post(self, group_id):
        """

        :param group_id:
        :return:
        """

        return {
            'data': True
        }


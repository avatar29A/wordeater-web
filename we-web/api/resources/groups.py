# coding=utf-8

import json
import datetime

from flask.ext.restplus import Resource
from flask import session, request
from app import api
from config import API_PATH
from decorators.authenticate import expose

from services.users import UserService
from services.groups import GroupService
from domain.model import db
from pydash import py_
from mongokit import ObjectId


# Mappers
from api.mapper.group_mapper import group_to_dict
from api.mapper.card_mapper import card_to_dict_for_learn

from logger import logger

__author__ = 'Glebov Boris'

groups_ns = api.namespace(name='Groups', description="Requests for page groups", path=API_PATH)


def get_user():
    us = UserService(db)

    current_user = session['user']
    user = us.get(current_user['login'])

    return user


@groups_ns.route('/learn/groups/', endpoint='groups_for_learns')
class GroupsForLearnAPI(Resource):
    def get(self):
        u"""
        Return groups by user.
        :return:
        """
        gs = GroupService(db)
        user = get_user()

        groups = gs.list(user)

        return {
            'data': py_(groups).map(group_to_dict).value()
        }


@groups_ns.route('/learn/group/<group_id>/', endpoint='group_for_learn')
class GroupForLearnAPI(Resource):
    def get(self, group_id):
        gs = GroupService(db)

        group = gs.get_one(group_id)
        if group is None:
            return {
                'data': {}
            }

        dto = group_to_dict(group)
        dto['cards'] = py_(group.cards).map(card_to_dict_for_learn).value()

        return {
            'data': dto
        }

    def post(self, group_id):
        """

        :param group_id:
        :return:
        """

        try:
            cards = json.loads(request.data)
            user = get_user()

            success = []

            for id in cards:
                card = db.Card.find_one({'_id': ObjectId(id)})
                if not card:
                    break

                card.is_studying = False
                card.save()

                self._add_to_training(user, card)
                success.append(id)
            return {
                'data': success
            }
        except Exception as ex:
            logger.error(ex.message)
            api.abort(500)


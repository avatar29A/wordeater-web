# coding=utf-8

import json
import datetime

from flask.ext.restplus import Resource
from flask import session, request
from app import api
from utils.wordeater_api import ApiResponse
from cerberus import Validator

from config import API_PATH, ENVELOPE_DATA

from services.service_locator import ServiceLocator
from decorators.authenticate import expose
from models import group_fields, group_fields_ext, group_schema, group_input_fields

from errors import ServerErrors, GroupsErrors
from logger import error

__author__ = 'Glebov Boris'

groups_ns = api.namespace(name='Groups', description="Requests for page groups", path=API_PATH)


class GroupResource(Resource):
    def __init__(self, api, *args, **kwargs):
        Resource.__init__(self, api, *args, **kwargs)
        self.ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)
        self.gs = ServiceLocator.resolve(ServiceLocator.GROUPS)
        self.cs = ServiceLocator.resolve(ServiceLocator.USERS)


@groups_ns.route('/groups/', endpoint='groups')
class GroupsAPI(GroupResource):
    @expose
    @api.marshal_with(group_fields, envelope=ENVELOPE_DATA, as_list=True)
    def get(self):
        u"""
        Return groups by user.
        :return:
        """

        user = self.ss.get_user()
        groups = self.gs.list(user)

        return groups

    @expose
    @api.doc(body=group_input_fields)
    @api.marshal_with(group_input_fields, envelope=ENVELOPE_DATA, code=201)
    def post(self):
        u"""
        Create new group
        :return:
        """

        v = Validator(group_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        name = args.get(u'name')
        description = args.get(u'description', u'')

        user = self.ss.get_user()
        duplicate_group = self.gs.single(user=user, name=name)
        if duplicate_group:
            return ApiResponse(status=409, errors=GroupsErrors.group_already_exists(name, [u'name']))

        group = self.gs.create(user, name, description)
        if group is None:
            return ApiResponse(status=500, errors=ServerErrors.internal_server_error([u'name']))

        return group


@groups_ns.route('/group/<group_id>/', endpoint='group')
class GroupAPI(GroupResource):
    @expose
    @api.marshal_with(group_fields_ext)
    def get(self, group_id):

        group = self.gs.single(group_id)
        if group is None:
            return ApiResponse(status=404, errors=GroupsErrors.group_dont_exists([]))

        return group

    @expose
    @api.doc(body=group_input_fields)
    @api.marshal_with(group_input_fields, envelope=ENVELOPE_DATA, code=200)
    def patch(self, group_id):
        """
        Update group
        :param group_id:
        :return:
        """

        v = Validator(group_schema)
        args = v.validated(request.get_json())

        if args is None:
            return ApiResponse(status=4001, errors=v.errors)

        group = self.gs.single(group_id)
        if group is None:
            return ApiResponse(status=404, errors=GroupsErrors.group_dont_exists([]))

        name = args.get(u'name')
        description = args.get(u'description', group.description)

        user = self.ss.get_user()
        duplicate_group = self.gs.single(user=user, name=name)
        if duplicate_group.id == group.id:
            return ApiResponse(status=409, errors=GroupsErrors.group_already_exists(name, [u'name']))

        try:
            group.name = name
            group.description = description

            return group
        except Exception as ex:
            error(u'GroupAPI.patch(group_id={0})'.format(group_id), ex)

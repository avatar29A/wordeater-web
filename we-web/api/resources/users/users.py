# coding=utf-8

from config import API_PATH
from decorators.authenticate import expose
from logger import logger
from flask.ext.restplus import Resource
from flask import session, request
from app import api


__author__ = 'Glebov Boris'

users_ns = api.namespace(name='Groups', description="Requests for page groups", path=API_PATH)


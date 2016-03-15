# coding=utf-8

import json
import unittest
from tests.dal.dal_test_base import db, BaseTest
from app import app
from services.service_locator import ServiceLocator

__author__ = 'Warlock'


class RestBaseTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

    def get_app_client(self):
        app.config['TESTING'] = True
        return app.test_client()

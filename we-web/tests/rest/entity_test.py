# coding=utf-8

import unittest
from tests.dal.dal_test_base import db, BaseTest
from domain.model import User
from app import app
import api.resources.entity

__author__ = 'Glebov Boris'


class EntityTest(BaseTest):
    def test_cards_all(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        r = self.app.get('/entities/')


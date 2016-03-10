# coding=utf-8

import json
import unittest
from tests.dal.dal_test_base import db, BaseTest

import api.resources.users.users
from app import app
from services.service_locator import ServiceLocator


__author__ = 'Glebov Boris'


class UserTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)

        self.headers = [('Content-Type', 'application/json')]

    def get_app_client(self):
        app.config['TESTING'] = True
        return app.test_client()

    def test_users_list_success(self):
        client_app = self.get_app_client()

        r = client_app.get('/api/v1/users/')
        data = json.loads(r.data)

        self.assertEqual(data[u'status'], 200)

    def test_users_sigin_fail(self):
        client_app = self.get_app_client()

        data = {
            u'login': u'123',
            u'password': u'123'
        }

        r = client_app.post('/api/v1/user/signin/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        self.assertEqual(4001, response_data[u'status'])

    def test_users_sigin_ok(self):
        us = ServiceLocator.resolve(ServiceLocator.USERS)
        us.create(u'user1', u'user1@example.com', u'123', first_name=u'demo', last_name=u'demo')

        client_app = self.get_app_client()

        data = {
            u'login': u'user1',
            u'password': u'123'
        }

        r = client_app.post('/api/v1/user/signin/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertIsNotNone(response_data[u'data'][u'auth_token'])

    def test_users_signup_fail(self):
        pass

    def test_users_signup_ok(self):
        pass

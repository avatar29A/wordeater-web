# coding=utf-8

from rest_test import *
import api.resources.cards.cards

__author__ = 'Warlock'


class CardsGetTest(RestBaseTest):
    """
    Test all cases for method GET: /cards/
    """

    def test_get_empty(self):
        """
        Cards collection is empty
        :return: empty list
        """
        self.clear_db()
        self.create_demo_session()

        response_data = self._get()

        self.assertEqual(200, response_data[u'status'])
        self.assertEqual(response_data[u'data'], [])

    def test_get_one_card(self):
        self.clear_db()
        self.create_demo_session()

        us = ServiceLocator.resolve(ServiceLocator.USERS)
        gs = ServiceLocator.resolve(ServiceLocator.GROUPS)
        cs = ServiceLocator.resolve(ServiceLocator.CARDS)

        user = us.single(u'user1')
        group = gs.pick_up(user)
        cs.create(user, group, u'god', u'собака')

        response_data = self._get()

        self.assertEqual(200, response_data[u'status'])
        self.assertEqual(len(response_data[u'data']), 1)

    def _get(self):

        client_app = self.get_app_client()

        r = client_app.get('/api/v1/cards/')
        response_data = json.loads(r.data)

        return response_data


class CardsPostTest(RestBaseTest):
    """
    Test all cases for method POST: /cards/
    """

    def test_post_validation_fail(self):
        self.clear_db()
        self.create_demo_session()

        result_data = self._post({})

        self.assertEqual(result_data[u'status'], 4001)

    def test_create_new_card(self):
        self.clear_db()
        self.create_demo_session()

        data = {
            u'foreign': u'dog',
            u'native': u'собака',
            u'context': u"dog it's human pet",
            u'transcription': u'',
        }

        result_data = self._post(data)

        self.assertEqual(result_data[u'status'], 201)
        self.assertEqual(result_data[u'data'][u'foreign'], data[u'foreign'])
        self.assertEqual(result_data[u'data'][u'native'], data[u'native'])

    def _post(self, data):
        client_app = self.get_app_client()

        r = client_app.post('/api/v1/cards/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data
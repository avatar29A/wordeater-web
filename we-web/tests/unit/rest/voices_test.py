# coding=utf-8

from rest_test import *
import api.resources.voices.voices

__author__ = 'Glebov Boris'


class VoicesAPI(RestBaseTest):
    """
    Test all cases for method /voices/
    """

    def test_post(self):
        """
        1. Create session
        2. Send request on voice by 'dog' word.
        3. Expected 200
        """

        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        data = {
            u'text': u'dog'
        }

        response_data = self._post(data)

        # Step 3
        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'text'], u'dog')

    def test_get_doesnt_exists(self):
        """
        1. Create session
        2. Send get
        3. Expected 404
        :return:
        """
        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 3
        response_data = self._get(u'dog')
        j = json.loads(response_data)
        self.assertEqual(j[u'status'], 404)
        self.assertEqual(j[u'errors'][u'error_type'], u'voice_doesnt_exists')

    def test_get(self):
        """
        1. Create session
        2. Send post
        3. Send get
        4. Check result
        :return:
        """
        # Step 1
        self.clear_db()
        self.create_demo_session()

        # Step 2
        data = {
            u'text': u'dog'
        }

        response_data = self._post(data)
        self.assertEqual(response_data[u'status'], 200)

        # Step 3
        response_data = self._get(u'dog')
        self.assertEqual(response_data, 'wave')

    def _get(self, text):
        client_app = self.get_app_client()
        r = client_app.get('/api/v1/voice/' + text + '/')
        return r.data

    def _post(self, data):
        client_app = self.get_app_client()
        r = client_app.post('/api/v1/voices/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data

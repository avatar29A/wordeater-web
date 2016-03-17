# coding=utf-8

from rest_test import *
import api.resources.translations.translations
from mongokit import ObjectId

__author__ = 'Glebov Boris'


class TranslationsTranslateAPI(RestBaseTest):
    """
    Test all cases for method POST: /translations/
    """

    def test_post(self):
        """
        1. Create session
        2. Send request on translate 'dog' word.
        3. Expected 200 and u'собака'
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
        self.assertEqual(response_data[u'data'][u'variations'][0], u'собака')

    def _post(self, data):
        client_app = self.get_app_client()
        r = client_app.post('/api/v1/translations/translate/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data


class TranslationsDetectAPI(RestBaseTest):
    """
    Test all cases for method POST: /translation/
    """
    def test_detect_en_lang(self):
        """
        1. Send request u'Hello world!'
        2. Expected lang=='en'
        """

        # Step 1
        data = {
            u'text': u'Hello world!'
        }

        response_data = self._post(data)

        self.assertEqual(response_data[u'status'], 200)
        self.assertEqual(response_data[u'data'][u'lang'], u'en')

    def _post(self, data):
        client_app = self.get_app_client()
        r = client_app.post('/api/v1/translations/detect/', headers=self.headers, data=json.dumps(data))
        response_data = json.loads(r.data)

        return response_data
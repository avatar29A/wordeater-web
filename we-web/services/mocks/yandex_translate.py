# coding=utf-8

import json


class YandexTranslateFake(object):
    def translate(self, text, direction):
        response =u'{"lang": "en-ru", "text": ["собака"], "code": 200}'

        return json.loads(response)

    def detect(self, text):
        return u'en'
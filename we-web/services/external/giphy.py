# coding=utf-8

import safygiphy
import requests

from services.base import BaseService

__author__ = 'Glebov Boris'


class GiphyService(BaseService):
    def __init__(self):
        self.engine = safygiphy.Giphy()

        BaseService.__init__(self)

    def random(self, text):
        """
        Get random gif image by tag, if word doesn't exists in DB
        :param text: text
        """
        response = self.engine.random(tag=text)
        if response and response[u'meta'][u'status'] == 200:
            data = response[u'data']
            response = requests.get(data[u'fixed_width_small_url'])

            if response.status_code == 200:
                return response.content
            else:
                return None
        else:
            return None

# coding=utf-8

import safygiphy

from services.base import BaseService
from services.service_locator import ServiceLocator
from logger import error
from services.exceptions import PictureLoadError

__author__ = 'Glebov Boris'


class PictureService(BaseService):
    def __init__(self):
        self.engine = safygiphy.Giphy()

        BaseService.__init__(self)

    def random(self, text):
        """
        Get random gif image by tag, if word doesn't exists in DB
        :param word: word
        :return:
        """
        picture = self.get(text)
        if picture:
            return picture

        response = self.engine.random(tag=text)
        if response and response[u'meta'][u'status'] == 200:
            return self.add(text, response)

        raise PictureLoadError(response)

    def get(self, text):
        """
        Try to find translation in DB
        :param text: sentence to translate.
        :param direction: Direction for translate. For example en-ru.

        :return: translated text
        """

        return self.db.Picture.find_one({'text': text})

    def add(self, text, response):
        """
        Add to collection new picture
        :param text: text for search
        :param response: response from giphy
        :return: Picture entity
        """

        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)
        data = response[u'data']

        picture = self.db.Picture()
        picture.text = text

        picture.mp4 = data[u'image_mp4_url']
        picture.url = data[u'url']
        picture.original = data[u'image_original_url']
        picture.original_small = data[u'fixed_width_small_url']

        picture.author = ss.get().login

        try:
            picture.validate()
            picture.save()

            return picture
        except Exception as ex:
            error(u'Pictures.add', ex)
            return None

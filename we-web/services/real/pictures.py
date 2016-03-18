# coding=utf-8

import safygiphy

from services.base import BaseService
from services.service_locator import ServiceLocator
from logger import error

__author__ = 'Glebov Boris'


class PictureService(BaseService):
    def __init__(self):
        self.engine = safygiphy.Giphy()

        BaseService.__init__(self)

    def get(self, text):
        """
        Try to find translation in DB
        :param text: sentence to translate.
        :param direction: Direction for translate. For example en-ru.

        :return: translated text
        """

        return self.db.Picture.find_one({'text': text})

    def add(self, text, file):
        """
        Add to collection new picture
        :param text: text for search
        :param file: gif image
        :return: Picture entity
        """

        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        picture = self.db.Picture()
        picture.text = text

        picture.author = ss.get().login

        try:
            picture.validate()
            picture.save()

            # Сохраняем картинку:
            picture.fs.text = text
            picture.fs.source = file

            return picture
        except Exception as ex:
            error(u'Pictures.add', ex)
            return None

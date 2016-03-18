# coding=utf-8

from services.base import BaseService
from services.service_locator import ServiceLocator
from mongokit import ObjectId
from logger import error

__author__ = 'Glebov Boris'


class PictureService(BaseService):
    def __init__(self):
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

        # check what text is doesn't exists, else to return  the found entity
        duplicate = self.get(text)
        if duplicate:
            return duplicate

        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        picture = self.db.Picture()
        picture.text = text

        picture.author = ss.get().login

        try:
            picture.validate()
            picture.save()

            # Сохраняем картинку:
            picture.fs.content = file

            return picture
        except Exception as ex:
            error(u'Pictures.add', ex)
            return None

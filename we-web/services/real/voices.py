# coding=utf-8

from services.base import BaseService
from services.service_locator import ServiceLocator
from logger import error

__author__ = 'Glebov Boris'


class VoicesService(BaseService):
    def __init__(self):
        BaseService.__init__(self)

    def get(self, text):
        """
        Try to find voice in DB
        :param text: sentence to find voice.
        :return: voice entity
        """

        return self.db.Voice.find_one({'text': text})

    def add(self, text, file):
        """
        Add to collection new voice
        :param text: text for search
        :param file: gif image
        :return: Picture entity
        """

        # Не соханяем запись без контента:
        if file is None:
            return None

        # check what text is doesn't exists, else to return  the found entity
        duplicate = self.get(text)
        if duplicate:
            return duplicate

        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        voice = self.db.Voice()
        voice.text = text

        voice.author = ss.get().login

        try:
            voice.validate()
            voice.save()

            # Сохраняем картинку:
            voice.fs.content = file

            return voice
        except Exception as ex:
            error(u'Voice.add', ex)
            return None

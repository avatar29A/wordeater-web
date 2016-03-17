# coding=utf-8

import config

from services.base import BaseService
from services.service_locator import ServiceLocator
from yandex_translate import YandexTranslate
from services.exceptions import TranslateError
from logger import error

__author__ = 'Glebov Boris'


class TranslateService(BaseService):
    #
    # Public methods
    def __init__(self):
        self.engine = YandexTranslate(config.TRANSLATE_YANDEX_KEY)

        BaseService.__init__(self)

    def translate(self, text, direction):
        """
        Translate text from foreign language on native.

        This method tries to find translated word in own DB and if translate doesn't exists,
        it sends request to external service
        :param text: sentence to translate.
        :param direction: Direction for translate. For example en-ru.

        :return: translated text
        """

        translation = self.get(text, direction)
        if translation:
            return translation

        response = self.engine.translate(text, direction)
        if response and response[u'code'] == 200:
            return self.add(text, response)

        raise TranslateError(response)

    def get(self, text, direction):
        """
        Try to find translation in DB
        :param text: sentence to translate.
        :param direction: Direction for translate. For example en-ru.

        :return: translated text
        """

        return self.db.Translation.find_one({'text': text, 'direction': direction})

    def add(self, text, translation):
        """
        Add to collection new translation
        :param text: sentence to translate.
        :param translation: response from translate.yandex.ru

        :return: translated text
        """
        ss = ServiceLocator.resolve(ServiceLocator.SESSIONS)

        translation_entity = self.db.Translation()

        translation_entity.direction = translation[u'lang']
        translation_entity.text = text
        translation_entity.variations = translation[u'text']
        translation_entity.author = ss.get().login

        try:
            translation_entity.validate()
            translation_entity.save()

            return translation_entity
        except Exception as ex:
            error(u'Translate.add', ex)
            return None

    def detect(self, text):
        """
        Detect language
        :param text: text for which needs to detect language
        :return: language
        """

        return self.engine.detect(text)

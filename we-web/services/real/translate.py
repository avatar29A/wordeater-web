# coding=utf-8

import config

from services.base import BaseService
from services.service_locator import ServiceLocator
from utils.session_manager import UserSession
from flask import session

__author__ = 'Glebov Boris'


class TranslateService(BaseService):
    #
    # Public methods

    def translate(self, text, foreign, native):
        """
        Translate text from foreign language on native.

        This method tries to find translated word in own DB and if translate doesn't exists,
        it sends request to external service
        :param text: sentence to translate.
        :param foreign: foreign language
        :param native: native language

        :return: translated text
        """

    def get(self, text, foreign, native):
        """
        Try to find translation in DB
        :param text: sentence to translate.
        :param foreign: foreign language
        :param native: native language

        :return: translated text
        """

        return self.db.Translation.find_one({'text': text, 'foreign': foreign, 'native': native})

# coding=utf-8

import json
from services.base import BaseService
from vocabulary import Vocabulary as vb

from logger import error

__author__ = 'Glebov Boris'


class VocabularityService(BaseService):
    @staticmethod
    def get_context(text):
        """
        Try to get context for card
        :param card:
        """

        try:
            m = json.loads(vb.usage_example(text))
            if len(m) > 0:
                return m[0]['text']
            return u''
        except Exception as ex:
            error(u'', ex)
            return u''

    @staticmethod
    def get_meaning(text, lang):
        """
        Try to get meaning for card
        :param text:
        :param lang:
        :return:
        """
        try:
            m = json.loads(vb.meaning(text, lang, lang))
            if len(m) > 0:
                return m[0]['text']
            return u''
        except Exception as ex:
            error(u'', ex)
            return u''

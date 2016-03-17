# coding=utf-8

from services.base import BaseService


__author__ = 'Glebov Boris'


class VocabularityService(BaseService):
    @staticmethod
    def get_context(text):
        """
        Try to get context for card
        :param card:
        """

        return u'Mock context'

    @staticmethod
    def get_meaning(text, lang):
        """
        Try to get meaning for card
        :param text:
        :param lang:
        :return:
        """

        return u'Mock meaning'

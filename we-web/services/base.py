# coding=utf-8
__author__ = 'Warlock'

from service_locator import ServiceLocator


class BaseService(object):
    @property
    def db(self):
        return ServiceLocator.resolve(ServiceLocator.DB)

    def _set_native(self, user, document):
        document.set_lang(user.native_lng)

    def _set_foreign(self, user, document):
        document.set_lang(user.foreign_lng)
# coding=utf-8
__author__ = 'Warlock'

from service_locator import ServiceLocator


class BaseService(object):
    @property
    def db(self):
        return ServiceLocator.resolve(ServiceLocator.DB)
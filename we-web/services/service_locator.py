# coding=utf-8
__author__ = 'Warlock'


class ServiceLocator(object):
    USERS = "users"
    GROUPS = "groups"
    CARDS = "cards"
    LOGIN_AUDIT = "login_audit"
    DB = "db"

    __service_factory = {}

    @staticmethod
    def register(service_name, service_instance):
        ServiceLocator.__service_factory[service_name] = service_instance

        return service_instance

    @staticmethod
    def resolve(service_name):
        return ServiceLocator.__service_factory[service_name]

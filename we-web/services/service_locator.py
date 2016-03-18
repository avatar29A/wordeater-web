# coding=utf-8
__author__ = 'Warlock'


class ServiceLocator(object):
    SESSIONS = "sessions"
    USERS = "users"
    GROUPS = "groups"
    CARDS = "cards"
    SCHEDULES = "schedules"
    LOGIN_AUDIT = "login_audit"
    TRANSLATIONS = "translations"
    PICTURES = "pictures"
    VOICES = "voices"
    VOCABULARITY = "vocabularity"

    DB = "db"

    # External
    BLUEMIX = "bluemix"
    GIPHY = "giphy"

    __service_factory = {}

    @staticmethod
    def register(service_name, service_instance):
        ServiceLocator.__service_factory[service_name] = service_instance

        return service_instance

    @staticmethod
    def resolve(service_name):
        return ServiceLocator.__service_factory[service_name]

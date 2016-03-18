# -*- coding: utf-8 -*-
import json

__author__ = 'Glebov Boris'


def _prepare_response(convert_to_json, response):
    if convert_to_json:
        return json.dumps(response)

    return response


def create_template_error():
    """
    Создает заготовку для генерации ошибок
    """
    return {'response': False}


class CommonErrors:

    @staticmethod
    def required_fields_is_empty(fields):
        """
        Пользователь не заполнил все обязательные поля
        """

        return {
            'error_type': u'required_fields_is_empty_error',
            'error_msg': u'Заполните все обязательные поля',
            'fields': fields
        }

    @staticmethod
    def entity_already_exists(message, fields):
        """
        Entity is exists error information
        :param fields:
        :return:
        """

        return {
            'error_type': u'entity_already_exists',
            'error_msg': message,
            'fields': fields
        }


class CardsErrors:
    @staticmethod
    def card_already_exists(foreign, fields):
        """
        Card is exists error information
        :param fields:
        :return:
        """

        return {
            'error_type': u'card_already_exists',
            'error_msg': u"Карточка со словом '{0}' уже существует в вашей библиотеки".format(foreign),
            'fields': fields
        }

    @staticmethod
    def card_dont_exists(fields):
        """
        Cards don't exists
        :param fields:
        :return:
        """

        return {
            'error_type': u'card_dont_exists',
            'error_msg': u'Запрошенная карточка не найдена. Возможно она была удалена.',
            'fields': fields
        }


class GroupsErrors:
    @staticmethod
    def group_already_exists(name, fields):
        """
        Card is exists error information
        :param fields:
        :return:
        """

        return {
            'error_type': u'group_already_exists',
            'error_msg': u"Группа с именем '{0}' уже существует".format(name),
            'fields': fields
        }

    @staticmethod
    def group_doesnt_exists(fields):
        """
        Cards don't exists
        :param fields:
        :return:
        """

        return {
            'error_type': u'group_doesnt_exists',
            'error_msg': u'Запрошенная группа не найдена, возможно она была удалена.',
            'fields': fields
        }


class PicturesErrors:
    @staticmethod
    def picture_doesnt_exists(fields):
        return {
            'error_type': u'picture_doesnt_exists',
            'error_msg': u"Picture doesn't exists",
            'fields': fields
        }


class VoicesErrors:
    @staticmethod
    def picture_doesnt_exists(fields):
        return {
            'error_type': u'voice_doesnt_exists',
            'error_msg': u"Voice doesn't exists",
            'fields': fields
        }


class SignErrors:
    """
    Ошибки регистрации и входа в систему
    """

    @staticmethod
    def login_or_password_wrong(fields):
        """
        Ответ на ошибку при неверно введенем логине и пароле
        """

        return {'error_type': u'login_or_password_wrong_error',
                'error_msg': u'Неправильный логин или пароль',
                'fields': fields}

    @staticmethod
    def password_wrong(fields):
        """
        Ответ на ошибку не верный пароль
        """

        return {'error_type': u'password_wrong_error',
                             'error_msg': u'Неправильный пароль',
                             'fields': fields}

    @staticmethod
    def password_does_not_match(fields):
        """
        Ответ на ошибку пароль не совпадает
        """

        return {
            'error_type': u'password_does_not_match_error',
            'error_msg': u'Пароли не совпадают',
            'fields': fields
        }

    @staticmethod
    def account_not_activated(fields):
        """
        Аккаунт пользователя не активирован
        """

        return {
            'error_type': u'account_not_activated',
            'error_msg': u'Ваш аккаунт не активирован',
            'fields': fields
        }

    @staticmethod
    def user_already_exists(fields):
        """
        User is already exists
        """

        return {
            'error_type': u'user_already_exists_error',
            'error_msg': u'User is already exists',
            'fields': fields
        }

    @staticmethod
    def email_already_exists(fields):
        """
        User with same email is already exists
        :param fields:
        :return:
        """

        return {
            'error_type': u'email_already_exists',
            'error_msg': u'Пользователь с такой эл. почтой уже зарегистрирован',
            'fields': fields
        }

    @staticmethod
    def login_already_exists(fields):
        """
        User with same login is already exists
        :return:
        """

        return {
            'error_type': u'user_already_exists_error',
            'error_msg': u'Пользователь с такой логином уже зарегистрирован',
            'fields': fields
        }

    @staticmethod
    def required_fields_is_empty(fields):
        """
        Пользователь не заполнил все обязательные поля
        """

        return {
            'error_type': u'required_fields_is_empty_error',
            'error_msg': u'Заполните все обязательные поля',
            'fields': fields
        }

    @staticmethod
    def incorrect_email(fields):
        """
        Некорректный email.
        """

        return {
            'error_type': u'incorect_email_error',
            'error_msg': u'Введите корректный адрес',
            'fields': fields
        }

    @staticmethod
    def access_denided(fields):
        """
        Не хватает прав доступа.
        """

        return {
            'error_type': u'access_denided',
            'error_msg': u'Access denided',
            'fields': fields
        }


class ServerErrors:
    """
    Inner server error
    """

    @staticmethod
    def internal_server_error(fields):
        """
        Creates response for inner server error
        """
        return {
            'error_type': u'internal_server_error',
            'error_msg': u'На сервере произошла ошибка',
            'fields': fields
        }

    @staticmethod
    def database_server_error(fields):
        """
        Creates response for errors with database
        """
        return {
            'error_type': u'database_server_error',
            'error_msg': u'База данных не доступна',
            'fields': fields
        }

    @staticmethod
    def abandon_user_session(fields):
        """
        User session is abandon
        """

        return {
            'error_type': u'abandon_user_session',
            'error_msg': u'Сессия пользователя истекла',
            'fields': fields
        }

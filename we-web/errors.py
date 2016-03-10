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
            'error_type': u'user_already_exists_error',
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

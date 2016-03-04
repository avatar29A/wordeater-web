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
    def required_fields_is_empty(fields, as_json=True):
        """
        Пользователь не заполнил все обязательные поля
        """

        response = create_template_error()

        response['error'] = {
            'error_type': u'required_fields_is_empty_error',
            'error_msg': u'Заполните все обязательные поля',
            'fields': fields
        }

        return _prepare_response(as_json, response)


class SignErrors:
    """
    Ошибки регистрации и входа в систему
    """

    @staticmethod
    def login_or_password_wrong(fields, as_json=False):
        """
        Ответ на ошибку при неверно введенем логине и пароле
        """
        response = create_template_error()
        response['error'] = {'error_type': u'login_or_password_wrong_error',
                             'error_msg': u'Неправильный логин или пароль',
                             'fields': fields}

        return _prepare_response(as_json, response)

    @staticmethod
    def password_wrong(fields, as_json=True):
        """
        Ответ на ошибку не верный пароль
        """
        response = create_template_error()
        response['error'] = {'error_type': u'password_wrong_error',
                             'error_msg': u'Неправильный пароль',
                             'fields': fields}

        return _prepare_response(as_json, response)

    @staticmethod
    def password_does_not_match(fields, as_json=True):
        """
        Ответ на ошибку пароль не совпадает
        """
        response = create_template_error()

        response['error'] = {
            'error_type': u'password_does_not_match_error',
            'error_msg': u'Пароли не совпадают',
            'fields': fields
        }

        return _prepare_response(as_json, response)

    @staticmethod
    def account_not_activated(fields, as_json=True):
        """
        Аккаунт пользователя не активирован
        """
        response = create_template_error()

        response['error'] = {
            'error_type': u'account_not_activated',
            'error_msg': u'Ваш аккаунт не активирован',
            'fields': fields
        }

        return _prepare_response(as_json, response)

    @staticmethod
    def user_already_exists(fields, as_json=True):
        """
        Пользователь с таким email уже существует
        """

        response = create_template_error()

        response['error'] = {
            'error_type': u'user_already_exists_error',
            'error_msg': u'Пользователь с такой эл. почтой уже зарегистрирован',
            'fields': fields
        }

        return _prepare_response(as_json, response)

    @staticmethod
    def required_fields_is_empty(fields, as_json=True):
        """
        Пользователь не заполнил все обязательные поля
        """

        response = create_template_error()

        response['error'] = {
            'error_type': u'required_fields_is_empty_error',
            'error_msg': u'Заполните все обязательные поля',
            'fields': fields
        }

        return _prepare_response(as_json, response)

    @staticmethod
    def incorrect_email(fields, as_json=True):
        """
        Некорректный email.
        """

        response = create_template_error()

        response['error'] = {
            'error_type': u'incorect_email_error',
            'error_msg': u'Введите корректный адрес',
            'fields': fields
        }

        return _prepare_response(as_json, response)

    @staticmethod
    def access_denided(fields, as_json=True):
        """
        Не хватает прав доступа.
        """

        response = create_template_error()

        response['error'] = {
            'error_type': u'incorect_email_error',
            'error_msg': u'Доступ запрещен',
            'fields': fields
        }

        return _prepare_response(as_json, response)


class ServerErrors:
    """
    Inner server error
    """

    @staticmethod
    def internal_server_error(fields, as_json=True):
        """
        Creates response for inner server error
        """
        resposne = create_template_error()

        resposne['error'] = {
            'error_type': u'internal_server_error',
            'error_msg': u'На сервере произошла ошибка',
            'fields': fields
        }

        return _prepare_response(as_json, resposne)

    @staticmethod
    def database_server_error(fields, as_json=True):
        """
        Creates response for errors with database
        """
        response = create_template_error()

        response['error'] = {
            'error_type': u'database_server_error',
            'error_msg': u'База данных не доступна',
            'fields': fields
        }

        return _prepare_response(as_json, response)

    @staticmethod
    def abandon_user_session(fields, as_json=True):
        """
        User session is abandon
        """

        response = create_template_error()

        response['error'] = {
            'error_type': u'abandon_user_session',
            'error_msg': u'Сессия пользователя истекла',
            'fields': fields
        }

        return _prepare_response(as_json, response)
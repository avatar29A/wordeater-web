# coding=utf-8
from flask.ext.restful import unpack
from flask.ext.restplus.utils import merge
from flask_restplus import Api
from flask.ext import restful
from functools import wraps

__author__ = 'Glebov Boris'


class ApiResponse(dict):
    pass


class WordeaterApi(Api):
    def marshal_with(self, fields, as_list=False, code=200, description=None, envelope=None, **kwargs_outer):
        """
        Декоратор для форматирования вывода

        :param as_list: Являются ли данные списком (для документации)
        :type as_list: bool
        :param code: Код http ответа по-умолчанию (также искользуется как статус по-умолчанию)
        :type code: integer
        """

        def wrapper(f):
            # документация для swagger
            doc = {
                'responses': {
                    code: (description, [fields]) if as_list else (description, fields)
                }
            }
            f.__apidoc__ = merge(getattr(f, '__apidoc__', {}), doc)

            @wraps(f)
            def inner_wrapper(*args, **kwargs):
                response = ApiResponse(status=code, message='', data=[], errors=[], code=None)

                resp = f(*args, **kwargs)
                # для обратной совместимости
                if isinstance(resp, tuple):
                    resp, response['code'], headers = unpack(resp)

                # предпочитаемый формат
                if isinstance(resp, ApiResponse):
                    response.update(resp)
                # если все значения по умолчанию и передаём только данные
                else:
                    response['data'] = resp

                response['data'] = restful.marshal(response['data'], fields)

                return response

            return inner_wrapper

        return wrapper
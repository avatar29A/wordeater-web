# -*- coding: utf-8 -*-
__author__ = 'Yakov Zubarev'


def validate_user_login(field, value, error):
    user_count = 0
    if user_count:
        error(field, "Пользователь с таким логином уже существует")
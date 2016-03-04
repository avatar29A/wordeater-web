# -*- coding: utf-8 -*-
__author__ = 'Glebov Boris'


def u(unicode_str):
    return unicode_str.encode('utf-8')


def from_1251(cp1251_str):
    return cp1251_str.decode('cp1251').encode('utf8')

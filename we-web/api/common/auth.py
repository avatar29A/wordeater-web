# coding=utf-8

__author__ = 'Glebov Boris'


def add_cors_header(response):
    if response.headers.get('Access-Control-Allow-Origin', None) is None:
        response.headers.add('Access-Control-Allow-Origin', '*')
    if response.headers.get('Access-Control-Allow-Methods', None) is None:
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,PUT,DELETE,OPTIONS')
    if response.headers.get('Access-Control-Allow-Headers', None) is None:
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Auth-Token')
    return response

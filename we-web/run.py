# coding=utf-8
__author__ = 'Warlock'

from app import app
import api.resources.groups

if __name__ == '__main__':
    app_options = {'debug': True, 'host': '0.0.0.0', 'port': 5050}
    app.run(**app_options)
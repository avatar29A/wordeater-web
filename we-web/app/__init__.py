# coding=utf-8
__author__ = 'Warlock'

import config

from flask import Flask, render_template, redirect
from utils.memcached_session import Session
from werkzeug.contrib.cache import MemcachedCache

from utils.wordeater_api import WordeaterApi
from flask.ext.restplus import apidoc

from services.service_locator import ServiceLocator
from services.real import cards, users

app = Flask(__name__)
#app.cache = MemcachedCache([config.MEMCACHED['host'], config.MEMCACHED['port']], 0)
#app.session_interface = Session()
app.secret_key = config.SECRET_KEY

# REGISTER SERVICES IN ServiceLocator
ServiceLocator.register(ServiceLocator.USERS, users.UserService())


@app.route('/')
def index():
    return redirect('/api/')


@app.route('/api/', endpoint='api')
def swagger_ui():
    return apidoc.ui_for(api)

api = WordeaterApi(app, version='1', title='', ui=False)



@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
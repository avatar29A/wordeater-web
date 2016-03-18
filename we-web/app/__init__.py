# coding=utf-8
import config

from flask import Flask, redirect
from utils.memcached_session import Session
from werkzeug.contrib.cache import MemcachedCache

from utils.wordeater_api import WordeaterApi
from flask.ext.restplus import apidoc

from domain.model import db

from services.service_locator import ServiceLocator
from services.real import cards, users, groups, session, translate, pictures, vocabularity
from services.external import bluemix, giphy

from api.common.auth import add_cors_header

__author__ = 'Glebov Boris'

app = Flask(__name__)
#app.cache = MemcachedCache([config.MEMCACHED['host'], config.MEMCACHED['port']], 0)
#app.session_interface = Session()
app.secret_key = config.SECRET_KEY

# добавление заголовков для CORS
app.after_request(add_cors_header)

# REGISTER SERVICES IN ServiceLocator

ServiceLocator.register(ServiceLocator.USERS, users.UserService())
ServiceLocator.register(ServiceLocator.CARDS, cards.CardService())
ServiceLocator.register(ServiceLocator.GROUPS, groups.GroupService())
ServiceLocator.register(ServiceLocator.SESSIONS, session.SessionService())
ServiceLocator.register(ServiceLocator.TRANSLATIONS, translate.TranslateService())
ServiceLocator.register(ServiceLocator.PICTURES, pictures.PictureService())
ServiceLocator.register(ServiceLocator.VOCABULARITY, vocabularity.VocabularityService())
ServiceLocator.register(ServiceLocator.DB, db)

# External

ServiceLocator.register(ServiceLocator.GIPHY, giphy.GiphyService())
ServiceLocator.register(ServiceLocator.BLUEMIX, bluemix.BluemixService())


@app.route('/')
def index():
    return redirect('/api/')


@app.route('/api/', endpoint='api')
def swagger_ui():
    return apidoc.ui_for(api)

api = WordeaterApi(app, version='1', title='', ui=False)

# coding=utf-8
__author__ = 'Warlock'

import config

from flask import Flask, render_template
from utils.memcached_session import Session
from werkzeug.contrib.cache import MemcachedCache

from utils.wordeater_api import WordeaterApi
from flask.ext.restplus import apidoc
from app.bundle import bundle

from modules import dashboard, training, words, about

app = Flask(__name__)
#app.cache = MemcachedCache([config.MEMCACHED['host'], config.MEMCACHED['port']], 0)
#app.session_interface = Session()
app.secret_key = config.SECRET_KEY

app.register_blueprint(dashboard.blueprint)
app.register_blueprint(training.blueprint)
app.register_blueprint(words.blueprint)
app.register_blueprint(about.blueprint)

bundle(app)

@app.route('/api/', endpoint='api')
def swagger_ui():
    return apidoc.ui_for(api)

api = WordeaterApi(app, version='1', title='', ui=False)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
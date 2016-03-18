# coding=utf-8
__author__ = 'Warlock'

from app import app

# API Resources

import api.resources.users.users
import api.resources.groups.groups
import api.resources.cards.cards
import api.resources.translations.translations
import api.resources.pictures.pictures
import api.resources.voices.voices
import api.resources.vocabularity.vocabularity

if __name__ == '__main__':
    app_options = {'debug': True, 'host': '0.0.0.0', 'port': 5050}
    app.run(**app_options)

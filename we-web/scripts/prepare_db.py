# coding=utf-8
__author__ = 'Warlock'

from flask.ext.script import Command
from services.users import UserService
from domain.model import db


class CreatDatabase(Command):
    def run(self):
        pass

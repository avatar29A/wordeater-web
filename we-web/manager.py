# coding=utf-8
__author__ = 'Warlock'

from flask.ext.script import Manager

from scripts.clear_db import ClearDatabase
from scripts.create_user import CreateUser

from app import app

manager = Manager(app)

if __name__ == "__main__":
    manager.add_command('clear_db', ClearDatabase())
    manager.add_command('create_user', CreateUser())

    manager.run()
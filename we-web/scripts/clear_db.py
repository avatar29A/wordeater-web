# coding=utf-8
__author__ = 'Warlock'

from flask.ext.script import Command
from domain.model import db


class ClearDatabase(Command):
    """
    Remove all rows from database
    """

    def _clear(self, collection):
        print u"Clear collection '{0}'".format(collection.__collection__)
        collection.drop()

    def run(self):
        print u'*** Run cleaning database\n'

        self._clear(db.User)
        self._clear(db.Group)
        self._clear(db.Card)
        self._clear(db.LoginAudit)

        print u"\ndone"

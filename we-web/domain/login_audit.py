# coding=utf-8
from model import *


@db.register
class LoginAudit(BaseDocument):
    __collection__ = "login_audits"

    structure = {
        'login': unicode,
        'ip': unicode,
        'stamp': datetime.datetime,
        'author': ObjectId
    }

    @staticmethod
    def get_collection():
        return db.LoginAudit

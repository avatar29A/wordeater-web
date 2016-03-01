# coding=utf-8
from model import *


@db.register
class LoginAudit(BaseDocument):
    __collection__ = "login_audits"

    structure = {
        'login': unicode,
        'ip': unicode,
        'stamp': datetime.datetime
    }

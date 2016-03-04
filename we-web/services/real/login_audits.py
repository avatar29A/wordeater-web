# coding=utf-8
__author__ = 'Warlock'

from services.base import BaseService
from datetime import datetime
from logger import logger


class LoginAutits(BaseService):
    def create(self, login, ip):
        assert login and ip, u"Login and IP can't be is empty"

        login_audit = self.db.LoginAudit()

        login_audit.login = login
        login_audit.ip = ip
        login_audit.stamp = datetime.now()

        try:
            login_audit.validate()
            login_audit.save()
        except Exception as ex:
            logger.error(ex.message)

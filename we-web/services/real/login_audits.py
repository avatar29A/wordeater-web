# coding=utf-8
__author__ = 'Warlock'

from services.base import BaseService
from datetime import datetime
from logger import logger


class LoginAutits(BaseService):
    def create(self, login, ip):
        login_audit = self.connection.LoginAudit()

        login_audit.login = login
        login_audit.ip = ip
        login_audit.stamp = datetime.now()

        try:
            login_audit.validate()
            login_audit.save()
        except Exception as ex:
            logger.error(ex.message)

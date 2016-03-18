import json
import requests
import config

from services.base import BaseService
from logger import error

__author__ = 'Glebov Boris'


class BluemixService(BaseService):
    def synthesize(self, text):
        """
        Synthesize text
        :param text: text for synthesize
        :return: audio/wav
        """
        data = {'text': text}
        r = requests.post(config.BLUEMIX_SYNTH_URL,
                          headers={'Content-Type': 'application/json', 'Accept': 'audio/wav'},
                          auth=(config.BLUEMIX_SYNTH_USERNAME, config.BLUEMIX_SYNTH_PASSWORD),
                          data=json.dumps(data))

        if r.status_code == 200:
            return r.content
        else:
            return None

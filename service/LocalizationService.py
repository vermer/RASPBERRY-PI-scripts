#!/usr/bin/env python
import json
from urllib import urlopen

from LoggingService import LoggingService
from TelegramService import TelegramService

SPACE = " "
COUNTRY_CODE = 'PL'
MESSAGE = "Your vpn connection is broken please reconnect. "


def getErrorMessage(code):
    return "If you need to make more requests or custom data, see our paid plans, which all have soft limits. " + code


def getTelegramMessage(jsonMessage):
    return MESSAGE + jsonMessage['country'] + SPACE + jsonMessage['ip'] + SPACE + jsonMessage['city']


class LocalizationService:
    logger = LoggingService("LocalizationService")
    json = None

    def __init__(self):
        self.logger.default()

    def getLocalizationJSON(self):
        if self.json is None:
            url = 'http://ipinfo.io/json'
            response = urlopen(url)
            if response.getcode() != 200:
                self.logger.error(getErrorMessage(str(response.getcode())))
                return None
            self.json = json.load(response)
            self.logger.debug(self.json)
            return self.json
        else:
            return self.json

    def sendMessage(self):
        j = self.getLocalizationJSON()
        if j['country'] == COUNTRY_CODE:
            TelegramService.sendMessage(getTelegramMessage(j))

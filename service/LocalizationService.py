#!/usr/bin/env python
import json
from urllib import urlopen

from LoggingService import LoggingService
from TelegramService import TelegramService


def getErrorMessage(code):
    return "If you need to make more requests or custom data, see our paid plans, which all have soft limits. " + code


class LocalizationService:
    logger = LoggingService("LocalizationService")
    json = None
    MESSAGE = "Your vpn connection is broken please reconnect. "
    telegramService = TelegramService()

    def __init__(self):
        self.logger.default()
        self.getLocalizationJSON()

    def getLocalizationJSON(self):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        if response.getcode() != 200:
            self.logger.error(getErrorMessage(str(response.getcode())))
            return None
        self.json = json.load(response)
        self.logger.debug(self.json)

    def getTelegramMessage(self):
        return self.MESSAGE + self.json['country'] + " " + self.json['ip'] + " " + self.json['city']

    def sendMessage(self):
        try:
            if self.json['country'] == 'PL':
                self.telegramService.sendMessage(self.getTelegramMessage())
        except:
            self.logger.error("There is problem with connection please Try again later")

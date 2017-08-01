#!/usr/bin/env python
import json
from urllib import urlopen

import requests

from LoggingService import LoggingService
from TelegramService import TelegramService

CLASS_NAME = "LocalizationService"
CITY = 'city'
IP = 'ip'
COUNTRY = 'country'
URL = 'http://ipinfo.io/json'
SPACE = " "
COUNTRY_CODE = 'PL'
MESSAGE = "Your vpn connection is broken please reconnect. "


def getErrorMessage(code):
    return "If you need to make more requests or custom data, see our paid plans, which all have soft limits. " + code


def getTelegramMessage(jsonResponse):
    return MESSAGE + jsonResponse[COUNTRY] + SPACE + jsonResponse[IP] + SPACE + jsonResponse[CITY]


def checkIfCountryCodeFromJSONisEqualCountryCode(jsonResponse):
    return jsonResponse[COUNTRY] == COUNTRY_CODE


def sendMessage(jsonResponse):
    TelegramService.sendMessage(getTelegramMessage(jsonResponse))


class LocalizationService:
    logger = LoggingService(CLASS_NAME)
    json = None

    def __init__(self):
        self.logger.default()

    def run(self):
        self.checkIfMessageShouldBeSend()

    def getLocalizationJSON(self):
        if self.json is not None:
            return self.json
        else:
            return self.getJSON()

    def getJSON(self):
        try:
            response = urlopen(URL)
        except requests.ConnectionError:
            self.logger.error("Connection problem with" + URL)
        self.logger.error(getErrorMessage(str(response.getcode())))
        return self.saveJSON(response)

    def saveJSON(self, response):
        self.json = json.load(response)
        self.logger.debug(self.json)
        return self.json

    def checkIfMessageShouldBeSend(self):
        jsonResponse = self.getLocalizationJSON()
        if checkIfCountryCodeFromJSONisEqualCountryCode(jsonResponse):
            sendMessage(jsonResponse)

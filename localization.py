#!/usr/bin/env python
import ConfigParser
import json
import urllib
from urllib import urlopen
import logging
from logging import handlers

class LocalizationSender:
    logger = None
    json = None
    MESSAGE = "Your vpn conection is broken please recconect. "
    def __init__(self):
        handler = logging.handlers.RotatingFileHandler('localization.log', maxBytes=1000000, backupCount=5)
        self.logger = logging.getLogger('LocalizationSender')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.getLocalizationJSON()

    def getErrorMessage(self, code):
        return "If you need to make more requests or custom data, see our paid plans, which all have soft limits. " + code

    def messageLogger(self, text):
        self.logger.info(text)

    def getConfig(self):
        config = ConfigParser.ConfigParser()
        config.read('localization.ini')
        return config

    def getLocalizationJSON(self):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        if response.getcode() != "200":
            self.messageLogger(self.getErrorMessage(str(response.getcode())))
        self.json = json.load(response)

    def getTelegramMessage(self):
        return self.MESSAGE + self.json['country'] + " " + self.json['ip'] + " " + self.json['city']


    def sendMessage(self):
        if self.json['country'] == 'PL':
            message = self.getTelegramMessage()
            self.messageLogger(message)
            message = urllib.urlopen(
            "https://api.telegram.org/bot" +
            self.getConfig().get('DEFAULT', 'telegramApiKey') +
            "/sendMessage?chat_id=" +
            self.getConfig().get('DEFAULT', 'telegramUsername') +
            "&text=" + message
            ).read()

localizationSender = LocalizationSender()
localizationSender.sendMessage()

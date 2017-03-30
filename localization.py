#!/usr/bin/env python
import ConfigParser
import json
import urllib
from urllib import urlopen
import logging
from logging import handlers

class LocalizationSender:
    logger = logging.getLogger('LocalizationSender')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler('localization.log', maxBytes=1000000, backupCount=5)
    logger.addHandler(handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    MESSAGE = "Your vpn conection is broken please recconect. "

    def messageLogger(self, text):
        self.logger.info(text)

    def getConfig(self):
        config = ConfigParser.ConfigParser()
        config.read('localization.ini')
        return config

    def getLocalizationJSON(self):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        return json.load(response)

    def getTelegramMessage(self):
        data = self.getLocalizationJSON()
        self.messageLogger(data)
        return self.MESSAGE + data['country'] + " " + data['ip'] + " " + data['city']


    def sendMessage(self):
        if self.getLocalizationJSON()['country'] == 'PL':
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

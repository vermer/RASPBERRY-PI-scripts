#!/usr/bin/env python
import ConfigParser
import json
import urllib
from urllib import urlopen
import logging
from logging import handlers
import datetime
import time
import httplib

class LocalizationSender:

    logger = None
    json = None
    MESSAGE = "Your vpn conection is broken please recconect. "
    CONFIG_FILE  = 'localization.ini'
    LOG_FILE_PATH = "logs\\"
    LOG_FILE = 'localization'
    LOG_FILE_EXT = '.log'

    def __init__(self):
        self.logger = logging.getLogger('LocalizationSender')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.handlers.TimedRotatingFileHandler(self.getLoggerFileName(), when='D', interval=1, backupCount=20, encoding=None)
        self.logger.addHandler(handler)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.getLocalizationJSON()

    def getLoggerFileName(self):
        now = datetime.datetime.now()
        return self.LOG_FILE_PATH + self.LOG_FILE + now.strftime("%Y-%m-%d") + self.LOG_FILE_EXT

    def getErrorMessage(self, code):
        return "If you need to make more requests or custom data, see our paid plans, which all have soft limits. " + code

    def messageLogger(self, text):
        self.logger.info(text)

    def getConfig(self):
        config = ConfigParser.ConfigParser()
        config.read(self.CONFIG_FILE)
        return config

    def getLocalizationJSON(self):
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        if response.getcode() != 201:
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

import configparser
import requests

CONFIG_FILE = 'localization.ini'


def getConfig():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def telegram_url(apiKey):
    return 'https://api.telegram.org/bot' + apiKey + "/sendMessage"


class TelegramService:
    def __init__(self):
        pass

    @staticmethod
    def sendMessage(message):
        parameters = {'chat_id': getConfig().get('DEFAULT', 'chat_id'), 'text': message}
        apiKey = getConfig().get('DEFAULT', 'telegramApiKey')
        requests.get(telegram_url(apiKey), data=parameters)

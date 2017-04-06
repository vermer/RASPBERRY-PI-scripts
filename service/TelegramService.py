import urllib
import ConfigParser
import requests

class TelegramService:

    CONFIG_FILE  = 'localization.ini'

    def sendMessage(self, message):
        parameters = {'chat_id' : self.getConfig().get('DEFAULT', 'chat_id'), 'text' : message}
        apiKey = self.getConfig().get('DEFAULT', 'telegramApiKey')
        r = requests.get('https://api.telegram.org/bot' + apiKey + "/sendMessage", data = parameters)

    def getConfig(self):
        config = ConfigParser.ConfigParser()
        config.read(self.CONFIG_FILE)
        return config

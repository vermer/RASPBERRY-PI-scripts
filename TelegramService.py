import urllib
import ConfigParser

class TelegramService:

    CONFIG_FILE  = 'localization.ini'

    def sendMessage(self, message):
        '''self.messageLogger(message)'''
        request = urllib.urlopen(
        "https://api.telegram.org/bot" +
        self.getConfig().get('DEFAULT', 'telegramApiKey') +
        "/sendMessage?chat_id=" +
        self.getConfig().get('DEFAULT', 'telegramUsername') +
        "&text=" + message
        ).read()

    def getConfig(self):
        config = ConfigParser.ConfigParser()
        config.read(self.CONFIG_FILE)
        return config

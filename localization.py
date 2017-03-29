#!/usr/bin/env python
import ConfigParser
import json
import urllib
from urllib import urlopen

import logging
logging.basicConfig(filename='localization.log',level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

config = ConfigParser.ConfigParser()
config.read('localization.ini')
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

IP = data['ip']
org = data['org']
city = data['city']
country = data['country']
region = data['region']

message = "Your vpn conection is broken please recconect " + country + " " + IP + " " + city + " " + org + " " + region

if country == 'PL':
    message = urllib.urlopen(
        "https://api.telegram.org/bot" +
        config.get('DEFAULT', 'telegramApiKey') +
        "/sendMessage?chat_id=" +
        config.get('DEFAULT', 'telegramUsername') +
        "&text=" + message
        ).read()

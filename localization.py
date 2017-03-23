#!/usr/bin/env python
import re
import json
import urllib
from urllib import urlopen

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

IP=data['ip']
org=data['org']
city = data['city']
country=data['country']
region=data['region']

if country =='PL':
    urllib.urlopen("https://api.telegram.org/bot328753599:AAFmc2WwoKgHZgpoO0FMUlU08Z8oyFhhbFU/sendMessage?chat_id=@RaspberryPILUm&text=" + country +" "+ IP+ " "  + city).read()

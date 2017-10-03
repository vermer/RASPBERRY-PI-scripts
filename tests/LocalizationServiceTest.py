#!/usr/bin/env python
import json
import unittest
from service.LocalizationService import LocalizationService
from service.LocalizationService import LocalizationService
from service.LocalizationService import getErrorMessage
from service.LocalizationService import getTelegramMessage
from service.LocalizationService import COUNTRY
from service.LocalizationService import SPACE
from service.LocalizationService import IP
from service.LocalizationService import CITY

CODE = '123456'
JSON = json.dumps({"ip": "31.172.182.114",
                   "hostname": "No Hostname",
                   "city": "Wawel",
                   "region": "Malopolskie",
                   "country": "PL",
                   "loc": "50.0500,19.9333",
                   "org": "AS50481 Fibertech Networks Sp. z o.o.",
                   "postal": "30-811"
                   })


class LocalizationServiceTest(unittest.TestCase):
    localizationService = LocalizationService();

    def testGetTelegramMessage(self):
        resp = json.loads(JSON)
        self.assertEqual(getTelegramMessage(JSON),
        "Your vpn connection is broken please reconnect. " + resp[COUNTRY] + SPACE + resp[IP] + SPACE + resp[CITY])

    def testGetErrorMessage(self):
        self.assertEqual(getErrorMessage(CODE),
        "If you need to make more requests or custom data, see our paid plans, which all have soft limits. " + CODE)


if __name__ == '__main__':
    unittest.main()

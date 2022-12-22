import requests
import json
from datetime import datetime as dt
from Advertising import Advertising, CSV

class Request:

    _url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    _data = {
        "asset": "USDT",
        "fiat": "RUB",
        "merchantCheck": False,
        "page": 1,
        "payTypes": ["TinkoffNew"],
        # "transAmount": 1000,
        "publisherType": None,
        "rows": 10,
        "tradeType": "BUY"
    }

    _headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
    }

    def request(self):
        time = dt.now().strftime("%d.%m.%Y %H:%M:%S")
        r = requests.post(url, headers=headers, json=data)
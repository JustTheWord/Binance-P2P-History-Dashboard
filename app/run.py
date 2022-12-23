import sys

import requests
import json
import logging
from datetime import datetime as dt
import time
from adv_objects import Advertisment, CSV # type: ignore

class Request:

    _url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    _data = {
        "asset": "USDT",
        "fiat": "RUB",
        "merchantCheck": False,
        "page": 1,
        "payTypes": ["TinkoffNew"],
        "publisherType": None,
        "rows": 20, # exploring the first 20 advertisements
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

    logging.basicConfig(level=10,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)])

    logger = logging.getLogger("Request")


    def request(self):
        self.logger.info("Requesting data from Binance")
        request_time = dt.now().strftime("%d.%m.%Y %H:%M:%S")
        r = requests.post(self._url, headers=self._headers, json=self._data)

        if not r.ok:
            self.logger.error("Request failed")
            return None

        else:
            self.logger.info("Request successful")

            adv_data = json.loads(r.text)['data']
            valid_advs = []

            for row in adv_data:
                adv = row['adv']
                advertiser = row['advertiser']

                if float(advertiser['monthFinishRate']) < 0.9 or\
                        int(advertiser['monthOrderCount']) < 15 or\
                        float(adv['surplusAmount']) < 100 or\
                        float(adv['minSingleTransAmount']) > 45_000:

                    """Not interested in such advertising"""
                    continue

                valid_advs.append(

                    Advertisment(float(adv['price']),
                                 float(adv['surplusAmount']),
                                 float(adv['minSingleTransAmount']),
                                 float(adv['dynamicMaxSingleTransAmount']),
                                 [method['identifier'] for method in adv['tradeMethods']],

                                 advertiser['userNo'],
                                 advertiser['userType'],
                                 advertiser['nickName'],
                                 float(advertiser['monthFinishRate']),
                                 int(advertiser['monthOrderCount']))
                )

            csv = CSV(time=request_time)

            if not valid_advs:
                self.logger.info("No valid advertising found")

            else:
                success = csv.write(valid_advs)
                self.logger.info("Data written to file") if success else self.logger.error("Data writing failed")


if "__main__" == __name__:
    try:
        while True:
            Request().request()
            time.sleep(30)

    except KeyboardInterrupt:
        print("---------------")
        print("Stop requesting")


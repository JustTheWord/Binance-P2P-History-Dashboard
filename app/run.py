import socket
import sys
import requests
from requests.exceptions import ConnectionError
import json
import logging
from datetime import datetime as dt
import time
from typing import Dict, Any
from objects import Advertisement, CSV, Logger # type: ignore

class Request:

    _url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

    def __init__(self,
                 request_config: Dict[str, Any],
                 headers: Dict[str, Any],
                 logger: Logger,):

        self._config = request_config
        self._data = request_config['data']
        self._headers = headers
        self.trade_type = self._data['tradeType'].lower() # 'buy' or 'sell'

        self.logger = logger.get_logger(f'Request{self.trade_type.capitalize()}')


    def request(self):
        self.logger.info("Requesting data from Binance")
        request_time = dt.now().strftime("%d.%m.%y %H:%M:%S")
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

                if float(advertiser['monthFinishRate']) < self._config['monthFinishRate'] or\
                        int(advertiser['monthOrderCount']) < self._config['monthOrderCount'] or\
                        float(adv['surplusAmount']) < self._config['surplusAmount'] or\
                        float(adv['minSingleTransAmount']) > self._config['minSingleTransAmount']:

                    """Not interested in such advertisements"""
                    continue

                valid_advs.append(

                    Advertisement(float(adv['price']),
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

            if not valid_advs:
                self.logger.info("No valid advertising found")

            else:
                """All data will be saved in the data folder according to the date"""
                filename = request_time.split(' ')[0] + '_' + self.trade_type + '.csv'
                csv = CSV(time=request_time, filename=f"../data/{filename}")
                success = csv.write(valid_advs)
                self.logger.info("Data written to file") if success else self.logger.error("Data writing failed")


if "__main__" == __name__:

    with open('../config.json', 'r') as conf:
        config = json.load(conf)

    log = Logger()
    main_logger = log.get_logger('Main')
    """Variable to restart the program if the connection is lost"""
    tries = 0

    while True:
        try:
            request = Request(config['buy'], config['headers'], log)
            request.request()
            main_logger.info("--------------------")

            request = Request(config['sell'], config['headers'], log)
            request.request()
            main_logger.info("--------------------")
            time.sleep(28)

        except (ConnectionError, socket.gaierror) as err:
            tries += 1
            wait = 2 ** tries # exponential backoff
            main_logger.error(f"Connection error: {err}. Waiting {wait} seconds")

            if tries > 8:
                main_logger.error("Too many connection errors. Exiting")
                raise err

            else:
                time.sleep(wait)
                continue

        except KeyboardInterrupt:
            main_logger.info("--------------------")
            main_logger.info("Program stopped by user")
            break

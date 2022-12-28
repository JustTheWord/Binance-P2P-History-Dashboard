from typing import List, Optional
import csv
import os
import sys
import logging


class CSV:
    def __init__(self,
                 filename: str = 'data.csv',
                 time: str = "00.00.0000 00:00:00"):

        """"Filename is the name of the file to write to"""
        self._filename = filename
        """Time is the time of the request"""
        self._time = time

    """Writes data to a csv file"""
    def write(self, advs_list: List['Advertisement']) -> bool:
        """Binance is already sorted advertising by price -> the best is the first"""
        top_advertising = advs_list[0]

        adv_processed = len(advs_list)

        """Average price of all valid advertisements"""
        average_price = sum([adv.price for adv in advs_list]) / adv_processed
        """Round to 2 decimal places"""
        average_price = float(f"{average_price:.2f}")

        top_price = top_advertising.price
        available_amount = top_advertising.available_amount
        min_trans_amount = top_advertising.min_transaction
        max_trans_amount = top_advertising.max_transaction
        month_finish_rate = top_advertising.month_finish_rate
        month_order_count = top_advertising.month_order_count
        trade_methods = '|'.join(top_advertising.trade_methods)
        user_no = top_advertising.user_no
        user_type = top_advertising.user_type
        nick_name = top_advertising.nick_name


        with open(self._filename, 'a', newline='') as file:

            writer = csv.writer(file, delimiter=';')

            """If file is empty -> write header"""
            if os.stat(self._filename).st_size == 0:
                try:
                    writer.writerow(['date', 'processed','averagePrice', 'topPrice',
                                     'availableAmount', 'minSingleTransAmount', 'maxSingleTransAmount',
                                     'monthFinishRate', 'monthOrderCount', 'tradeMethods',
                                     'userNo', 'userType', 'nickName'])

                except csv.Error:
                    """If something goes wrong return False to log it"""
                    return False

            """Write data"""
            try:
                writer.writerow([self._time, adv_processed, average_price, top_price,
                                 available_amount, min_trans_amount, max_trans_amount,
                                 month_finish_rate, month_order_count, trade_methods,
                                 user_no, user_type, nick_name])
                return True

            except csv.Error:
                return False

class Advertisement:

    def __init__(self,
                 price: float = 0.0,
                 available_amount: float = 0.0,
                 min_transaction: float = 0.0,
                 max_transaction: float = 0.0,
                 trade_methods: List[str] = [],

                 user_no: str = '',
                 user_type: str = 'user',
                 nick_name: str = '',
                 month_finish_rate: float = 0.0,
                 month_order_count: int = 0):

        self.price = price
        self.available_amount = available_amount
        self.min_transaction = min_transaction
        self.max_transaction = max_transaction
        self.trade_methods = trade_methods

        self.user_no = user_no
        self.user_type = user_type
        self.nick_name = nick_name
        self.month_finish_rate = month_finish_rate
        self.month_order_count = month_order_count


class Logger:

    logging.basicConfig(level=10,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        handlers=[logging.FileHandler("../logs/app.log"),
                                  logging.StreamHandler(sys.stdout)])
    def __init__(self):
        self._logger = logging.getLogger('Main')
        self._logger_buy = logging.getLogger('RequestBuy')
        self._logger_sell = logging.getLogger('RequestSell')

    def get_logger(self, name: str = 'Main') -> logging.Logger:
        match name:
            case 'Main':
                return self._logger

            case 'RequestBuy':
                return self._logger_buy

            case 'RequestSell':
                return self._logger_sell
from typing import List


class CSV:
    def __init__(self,
                 trade_type: str,
                 time: str = "00.00.0000 00:00:00",
                 adv_list: List['Advertising'] = None,
                 ):
        self.trade_type = trade_type
        self._time = time
        self._adv_processed = len(adv_list)

    @property
    def get_csv(self):
        pass


class Advertising:

    def __init__(self,
                 price: float = None,
                 identifier: str = None,
                 user_no: str = None):
        self.price = price
        self.identifier = identifier
        self.user_no = user_no



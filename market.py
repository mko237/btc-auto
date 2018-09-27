from scratch import HistoryClient
from time import sleep

class Market:

    def __init__(self,get_data=True):
        self.history = HistoryClient()
        self.state_window_len = 130
        self.last_interval_id = self.state_window_len
        if get_data:
            self._init_data()

    def _init_data(self):
        self.data = self.history.get_data(interval_mins=5,total_days=3)
        sleep(20)
        print("init data:",self.data[0])
        #self.data = [float(x) for x in data]
        self.data_pct = self.history.to_pct_change(self.data)
        self.data_len = len(self.data)

    def set_data(self,data):
        self.data = data
        self.data_len = len(self.data)
        self.data_pct = self.history.to_pct_change(self.data)

    def next_state():
        self.last_interval_id += 1

    def get_state(self):
        if self.last_interval_id > self.data_len - 1:
            state = None
        else:
            start_index = self.last_interval_id - self.state_window_len
            state = self.data_pct[start_index:self.last_interval_id]
        return state

    def get_price(self,symbol):
        price = self.data[self.last_interval_id]
        if symbol.upper()[:3] == "USD":
           price = 1/price
        return price


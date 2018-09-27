import pymongo
import random
import numpy as np
from datetime import datetime,timedelta
client = pymongo.MongoClient('localhost',27017)
db =  client.btc_auto

class HistoryClient():

    def __init__(self):
        pass
    def get_max_guid(self):
        try:
            res = db.coins.find_one(sort=[('guid',pymongo.DESCENDING)])["guid"]
        except TypeError:
            res = 1
        return res

    def get_max_end_time(self):
        res = db.coins.find_one(sort=[('data.k.T',pymongo.DESCENDING)])["data"]["k"]["T"]
        res = datetime.fromtimestamp(res/1000)
        return res

    def get_min_end_time(self):
        res = db.coins.find_one(sort=[("data.k.T",pymongo.ASCENDING)])['data']['k']['T']
        res = datetime.fromtimestamp(res/1000)
        return res

    def get_data(self,start_time=None,interval_mins=1,total_days=1):
        rows = []
        intervals_in_day = 1440/interval_mins
        num_total_mins = total_days * intervals_in_day * interval_mins
        if start_time is None:
            max_start = (self.get_max_end_time() - timedelta(minutes=num_total_mins)).timestamp()*1000
            min_start = self.get_min_end_time().timestamp()*1000
            start_time = random.randint(min_start,max_start)
            start_time = (datetime.now() - timedelta(days=5)).timestamp()*1000
            start_time = random.normalvariate(start_time,8.64e+7)
        print("interval_mins: {}".format(interval_mins))
        print("interval_in_day: {}".format(intervals_in_day))
        print("start_time: {}".format(datetime.fromtimestamp(start_time/1000)))
        coins_cursor = db.coins.find({"stream_name":"btcusdt@kline_1m"
                                              ,"data.k.T":{"$gt":start_time}})

        print("coins: {}".format(coins_cursor.count()))

        for i,row in enumerate(list(coins_cursor)):
            if i < num_total_mins and i % interval_mins==0:
                rows.append(float(row['data']['k']['o']))
            elif i>num_total_mins:
                break

        return rows

    def to_pct_change(self,array):
        array = list(map(float,array))
        pct_array = []
        for i in range(len(array)):
            if i == 0:
                pct = 0.0
            else:
                pct = ((array[i] - array[i-1])/array[i-1])*100
            pct_array.append(pct)
        return pct_array

if __name__ ==  '__main__':
    h = HistoryClient()
    rows = h.get_data(interval_mins=20)
    pct_rows = h.to_pct_change(rows)
    print(rows[:40])
    print(pct_rows[:40])


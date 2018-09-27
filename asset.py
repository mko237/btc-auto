#class Asset():
#
#    def __init__(self,broker='GDAX'):
#        self.last_updated = 'xxx' # this should be a clock()/timestamp
#
#
#    def get_price(self):
#        pass
#
#    def get_statistic(self): #get_asset_stat(assest_name,statistic={}): statistic =  price sma, ema
#
#
#    def calc_sma(self,period):
#        pass
import numpy as np
import talib
import pprint
import asyncio
import aioredis
import json
import random
#rint("STARTING REDIS SUB TEST")
# Util
kline_key_mapping = dict(t='start_time'
                        ,T='end_time'
                        ,s='symbol'
                        ,i='interval'
                        ,f='first_trade_id'
                        ,L='last_trade_id'
                        ,o='open'
                        ,c='close'
                        ,h='high'
                        ,l='low'
                        ,v='volume'
                        ,n='trades'
                        ,x='end_of_kline'
                        ,q='volume_quote'
                        ,V='volume_active_buy'
                        ,Q='volume_quote_active_buy'
                        ,B='ignore'
                        )
kline_socket_mapping = dict(e='event_type'
                           ,E='event_time'
                           ,s='symbol'
                           ,k='kline'
                           )
kline_history_length=300



async def reader(stream_name):
    print("Listening for msgs from: {}...".format(stream_name))
    sub = await aioredis.create_redis(('localhost',6379))
    pub = await aioredis.create_redis(('localhost',6379))
    channel = await sub.subscribe(stream_name)
    #print(channel,type(channel))
    kline_history = np.array([])
    while True:
       msg = await channel[0].get(encoding='utf-8')
       msg = msg.replace('\'','\"')
       msg = msg.replace("False","\"False\"")
       msg = msg.replace("True","\"True\"")
       msg_json = json.loads(msg)
       #i = random.uniform(0,4)
       #await asyncio.sleep(i)
       msg_json = {(kline_socket_mapping[k] if k in kline_socket_mapping.keys() else k):v for k,v in msg_json.items() }
       msg_json["kline"]={(kline_key_mapping[k] if k in kline_key_mapping.keys() else k):v for k,v in msg_json["kline"].items()}
       if msg_json["kline"]["end_of_kline"] == "True":
          close = float(msg_json["kline"]["close"])
          kline_history = np.append(kline_history,close)
          if kline_history.size > kline_history_length:
              kline_history = np.delete(kline_history,0)
          msg_json["kline_history"] = kline_history.tolist()[-15:]
          msg_json["sma_30"] = talib.SMA(kline_history,30).tolist()[-5:]
          msg_json["sma_90"] = talib.SMA(kline_history,90).tolist()[-5:]
          print("{}".format(stream_name),end=': ')
          pprint.pprint(msg_json)
          pub.publish_json("assets",msg_json)

loop = asyncio.get_event_loop()

loop.create_task(reader("btcusdt@kline_1m"))
loop.create_task(reader("ethusdt@kline_1m"))
loop.run_forever()

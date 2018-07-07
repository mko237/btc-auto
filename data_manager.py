#import binance_account
#
#class DataManager():
#    """This class should manage/match all strategies agaisnt all incoming data streams"""
#    def __init__(self,period=1):
#        self.period = period # used to determine update freq/period
#
#
#    def update_asset_price(self,asset):
#        pass
#
#    def update_account_balance(self,account):
#        pass
#
#    def update_account_positions(self,account):
#        pass
#
#    def updates_all

from binance_algotrader import BinanceAccount
import redis
r = redis.StrictRedis('localhost',6379)
account = BinanceAccount()

def publish_to_redis(msg):
    stream_name = msg['stream']
    r.publish(stream_name,msg['data'])


print("Starting redis mulistream...")
account.start_multi_stream(streams=["btcusdt@kline_1m","ethusdt@kline_1m"],callback=publish_to_redis)

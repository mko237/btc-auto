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
import pymongo
from builtins import TypeError
from binance_algotrader import BinanceAccount
import redis
r = redis.StrictRedis('localhost',6379)
account = BinanceAccount()
client = pymongo.MongoClient('localhost',27017)
db =  client.btc_auto
db.coins.create_index([("guid",pymongo.ASCENDING)],unique=True)

def get_next_guid():
    try:
        res = db.coins.find_one(sort=[('guid',pymongo.DESCENDING)])["guid"]+1
    except TypeError:
        res = 1
    return res

def save_to_db(msg,guid=None):
    if not guid:
        guid = get_next_guid()
    record = dict()
    record["stream_name"] = msg['stream']
    record["guid"] = guid
    record["data"] = msg["data"]
    db.coins.insert_one(record)

def publish_to_redis(msg,guid):
    stream_name = msg['stream']
    msg['data']['guid'] = guid
    r.publish(stream_name,msg['data'])

def process_msg(msg):
    guid = get_next_guid()
    save_to_db(msg,guid)
    publish_to_redis(msg,guid)


print("Starting redis mulistream...")
account.start_multi_stream(streams=["btcusdt@kline_1m","ethusdt@kline_1m"],callback=process_msg)

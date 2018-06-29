from binance_algotrader import BinanceAccount
import redis
r = redis.StrictRedis('localhost',6379)
account = BinanceAccount()

def publish_to_redis(msg):
   r.publish("redis_test",msg)

account.start_ticker_stream(symbol="BTCUSDT",callback=publish_to_redis)



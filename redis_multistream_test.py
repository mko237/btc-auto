from binance_algotrader import BinanceAccount
import redis
r = redis.StrictRedis('localhost',6379)
account = BinanceAccount()

def publish_to_redis(msg):
    stream_name = msg['stream']
    r.publish(stream_name,msg['data'])

print("Starting redis mulistream...")
account.start_multi_stream(streams=["btcusdt@kline_1m","ethusdt@kline_1m"],callback=publish_to_redis)



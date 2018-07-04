import asyncio
import aioredis
import json
import random
#rint("STARTING REDIS SUB TEST")

async def reader(stream_name):
    print("Listening for msgs from: {}...".format(stream_name))
    sub = await aioredis.create_redis(('localhost',6379))
    channel = await sub.subscribe(stream_name)
    #print(channel,type(channel))
    while True:
       msg = await channel[0].get(encoding='utf-8')
       msg = msg.replace('\'','\"')
       msg_json = json.loads(msg)
       #i = random.uniform(0,4)
       #await asyncio.sleep(i)
       print("{}: {}".format(stream_name,msg_json['c']))

loop = asyncio.get_event_loop()

loop.create_task(reader("btcusdt@kline_1m"))
loop.create_task(reader("ethusdt@kline_1m"))
loop.run_forever()

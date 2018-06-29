import asyncio
import aioredis
import json
import random
#rint("STARTING REDIS SUB TEST")

async def reader():

    sub = await aioredis.create_redis(('localhost',6379))
    channel = await sub.subscribe("redis_test")
    #print(channel,type(channel))
    while True:
       msg = await channel[0].get(encoding='utf-8')
       msg = msg.replace('\'','\"')
       msg_json = json.loads(msg)
       #i = random.uniform(0,4)
       #await asyncio.sleep(i)
       print("ASYNC READER: {}".format(msg_json['c']))
async def rng():
    while True:
        print(random.uniform(1,100))
        print ("___________------------____________---------_________")
        i = random.uniform(0,4)
        await asyncio.sleep(i)

#tsk1 = asyncio.ensure_future(rng())
#tsk2 = asyncio.ensure_future(reader())
loop = asyncio.get_event_loop()

loop.create_task(reader())
loop.create_task(rng())
loop.run_forever()

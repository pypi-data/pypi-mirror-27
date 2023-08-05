#!/usr/bin/env python
#-*-coding:utf-8-*-

#异步连接aioredis
import aioredis
import asyncio
try:
    import uvloop
    loop = asyncio.set_event_loop_policy(uvloop.EventLoopPolicy)
except:
    loop = asyncio.get_event_loop()

#config_dt
r_dt = {
    "host":"localhost",
    "port":6379,
    "minsize":5,
    "maxsize":10,
}
async def r():
    pool = await aioredis.create_pool(
        (r_dt.get("host"),r_dt.get("port")),
        loop=loop
    )
    with await pool as rcon:
        await rcon.set("my","haha")
        print((await rcon.get("my")))
    pool.clear()

loop.run_until_complete(r())

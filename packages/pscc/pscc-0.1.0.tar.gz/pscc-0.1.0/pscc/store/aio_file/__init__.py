#!/usr/bin/env python
#-*-coding:utf-8-*-

#异步操作文件

import aiofiles
import asyncio
from aiofiles import os as fio
import os
root_path = "/root/Downloads/Pscc/test"
text = os.path.join(root_path,"test.text")
# print(text)
#输入文件长度
async def read_file_stat():
    stat = await fio.stat(text)
    print(stat.st_size)
#读取文件
async def async_read():
    async with aiofiles.open(text,"rb") as f:
        # print(type)
        async for i in f:
            print(i)
#写入文件
async def async_write():
    async with aiofiles.open(text,"wb") as f:
        # print(type)
        sents = "a in b".encode("utf-8")
        await f.write(sents)


if __name__ == "__main__":
    try:
        import uvloop
        loop = asyncio.set_event_loop_policy(uvloop.EventLoopPolicy)
    except:
        loop = asyncio.get_event_loop()
    # loop.run_until_complete(async_read())
    # loop.run_until_complete(read_file_stat())
        loop.run_until_complete(async_write())

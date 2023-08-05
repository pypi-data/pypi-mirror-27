#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="读写文本的基本操作"

import asyncio

import aiofiles

# 日志配置
from pscc.utils.Logconfig import load_my_logging_cfg

logger = load_my_logging_cfg("crawler_status")

# 异步操作文件夹


class AFile:

    def __init__(self, fn, data=None):
        self.filename = fn
        self.data = data

    async def control(self):
        pass
# 读取文件夹操作

# 写入文件夹操作


class AWrite(AFile):

    def __init__(self, fn, data=None, ftype="ab+"):
        super(AWrite, self).__init__(fn, data)
        self.ftype = ftype

    async def control(self):
        async with aiofiles.open(self.filename, self.ftype) as f:
            try:
                data = str(self.data).encode("utf-8")
            except Exception as e:
                data = str(self.data)
            try:
                await f.write(data)
            except TypeError as e:
                logger.info("类型错误,非byte存储,开始转化{}".format(data))
                fdata = data.decode("utf-8")
                logger.info("转化完成{}".format(fdata))
                await f.write(fdata)


if __name__ == "__main__":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()
    except ImportError as e :
        loop = asyncio.get_event_loop()
    a = AWrite("test.text")
    loop.run_until_complete(a.control())

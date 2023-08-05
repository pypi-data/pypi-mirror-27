#!/usr/bin/env python
#-*-coding:utf-8-*-

import asyncio
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError as e:
    pass

from pscc.utils.Logconfig import load_my_logging_cfg
logger = load_my_logging_cfg("crawler_status")
from pscc.config import DevConfig


"""实例化配置"""
reqcfg = DevConfig().request
rescfg = DevConfig().response


async def fetch(url, retry, spider, session, semaphore):
    """普通请求方式"""
    with (await semaphore):
        try:
            if callable(spider.headers):

                headers = spider.headers()
            else:
                headers = spider.headers
            async with session.get(url, headers=headers,
                                   proxy=spider.proxy(),
                                   timeout=int(reqcfg("timeout")),
                                   params=spider.params) as response:
                if rescfg(response.status)[0]:
                    try:
                        data = await response.text()
                    except:
                        data = await response.text(encoding="gbk")
                    return data
                logger.error('Error: {} {} retry remaining-{} {}'.format(url, response.status, retry, rescfg(response.status)[1]))
                return None
        except:
            pass
    return None


async def api_requests(url, spider, method, session, semaphore):
    """api 请求方式"""
    with (await semaphore):
        try:
            if callable(spider.headers):

                headers = spider.headers()
            else:
                headers = spider.headers
            if method == "get":
                async with session.get(url, headers=headers,
                                       proxy=spider.proxy(),
                                       timeout=int(reqcfg("timeout")),
                                       params=spider.params) as response:
                    if rescfg(response.status)[0]:
                        try:
                            data = await response.text()
                        except UnicodeEncodeError as e:
                            data = await response.text(encoding="gbk")
                        return data
                    logger.error('Requests Errors: {} {}  {}'.format(url, response.status, rescfg(response.status)[1]))
                    return None
        except:
            pass
    return None

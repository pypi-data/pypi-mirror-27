import asyncio
import re
from datetime import datetime

import aiohttp

from pscc.requests import api_requests
from pscc.requests import fetch
from pscc.utils.Logconfig import load_my_logging_cfg

# from config import DevConfig
logger = load_my_logging_cfg("crawler_status")

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError as e:
    pass


class Spider:
    start_url = ''
    base_url = None
    parsers = []
    error_urls = []
    params = []
    urls_count = 0
    concurrency = 5
    interval = None # Todo: Limit the interval between two requests
    headers = {}
    proxyable = None
    proxy_url = None
    api = False
    api_method = None
    retry = 3

    @classmethod
    def proxy(cls):
        if cls.proxyable:
            cls.proxy_url = 1
        else:
            pass
        return cls.proxy_url

    @classmethod
    def is_running(cls):
        is_running = False
        for parser in cls.parsers:
            if len(parser.pre_parse_urls) > 0 or len(parser.parsing_urls) > 0:
                is_running = True
        return is_running

    @classmethod
    def parse(cls, html):
        for parser in cls.parsers:
            parser.parse_urls(html, cls.base_url)

    @classmethod
    def run(cls):
        logger.info('Spider started!')
        start_time = datetime.now()
        loop = asyncio.get_event_loop()
        if not cls.api:
            """
            获取基域名
            """
            if cls.base_url is None:
                cls.base_url = re.match('(http|https)://[\w\-_]+(\.[\w\-_]+)+/', cls.start_url).group()
                logger.info('Base url: {}'.format(cls.base_url))
            try:
                semaphore = asyncio.Semaphore(cls.concurrency)
                tasks = asyncio.wait([parser.task(cls, semaphore) for parser in cls.parsers])
                loop.run_until_complete(cls.init_parse(semaphore))
                loop.run_until_complete(tasks)
            except KeyboardInterrupt:
                for task in asyncio.Task.all_tasks():
                    task.cancel()
                loop.run_forever()
            finally:
                end_time = datetime.now()
                for parser in cls.parsers:
                    if parser.item is not None:
                        logger.info('Item "{}": {}'.format(parser.item.name, parser.item.count))
                logger.info('Requests count: {}'.format(cls.urls_count))
                logger.info('Error count: {}'.format(len(set(cls.error_urls))))
                logger.info('Time usage: {}'.format(end_time - start_time))
                logger.info('Spider finished!')
                loop.close()
        else:
            try:
                semaphore = asyncio.Semaphore(cls.concurrency)
                loop.run_until_complete(cls.init_api_parse(semaphore))
            except:
                loop.run_forever()

    @classmethod
    async def init_parse(cls, semaphore):
        with aiohttp.ClientSession() as session:
            html = await fetch(cls.start_url, cls.retry, cls, session, semaphore)
            cls.parse(html)

    @classmethod
    async def init_api_parse(cls, semaphore):
        with aiohttp.ClientSession() as session:
            if not cls.api_method:
                cls.api_method="get"
                print(cls.api_method)
                html = await api_requests(cls.start_url, cls, cls.api_method, session, semaphore)
                print(html)

if __name__ == "__main__":
    class T(Spider):
        proxyable = None

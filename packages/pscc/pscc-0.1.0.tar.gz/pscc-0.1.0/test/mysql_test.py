#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__="2017-11-28"
# __purpose__="基本使用"

"""顶层包引入"""
import sys
sys.path.append("/root/Downloads/Pscc")

"""引入基本包，受__all__限制"""
from pscc import (XS, Item, XPathParser, Spider)
from pscc import dbsave
"""构建子域名处理方法"""


class Title(Item):

    title = XS('//h1[@id="articleTitle"]')

    async def save(self):
        save = dbsave.Insert(table="user", fl={"username": self.title})
        await save.contorl()
        # pass


"""初始爬虫"""


class MySpider(Spider):
    # 不启用代理
    proxyable = False
    # 添加初始域名
    start_url = 'http://difang.gmw.cn/jl/node_12998.htm'
    # start_url = 'https://google.com/'
    # 重试次数
    concurrency = 5
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')}
    # 解析出子域名，再由Title类解析
    parsers = [
               XPathParser('//ul[@class="channel-newsGroup"][1]/li/a/@href', Title)
              ]


if __name__ == '__main__':
    # 启动
    MySpider.run()

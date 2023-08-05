#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__=""

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


"""初始爬虫"""


class MySpider(Spider):
    # 不启用代理
    proxyable = False
    # 添加初始域名
    start_url = 'http://httpbin.org/get'
    # start_url = 'https://api.github.com/events'
    # start_url = 'https://google.com/'
    # 启用api爬取
    api = True
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')}
    # 解析出子域名，再由Title类解析



if __name__ == '__main__':
    # 启动
    MySpider.run()

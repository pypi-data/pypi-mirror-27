#!/usr/bin/env python
#-*-coding:utf-8-*-

#解析器
"""
包含基类 Selector，继承类XS、RS、QS
"""
#正则包、query包、 xpath包
import re
from lxml import etree
from pyquery import PyQuery as pq


class Selector:
    def __init__(self,rule,attr=None):
        self.rule = rule
        self.attr = attr

    def __str__(self):

        return "{}({})".format(self.__class__.__name__,self.rule)

    def __repr__(self):

        return "{}({})".format(self.__class__.__name__,self.rule)

    def parse_detail(self,html):

        print("您还未指定具体的选择器,无法帮您解析")
        raise NotImplementedError


# 使用pyquery解析

"""
:param html_code  attr? 类似href src
:return str
"""


class QS(Selector):
    def parse_detail(self,html):
        pq_content = pq(html)
        if self.attr is None:
            try:
                return pq_content(self.rule)[0].text
            except IndexError:
                return None
        return pq_content(self.rule)[0].attr(self.attr,None)

# 使用xpath解析


"""
:param html_code  attr? 类似href src
:return str
"""


class XS(Selector):
    def parse_detail(self,html):
        xp_content = etree.HTML(html)
        try:
            if self.attr is None:
                return xp_content.xpath(self.rule)[0].text
            return xp_content.xpath(self.rule)[0].get(self.attr,None)
        except IndexError:
            return None

# 使用正则表达式解析


"""
:param html_code  attr? 类似href src
:return str
"""


class RS(Selector):
    def parse_detail(self, html):
        try:
            return re.findall(self.rule, html)[0]
        except IndexError:
            return None

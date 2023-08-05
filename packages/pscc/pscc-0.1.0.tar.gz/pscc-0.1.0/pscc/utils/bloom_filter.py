#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="布隆过滤器"

import pybloom_live


class Bloom_Set:
    def __init__(self):
        self.bloom_filter = pybloom_live.ScalableBloomFilter(mode=pybloom_live.ScalableBloomFilter.LARGE_SET_GROWTH)
        self.set = set()

    def add(self,value):
        if not self.inable(value):
            self.bloom_filter.add(value)
            self.set.add(value)

    def inable(self,value):
        if value in self.bloom_filter:
            return True
        else:
            return False

    @property
    def bset(self):
        return self.set


BFS = Bloom_Set()

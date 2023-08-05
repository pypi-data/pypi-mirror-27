#!/usr/bin/env python
#-*-coding:utf-8-*-

from functools import wraps
import time

def runtime(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        start_time = time.time()
        result = func(*args,**kwargs)
        end_time = time.time()
        print("花费时间：{}".format(end_time-start_time))
        return result
    return wrap
"""
test
"""
# @runtime
# def a():
#     x = [1+1 for _ in range(10000)]
#     return x
# print(a())
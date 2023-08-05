#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="配置日志装饰器"

from pscc.utils.Logconfig import load_my_logging_cfg

"""错误日志收集器"""


class ELogger:

    def __init__(self, t):
        self.type   = t
        self.logger = None

    def init_logger(self):
        self.logger = load_my_logging_cfg(self.type)
        return self.logger

    def __call__(self,func):
        """load logger first"""
        self.init_logger()

        def logger(*args,**kwargs):
            try:
                r = func(*args,**kwargs)
                return r
            except IndexError as e:
                self.logger.info("记录错误方法:{}，错误类型以及参数:{}-{}".format(func.__name__,"索引错误",e.args))
            except TypeError as e:
                self.logger.info("记录错误方法:{}，错误类型以及参数:{}-{}".format(func.__name__,"参数类型错误",e.args))
        return logger

@ELogger("error_collect")
def a():
    raise IndexError


a()



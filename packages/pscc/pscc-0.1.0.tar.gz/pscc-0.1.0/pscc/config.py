#!/usr/bin/env python
#-*-coding:utf-8*-
# __all__=""
# __datetime__=""
# __purpose__=""

from pscc.utils.Error import (
                    NoKeyError
                        )


class Config:
    def __init__(self):
        pass

    """定义request的cfg"""

    class RequestCfg:
        request_dict = {
            "proxy": "127.0.0.1",
            "Rconcurrency": 100,
            "timeout": 100
        }

    """获取request的cfg"""
    def request(self,cfg):
        request_dict = self.RequestCfg().request_dict
        if request_dict.get(cfg):
            value = request_dict.get(cfg)
            return str(value)
        else:
            raise NoKeyError(cfg)

    """定义网页响应"""

    class ResponseCfg:
        response_dict = {
            # 2 类
            200: (True, "",),
            201: (True, "",),
            # 3 类
            # 4 类
            403: (False, "",),
            404: (False, "",),
        }

    """获取网页响应的cfg"""

    def response(self, cfg):
        response_dict = self.ResponseCfg().response_dict
        if response_dict.get(cfg):
            value = response_dict.get(cfg)
            return value
        else:
            raise NoKeyError(cfg)

    """定义网页编码"""
    """定义数据库连接"""
    class MySQLCfg:
        def __init__(self):
            self.mcfg = self.get_cfg()

        def get_cfg(self):
            conn_dt = {
                        "host": "127.0.0.1",
                        "port": 3306,
                        "database": "shape",
                        "password": "linhanqiu",
                        "user": "linhanqiu",
                        "charset": "utf8"
                       }
            return conn_dt

        def __getattr__(self, item):
            return self.mcfg.get(item)


class DevConfig(Config):
    pass


class ProConfig(Config):
    pass



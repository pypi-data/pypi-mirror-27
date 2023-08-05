#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__=""


class Error(Exception):
    def __init__(self):
        super(Error,self).__init__()


class NoKeyError(Error):
    def __init__(self,keyname):
        self.kn = keyname

    def __str__(self):
        ErrorMes = "'{}'为不存在的键，请重新输入".format(self.kn)
        return ErrorMes
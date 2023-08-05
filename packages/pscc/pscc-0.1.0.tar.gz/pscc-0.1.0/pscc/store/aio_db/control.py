#!/usr/bin/env python3
#-*-coding:utf-8-*-
# __all__=""
# __datetime__=""
# __purpose__="数据库基本操作"

import asyncio

# 使用uvloop代替asyncio的eventloop
import aiomysql

# 日志配置
from pscc.utils.Logconfig import load_my_logging_cfg

logger = load_my_logging_cfg("crawler_status")
loop = asyncio.get_event_loop()
# 导入配置库
from pscc.config import DevConfig
# 实例数据库配置
mcfg = DevConfig().MySQLCfg()


class Control:
    def __init__(self, *args, **kwargs):
        self.loop = loop

    async def conn(self):
        pool = await aiomysql.create_pool(host=mcfg.host,
                                          port=mcfg.port,
                                          user=mcfg.user,
                                          password=mcfg.password,
                                          db=mcfg.database,
                                          charset=mcfg.charset,
                                          loop=loop)
        conn = await pool.acquire()
        return conn

    async def contorl(self):
        pass

    async def run(self):
        pass


class Select(Control):
    """查询类
    :param table "user"
            fl   ["username"]
            limit 50
    :return result
    """

    def __init__(self, table=None, fl=[], limit=50, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
        self.table = table
        self.fl = fl
        self.limit = limit

    async def contorl(self):
        """封装选择查看操作"""
        conn = await self.conn()
        if len(self.fl) == 1:
            field = ''.join(self.fl)
        else:
            field = ','.join(self.fl)
        sql = "SELECT {} FROM {} LIMIT {} ;".format(field, self.table, self.limit)
        async with conn.cursor() as cur:
            await cur.execute(sql)
            c = await cur.fetchall()
            print(c)

    def __call__(self, *args, **kwargs):
        self.loop.run_until_complete(self.contorl())


class Insert(Control):
    """查询类
    :param table "user"
            fl   ["username"]
            limit 50
    :return result
    """

    def __init__(self, table=None, fl={}, *args, **kwargs):
        super(Insert, self).__init__(*args, **kwargs)
        self.table = table
        self.fl = fl

    async def contorl(self):
        """封装选择查看操作"""
        conn = await self.conn()
        if len(self.fl.keys())==1:
            fl_key = ''.join([i for i in self.fl])
            fl_value = str(self.fl[fl_key])
            if isinstance(fl_value,str):
                fl_value = fl_value.encode("utf-8")
                fl_value = fl_value.decode("utf-8")
            sql = "INSERT INTO {}({}) VALUES ('{}');".format(self.table, fl_key, fl_value)
            logger.info("Inserted {}-{} Success!".format(fl_key, fl_value))
        async with conn.cursor() as cur:
            await cur.execute(sql)
        await conn.commit()

    def __call__(self, *args, **kwargs):
        self.loop.run_until_complete(self.contorl())
        self.loop.close()


if __name__ == "__main__":
    # test
    a = Insert(table="user",fl={"username":"sadasd"})
    a()

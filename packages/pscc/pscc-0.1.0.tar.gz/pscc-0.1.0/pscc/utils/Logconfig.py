"""
logging配置
"""

import os
import logging.config

# 定义三种日志输出格式 开始

standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]' #其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# 定义日志输出格式 结束

pwd = os.getcwd()
grader_father = os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")  # 根目录

logfile_dir = os.path.dirname(os.path.abspath(__file__))  # log文件的父目录
logfile_log_dir = grader_father+"/log"

# print(logfile_log_dir)

logfile_name0 = 'crawler_status.log'  # log文件名
logfile_name1 = 'data_filter.log'  # log1文件名
logfile_name2 = 'upload_status.log'  # log2文件名
logfile_name_error = 'error.log'  # log_error文件名
logfile_name_count = 'count.log'  # log_count文件名

# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_log_dir):
    os.mkdir(logfile_log_dir)

# log文件的全路径
logfile_path0 = os.path.join(logfile_log_dir, logfile_name0)
logfile_path1 = os.path.join(logfile_log_dir, logfile_name1)
logfile_path2 = os.path.join(logfile_log_dir, logfile_name2)
logfile_path_error = os.path.join(logfile_log_dir, logfile_name_error)
logfile_path_count = os.path.join(logfile_log_dir, logfile_name_count)

# log配置字典
LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'default0': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path0,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'default1': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path1,  # 日志文件
            'maxBytes': 1024*1024*5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'default2': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path2,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'default3': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path_error,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'default4': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path_count,  # 日志文件
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {


        # logging.getLogger(__name__)拿到的logger配置
        'crawler_status': {
            'handlers': ['default0', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
        'data_filter': {
            'handlers': ['default1', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
        'upload_status': {
            'handlers': ['default2', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
        'error_collect': {
            'handlers': ['default3', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
        'item_count': {
            'handlers': ['default4', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}


def load_my_logging_cfg(type):
    logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(type)  # 生成一个log实例
    return logger
if __name__ == '__main__':
    """
    生成目录
    """
    logger = load_my_logging_cfg("")#不存在的key值来产生log文件
    logger.info("lin")

"""
- author : "leeyoung"
- email : "reusleeyoung@163.com"
- date   : "2017.9.20"
"""
#coding=utf-8

import logging

# 把error信息写入日志文件
class Logger():
    def __init__(self, logname, logger):
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.ERROR)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.ERROR)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)

    def getlog(self):
        return self.logger
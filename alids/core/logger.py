#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   alids\core\logger.py 
@Time    :   2022-01-22 18:15:50 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import os


class Logger(object):
    def __init__(self, log_path: str = os.path.dirname(__file__)):
        self.log_path = log_path
        self.runtime_log_path = os.path.join(log_path, 'runtime.log')
        self.error_log_path = os.path.join(log_path, 'error.log')

    def log(self, msg: str):
        with open(self.runtime_log_path, 'a') as f:
            f.write(msg + '\n')

    def error(self, msg: str):
        with open(self.error_log_path, 'a') as f:
            f.write(msg + '\n')
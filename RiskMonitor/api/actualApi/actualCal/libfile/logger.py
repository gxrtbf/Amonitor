#!/usr/bin/python
#coding=utf-8

import logging
import sys
import os

class Logger:        
    def __init__(self, logName, logFile):
        self._logger = logging.getLogger(logName)
        handler = logging.FileHandler(logFile)
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(name)s %(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        
    def log(self, msg, level='info'):
        if self._logger is not None:
            if level == 'warning':
                self._logger.warning(msg)
            else:
                self._logger.info(msg)
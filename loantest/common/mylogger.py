#-*-coding: UTF-8 -*-
'''
Created on 2019年9月26日
@author: LIJY
'''
import logging
from logging import Logger
from configparser import ConfigParser
import os


class DoneLogger(Logger):
    def __init__(self,name,cfg_file,section,logfile,level = logging.NOTSET):
        '''
        继承logger类，读取配置文件中的logger配置信息，直接初始化好logger,添加handler和设置日志级别
        '''
        super().__init__(name,level)  # 调用父类初始化方法
        cfg = ConfigParser()  
        self.section = section
        if not os.path.exists(logfile):
            os.mkdir(logfile)
        self.logfile = logfile

        cfg.read(cfg_file,encoding='utf-8')  # 读取配置文件
        
        # 新建filehandler:
        if cfg.getboolean(self.section, "file_logger_on"):    # 如果有设置filehandler则新建，添加到logger中
            file_handler = logging.FileHandler(self.logfile,encoding ='utf-8')
            file_handler.setLevel(cfg.getint(section, "file_level"))
            file_fmt = logging.Formatter(cfg.get(section, "file_fmt"))
            file_handler.setFormatter(file_fmt)
            self.addHandler(file_handler)
            
        # 新建consolhandler
        if cfg.getboolean(self.section, "consol_logger_on"):  # 如果设置有consolhandler则新建，添加到logger中
            consol_handler = logging.StreamHandler()
            consol_handler.setLevel(cfg.getint(section, "consol_level"))
            consol_fmt = logging.Formatter(cfg.get(section, "consol_fmt"))
            consol_handler.setFormatter(file_fmt)
            self.addHandler(consol_handler) 
        


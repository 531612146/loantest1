#-*-coding: UTF-8 -*-
'''
Created on 2019年10月11日
@author: LIJY
'''

import os
from common.ini_oper import IniRead
from common.mylogger import DoneLogger

class ConfFilePath:
    projectpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    datapath = os.path.join(projectpath,'data')
    loggerpath = os.path.join(projectpath,'log')
    confpath = os.path.join(projectpath,'conf')
    casepath = os.path.join(projectpath,'case')
    reportpath = os.path.join(projectpath,'report')
    
class ConfFile():
    conffile = os.path.join(ConfFilePath.confpath,'conf.ini')
    logger_conf_file = os.path.join(ConfFilePath.confpath,'logger.ini')
    testdatafile = os.path.join(ConfFilePath.confpath,'testdata.ini')
        
class MyLogger(DoneLogger):
    def __init__(self,name,section,logfilename,level=0):
        cfg_file = ConfFile.logger_conf_file
        logfile = os.path.join(ConfFilePath.loggerpath,logfilename)      
        super().__init__(name,cfg_file,section,logfile,level)
        
        
if __name__=='__main__':
    print(ConfFile.testdatafile)


  
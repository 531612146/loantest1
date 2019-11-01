#-*-coding: UTF-8 -*-
'''
Created on 2019年10月8日
@author: LIJY
'''

from conf import constant
from common import HTMLTestRunner
import unittest
from datetime import datetime
import os
from conf import constant

logger = constant.MyLogger("run_log","logger","log.txt")


class RunReport:
    def __init__(self,casepath,pattern,reportname):
        '''
        初始化case路径，案例格式，报告地址
        '''
        self.reportname = reportname
        self.loader = unittest.TestLoader()
        self.suite = self.loader.discover(casepath, pattern)  # 初始化的时候就加载好测试案例
    
    def runcase(self):
        '''
        把跑案例方法封装到一个方法里面
        '''
        # 生成文件名
        # 把reportname加上时间戳
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.reportname = os.path.join(constant.ConfFilePath.reportpath,(self.reportname+time))+'.html'
        
        with open(self.reportname,'wb') as f:
            runner = HTMLTestRunner.HTMLTestRunner(f, verbosity=2)
            runner.run(self.suite)
    
if __name__=='__main__':
    try:
        logger.info("初始化run...")
        run1 = RunReport(constant.ConfFilePath.casepath,'test*.py','loanrun')
        logger.info('初始化run结束...')
    except Exception as e:
        logger.error(str(e)+'****run初始化报错了****')
     
    logger.info("runcase开始...")
    try:
        run1.runcase()
    except Exception as e:
        print('******runcase报错了******',str(e))
    logger.info("...runcase运行结束...")
  
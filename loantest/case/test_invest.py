#-*-coding: UTF-8 -*-
'''
Created on 2019年10月29日
@author: LIJY
'''


from common import ddt
import unittest
from common.exceldata import Exceldata
from common.ini_oper import IniRead
from conf import constant
import os
from requests import Session
from middleware import db_handler
from common import random_num
import json
from func import loan_pre


logger = constant.MyLogger("case_log","logger","log.txt")

@ddt.ddt
class TestInvest(unittest.TestCase):
    # 从配置文件读取测试文件名和测试的sheet名称
    data_conf_file = constant.ConfFile.testdatafile
    data_file_path = constant.ConfFilePath.datapath
    data_file = IniRead(data_conf_file).get_section_option('loaninvest','filename')
    data_file = os.path.join(data_file_path,data_file)
    data_sheet = IniRead(data_conf_file).get_section_option('loaninvest', 'sheet')
    data = Exceldata(data_file).get_data(data_sheet)
    
    # 读取环境的url地址ip部分
    base_url = IniRead(data_conf_file).get_section_option('loaninvest', 'path') 
    
    @classmethod
    def setUpClass(cls):
        # 初始化Session请求
        cls.ssion = Session()
        cls.conn = db_handler.DbConnect('db')
          
    @classmethod
    def tearDownClass(cls):
        cls.ssion.close()
        cls.conn.close()


    @ddt.data(*data)
    def test_invest(self,row):
        # 读取每行数据的值
        url = (self.base_url + row['URL']).strip()
        headers = row['HEADERS']
        method = row['METHOD']
        data = row['DATA']
        expected = row['EXPECTED']      
        
        # label替换
        with loan_pre.Investlabel() as f:
            data = loan_pre.ReplaceLabel().replace_label(data, f)
        
        with loan_pre.Investlabel() as f:
            headers = loan_pre.ReplaceLabel().replace_label(headers, f)
        
        # 数据的格式转换
        
        data = json.loads(data)
        headers = eval(headers)
        expected = json.loads(expected)
        url.strip()
        
        # 发送http请求
        res = self.ssion.request(method=method, url = url, json = data, headers=headers)
        print('********res.json()********',res.json())
   
        try:
            self.assertEqual(expected['code'], res.json()['code'])
            if row['TITLE']=='投资金额超过loan剩余金额，投资失败':  
                self.assertRegex(res.json()['msg'], expected['msg'])
            else:
                self.assertEqual(expected['msg'], res.json()['msg'])   
        except Exception as e:
            logger.error(str(e)+'test失败了')
            raise e

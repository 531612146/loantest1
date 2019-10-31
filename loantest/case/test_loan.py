# #-*-coding: UTF-8 -*-
# '''
# Created on 2019年10月21日
# @author: LIJY
# '''
# from common import ddt
# import unittest
# from common.exceldata import Exceldata
# from common.ini_oper import IniRead
# from conf import constant
# import os
# from requests import Session
# from middleware import db_handler
# from common import random_num
# import json
# from func.loan_pre import GetToken
# 
# logger = constant.MyLogger("case_log","logger","log.txt")
# 
# 
# @ddt.ddt
# class TestWithdraw(unittest.TestCase):
#     # 从配置文件读取测试文件名和测试的sheet名称
#     data_conf_file = constant.ConfFile.testdatafile
#     data_file_path = constant.ConfFilePath.datapath
#     data_file = IniRead(data_conf_file).get_section_option('loanwithdraw','filename')
#     data_file = os.path.join(data_file_path,data_file)
#     data_sheet = IniRead(data_conf_file).get_section_option('loanwithdraw', 'sheet')
#     data = Exceldata(data_file).get_data(data_sheet)
#     
#     # 读取环境的url地址ip部分
#     base_url = IniRead(data_conf_file).get_section_option('loanwithdraw', 'path') 
#     
#     @classmethod
#     def setUpClass(cls):
#         cls.auth = 'Bearer '+GetToken().login()['token']
#         cls.member_id = GetToken().login()['id']
#         cls.mobile_phone = GetToken().data['mobile_phone']
#         
#         # 初始化Session请求
#         cls.ssion = Session()
#           
#     @classmethod
#     def tearDownClass(cls):
#         cls.ssion.close()
#         
# 
#     @ddt.data(*data)
#     def test_withdraw(self,row):
#         # 读取每行数据的值
#         url = (self.base_url + row['URL']).strip()
#         headers = eval(row['HEADERS'])
#         method = row['METHOD']
#         data = row['DATA']
#         expected = row['EXPECTED']
#         # 数据的格式转换
#         data = json.loads(row['DATA'])
#         headers['Authorization'] = self.auth
#         expected = json.loads(expected)
#         url.strip()
#          
#         # 进行数据库连接获取，获取余额
#         conn = db_handler.DbConnect('db')
#         sql_leaveamount = 'select leave_amount from member where id = %s'
#         sql_rand_id = 'select id from member order by rand() limit 1'
#         
#         # 发送http请求，发送之前查询余额
#         cursor = conn.execute(sql_leaveamount, self.member_id)
#         leave_amount = float(cursor.fetchall()[0]['leave_amount'])
# 
#         # 替换*member_id*
#         if '*member_id*' == data['member_id']:
#             data['member_id'] = str(self.member_id)
#         # 替换超额数据
#         if '*exceed_amount*' ==data['amount']:
#             data['amount'] = float(leave_amount)+1
#             
#         # 替换随机的用户
#         if '*rand_one*' == data['member_id']:
#             cursor = conn.execute(sql_rand_id)
#             rand_id = cursor.fetchall()[0]['id']           
#             data['member_id'] = str(rand_id)
# 
#         # 发送http请求
#         print('************data******',data,type(data))
#         res = self.ssion.request(method=method, url = url, json = data, headers=headers)
#         print('************res.json******',res.json())
#          
#         try:
#             self.assertEqual(expected['code'], res.json()['code'])
#             self.assertEqual(expected['msg'], res.json()['msg'])
#             
#             # 如果应答成功，检查应答信息里面的余额与数据库中的最新余额相等
#             if expected['code']==0:
#                 # 查询最新余额
#                 new_leave_amount = float(conn.execute(sql_leaveamount, self.member_id).fetchall()[0]['leave_amount'])
#                 self.assertEqual(leave_amount-data['amount'], new_leave_amount)
#                 self.assertEqual(res.json()['data']['leave_amount'],new_leave_amount)          
#         except Exception as e:
#             logger.error(str(e)+'test失败了')
#             raise e

        


# @ddt.ddt
# class TestRegister(unittest.TestCase):
#      # 从配置文件读取测试文件名和测试的sheet名称
#     data_conf_file = constant.ConfFile.testdatafile
#     data_file_path = constant.ConfFilePath.datapath
#     data_file = IniRead(data_conf_file).get_section_option('loanregister','filename')
#     data_file = os.path.join(data_file_path,data_file)
#     data_sheet = IniRead(data_conf_file).get_section_option('loanregister', 'sheet')
#     data = Exceldata(data_file).get_data(data_sheet)
#      
#     # 读取环境的url地址ip部分
#     base_url = IniRead(data_conf_file).get_section_option('loanregister', 'path')
#     
#      
#     @ddt.data(*data)
#     def test_register(self,row):
#         # 读取每行数据的值
#         url = self.base_url + row['URL']
#         headers = row['HEADERS']
#         method = row['METHOD']
#         data = row['DATA']
#         expected = row['EXPECTED']
#         
#         # 进行数据库连接获取，获取存在的手机号
#         conn = db_handler.DbConnect('db')
#         sql_if_phone_exist = 'select mobile_phone from member where mobile_phone = %s'
#         sql_one_exist_phone = 'select mobile_phone from member order by rand() limit 1'
# 
#         # 随机生成新手机号替换new_phone
#         if '*new_phone*' in row['DATA']:                   
#             while True:
#                 new_phone = random_num.rand_phone()
#                 # 查看随机生成号码有没有在数据库中
#                 cursor = conn.execute(sql_if_phone_exist, new_phone)
#                 res_new_phone = cursor.fetchall()
#                 if not res_new_phone: 
#                     row['DATA'] = row['DATA'].replace('*new_phone*',new_phone)
#                     print('***++++++++++++',row['DATA'])
#                     break                 
#                 else:
#                     continue
#                 
#         # 用已存在的phone替换existphone
#         if '*exist_phone*' in row['DATA']: 
#             cursor = conn.execute(sql_one_exist_phone)
#             res_exist_phone = cursor.fetchall()
#             exist_phone = res_exist_phone[0]['mobile_phone']
#             row['DATA'] = row['DATA'].replace('*exist_phone*',exist_phone)
# 
# #             
#         # 发送http请求
#         ssion = Session()
#         res = ssion.request(method=method, url =url, json = json.loads(row['DATA']), headers=eval(headers))
#         
#         try:
#             self.assertEqual(json.loads(expected)['code'], res.json()['code'])
#             self.assertEqual(json.loads(expected)['msg'], res.json()['msg'])
#             
#         except Exception as e:
#             logger.error(str(e)+'test失败了')
#             raise e
        


# @ddt.ddt
# class TestLogin(unittest.TestCase):
#     # 从配置文件中读取测试文件名和测试的sheet名称
#     data_conf_file = constant.ConfFile.testdatafile
#     data_file_path = constant.ConfFilePath.datapath
#     data_file = IniRead(data_conf_file).get_section_option('loanlogin','filename')
#     data_file = os.path.join(data_file_path,data_file)
#     data_sheet = IniRead(data_conf_file).get_section_option('loanlogin', 'sheet')
#     data = Exceldata(data_file).get_data(data_sheet)
#      
#     # 读取环境的url地址ip部分
#     base_url = IniRead(data_conf_file).get_section_option('loanlogin', 'path')
#      
#      
#     @ddt.data(*data)
#     def test_login(self,row):
#         # 读取每行数据的值
#         url = self.base_url + row['URL']
#         headers = row['HEADERS']
#         print(headers)
#         print(type(headers))
#         method = row['METHOD']
#         data = row['DATA']
#         expected = row['EXPECTED']
#  
#         # 发送http请求
#         ssion = Session()
#         res = ssion.request(method=method, url =url, json = row['DATA'], headers=headers)
#         print(res.json())
#  
#         try:
#             for i in expected:
#                 logger.debug('************测试数据******')
#                 logger.debug(str(i))
#                 self.assertEqual(res.json()[i],expected[i])
#         except Exception as e:
#             logger.error(str(e)+'test失败了')
#             raise e   
    
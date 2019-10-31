#-*-coding: UTF-8 -*-
'''
Created on 2019年10月24日
@author: LIJY
'''


from common.ini_oper import IniRead
from conf import constant
from requests import Session
from conf import constant
logger = constant.MyLogger("case_log","logger","log.txt")
import re
from middleware import db_handler


class ReplaceLabel:
    def replace_label(self,target,label):
        '''
        替换str中的**数据，
        '''
        partern = r'\*(.*?)\*'
        while re.search(partern,target):
            key = re.search(partern,target).group(1)
            value = getattr(label,key,'') 
            target = re.sub(partern,value,target,1)
        return target
    

class GetToken:
    
    data_conf_file = constant.ConfFile.testdatafile     
    data = eval(IniRead(data_conf_file).get_section_option('pre_login','data'))
    headers = eval(IniRead(data_conf_file).get_section_option('pre_login','headers'))
    method = IniRead(data_conf_file).get_section_option('pre_login','method')
    url = IniRead(data_conf_file).get_section_option('pre_login','url')
    
    def login(self):
        # 读取配置文件中的用户名和密码登录，返回id和token的字典
        session = Session()
        try:
            res = session.request(method=self.method, url=self.url, json=self.data,headers=self.headers)
            id_token = {}
            id_token['token'] = res.json()['data']['token_info']['token']
            id_token['id'] = res.json()['data']['id']
            session.close()
            return id_token
        except:
            logger.error("提前登陆获取token失败")
            session.close()
            
class Investlabel:
    
    def __enter__(self):
        self.conn = db_handler.DbConnect('db')
        self.sql_loan_id = "select id as loan_id from loan where status = '2'  order by create_time desc limit 1"
        self.token_id = GetToken().login()
        return self
    
    def __exit__(self,exc_type, exc_val, exc_tb):
        self.conn.close()

    
    @property
    def loan_id(self):
        cursor = self.conn.execute(self.sql_loan_id)
        cursor.close()        
        return str(cursor.fetchall()[0]['loan_id'])
    
    @property
    def member_id(self):
        return str(self.token_id['id'])
        
        
        
    @property   
    def Authorization(self):
        return 'Bearer ' + self.token_id['token']
    
    @property
    def rand_member_id(self):
        id = str(int(self.token_id['id'])-1)
        return id
    
    @property
    def loan_not_status2(self):
        sql_loan_wrong_status = "select id as loan_id from loan where status = '3'  order by create_time desc limit 1"
        cursor = self.conn.execute(sql_loan_wrong_status)
        cursor.close()        
        return str(cursor.fetchall()[0]['loan_id'])
    
    @property
    def full_amount(self):
        sql_full_amount = 'select((select amount from loan where id =%s)-(select sum(amount) from invest where loan_id = %s)) as full_amount'
        cursor = self.conn.execute(sql_full_amount,[self.loan_id,self.loan_id])
        cursor.close()
        return str(cursor.fetchall()[0]['full_amount'])


# class AddLoan:
#     data_conf_file = constant.ConfFile.testdatafile    
#     data = eval(IniRead(data_conf_file).get_section_option('createloan','data'))
#     headers = eval(IniRead(data_conf_file).get_section_option('createloan','headers'))
#     method = IniRead(data_conf_file).get_section_option('createloan','method')
#     url = IniRead(data_conf_file).get_section_option('createloan','url')
#     audit_url = IniRead(data_conf_file).get_section_option('createloan','audit_url')
#     audit_data = eval(IniRead(data_conf_file).get_section_option('createloan','audit_data'))
#       
#     # 登录获取token 并把token加到头部信息中
#     token = GetToken().login()
#     auth = 'Bearer ' + token['token']
#     headers['Authorization'] = auth
#     
#     def loan_audit(self,loan_id):
#         session = Session()
#         self.audit_data["loan_id"] = loan_id       
#         try:
#             res = session.request(method=self.method, url=self.audit_url, json=self.audit_data,headers=self.headers)
#             if res.json()["code"] !=0:
#                 logger.error("loan审核失败")               
#         except:
#             logger.error("loan审核失败")
# 
#     @property
#     def create_loan(self):
#         # 返回loanID str类型
#         session = Session()
#         try:
#             res = session.request(method=self.method, url=self.url, json=self.data,headers=self.headers)
#             loan_id = res.json()['data']['id']
#         except:
#             logger.error("前置处理创建loan失败")
#         # 创建完loan后直接审核
#         self.loan_audit(loan_id)
#         return loan_id



if __name__=='__main__':
#     print(type(GetToken().data))
#     print(GetToken().login())
    data = "{'member_id': '*member_id*', 'loan_id': '*loan_id*', 'amount': 50}"
    with Investlabel() as f:
        c = ReplaceLabel().replace_label(data, f)
        d = f.full_amount()
    print(type(d),d)
    
    
    







    
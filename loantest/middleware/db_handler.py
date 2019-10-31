#-*-coding: UTF-8 -*-
'''
Created on 2019年10月22日
@author: LIJY
'''

from common import db_handler
from conf import constant
from common import ini_oper
import pymysql
from pymysql.cursors import DictCursor 


class DbConnect(db_handler.DBConnect):
    '''
    获取配置文件中的信息
    '''
    def __init__(self,section):
        # 读取配置文件中对应的sectiond中的文件
        filepath = constant.ConfFile.testdatafile
        iniread = ini_oper.IniRead(filepath)
        self.host = iniread.get_section_option(section,'host')
        self.port = int(iniread.get_section_option(section,'port'))
        self.user = iniread.get_section_option(section,'user')
        self.password = iniread.get_section_option(section,'password')
        self.database = iniread.get_section_option(section,'database')
        # 初始化从配置文件中读取的数据             
        super().__init__(host=self.host,port=self.port,user=self.user,password=self.password,database=self.database)
        


if __name__=='__main__':
    # 测试一下功能是否正常
    conn = DbConnect('db')
    cursor = conn.execute('select mobile_phone from member')
    res = cursor.fetchall()
    print(res)
    from common import random_num
    
    new_phone = random_num.rand_phone()
    # 查看该号码有没有在数据库中
    sql_if_phone_exist = 'select mobile_phone from member where mobile_phone = %s'
    cursor = conn.execute(sql_if_phone_exist, new_phone)
    res = cursor.fetchall()
    print(res)
    if res:
        print('TRUE')
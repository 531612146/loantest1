#-*-coding: UTF-8 -*-
'''
Created on 2019年10月22日
@author: LIJY
'''

import pymysql
from pymysql.cursors import DictCursor 


class DBConnect:
    def __init__(self,host,user,password,database,charset='utf8',cursorclass=DictCursor,port=3306):
        self.conn = pymysql.connect(host=host,port=port,user=user,password=password,database=database,charset=charset,cursorclass=cursorclass )
        self.conn.autocommit(1)
        
    def close(self):
        # 断开连接
        self.conn.close()
       
    def execute(self,sql,args=None):
        '''
        输入sql语句，返回一个cursor
        '''
        # 新建游标
        cursor = self.conn.cursor()
        cursor.execute(sql,args)
        cursor.close()
        return cursor
        

if __name__=='__main__':
    conn = DBConnect(host='120.78.128.25',port=3306,user='future',password='123456',database='futureloan',charset='utf8',cursorclass=DictCursor)
    cursor = conn.execute('select * from loan')
    res = cursor.fetchone()
    print(res)
    res = cursor.fetchone()
    print(res)
    cursor = conn.execute('select * from loan limit 10')
    print(cursor.fetchall())
    
    sql = 'select * from loan where id = %s'
    cursor = conn.execute(sql,[1,])
    print('****',cursor.fetchall())
    



    
        
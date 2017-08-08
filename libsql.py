#!/usr/bin/python
#!-*-coding:utf-8-*-
'''
    Author:leo
    Date:2017/06/23
    Description:Python MYSQL Lib
    Note:SQL语句书写注意字符串中的单引号、反斜杠的转义
'''
'''
    ModifyDate:2017/07/04
    ModifyAuthor:leo
    Add:insert,delete,update,search
'''
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class mysql_lib:
    def __init__(self):
        self.conn = None
        self.sql_cursor = None
    def conn_db(self,host='127.0.0.1',port=3306,username='root',password='12345',dbname='admin'):
        try:
            self.conn = MySQLdb.connect(
                host=host,
                port=port,
                user=username,
                passwd=password,
                db=dbname,
                charset='utf8'
            )
            self.sql_cursor = self.conn.cursor()
        except Exception,e:
            return (1, str(e))
        else:
            return (0,'success')

    # 插入条目，成功，返回成功信息(0,'success')，失败，返回Exception信息
    def insert(self,sql):
        try:
            self.sql_cursor.execute(sql.encode('utf-8'))
        except Exception,e:
            return (1, str(e))
        else:
            self.conn.commit()
            return (0,'success')
    #查询条目，成功，返回条目，失败，返回Exception信息
    def search(self,sql):
        try:
            self.sql_cursor.execute(sql.encode('utf-8'))
        except Exception,e:
            return (1, str(e))
        else:
            #元组（）形式
            items = self.sql_cursor.fetchall()
            #cc = self.sql_cursor.rowcount
            return (0,items)
    def c_search(self,sql):
        try:
            self.sql_cursor.execute(sql.encode('utf-8'))
        except Exception,e:
            return (1, str(e))
        else:
            #元组（）形式
            #items = self.sql_cursor.fetchall()
            cc = self.sql_cursor.rowcount
            return (0,cc)
    def close_conn(self):
        self.sql_cursor.close()
        self.conn.commit()
        self.conn.close()
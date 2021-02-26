#coding=utf-8
'''
MySQLdb/pymysql模块
• MySQLdb/pymysql常用方法：
• MySQLdb.connect 建立和MySQL 数据库的连接
• cursor=conn.cursor() 通过上一步建立的连接获取个cursor对象
• cursor.execute（sql) 执行SQL 语句， 但返回结果不是SQL
执行的结果，是此SQL 执行后所影响的行数
• cursor.fetchall（）： 获取SQL 执行的所有结果，返回
结果是个嵌套的元组
• cursor.fetchall（）获取SQL 执行的结果，只获取第一条
• cursor.close() ， conn.close() ： 关闭连接和cursor
'''
import pymysql
#没有下载MydSQLdb
import time
import logging
import traceback
import urllib
class DBOperateAction():
    #初始化实例
    def __init__(self,dbhost,dbacount,dbpassword,dbname,port=3306,charset="utf8"):
        self.dbhost=dbhost
        self.dbacount=dbacount
        self.dbpassword=dbpassword
        self.dbname=dbname
        self.charset=charset
        self.port=port
        self.db_conn=""
        self.db_cursor=""#cursor对象
    #连接数据库
    def connect(self):
        try:
            self.db_conn=pymysql.connect(host=self.dbhost,user=self.dbacount,passwd=self.dbpassword,
                                         db=self.dbname,port=self.port,charset=self.charset)
            self.db_cursor=self.db_conn.cursor()#通过上一步建立的连接获取个cursor对象
            return True
        except pymysql.OperationalError:
            logging.error("连接失败失败失败败")
            logging.exception("exception message:")
            return False

    def re_connect(self):
        logging.error("连接到服务器失败 重连")
        try:
            self.db_conn=pymysql.connect(host=self.dbhost,user=self.dbacount,passwd=self.dbpassword,
                                         db=self.dbname,port=self.port,charset="utf8",connect_time=5)
            self.db_cursor=self.db_conn.cursor()
            return True
        except pymysql.OperationalError:
            logging.error("重连失败")
            return False
    def get_all_result(self,sql):
        try:
            #logging.info("Execute sql:"+sql)
            self.db_cursor.execute(sql)
            self.db_conn.commit()
            result=self.db_cursor.fetchall()
            return result
        except pymysql.OperationalError:
            for i in range(0,3):
                time.sleep(5)
                if self.re_connect():
                    logging.info("连接成功")
                    return False
        except pymysql.ProgrammingError:
            logging.exception("exception message:")
            return False
    def get_one_result(self,sql):
        try:
            #logging.info("execute sql:"+sql[:500])
            self.db_cursor.execute(sql)
            self.db_conn.commit()
            result = self.db_cursor.fetchall()
            return result
        except pymysql.OperationalError:
            traceback.print_exc()
            for i in range(0,3):
                time.sleep(5)
                if self.re_connect():
                    logging.info("连接成功")
                    self.db_cursor.fetchone()
                    logging.warn("重连成功警告")
            return False
    def close_connection(self):
        self.db_conn.close()

if __name__=="__main__":
    host="db1.kidaas.com"
    db_account="idaas"
    db_passwd="idaas123"
    db_name="policy_center_dev"

    db_operation=DBOperateAction(host,db_account,db_passwd,db_name,port=3306)
    db_operation.connect()
    select_sql="select * from TB_DEVICE where STATUS=2000 "
    print(select_sql)
    #results=db_operation.get_all_result(select_sql)
    results = db_operation.get_one_result(select_sql)
    db_operation.close_connection()
    print(len(results))
    # for item in results:
    #     for item2 in item:
    #         print(item2)
    print("**"*50)
    #print type(results)

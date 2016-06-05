#-*- coding: utf-8 -*-
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt",charset="utf8" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
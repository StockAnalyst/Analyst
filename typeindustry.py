#!usr/bin/python
#-*- coding: UTF-8 -*-
import timecheck
import checktddata
import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt",charset='utf8' )
cursor = db.cursor()

tradetime = timecheck.getweekday(todaydate,'1530')
tradetime = checktddata.check_mktequd(tradetime)


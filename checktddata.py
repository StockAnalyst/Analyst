#!/usr/bin/python
#-*- coding: UTF-8 -*-  
#检查数据库中是否有当日数据，若没有，获取（最多重复获取两次）。返回获取到的数据交易日期
import timecheck
import mkt
import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt",charset='utf8' )

cursor = db.cursor()
def check_mktequd(tradetime):
	#mkt_mktequd = `mkt_mktequd`
	cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd where tradeDate=%s
						""",(tradetime))
	counttoday,i = 0,0
	counttoday += cursor.rowcount
	print counttoday
	while (counttoday == 0 and i < 2):
		inputtradetime = timecheck.chgtimefor(tradetime)
		mkt.mktequd(inputtradetime)
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd where tradeDate=%s
						""",(tradetime))
		counttoday += cursor.rowcount
		#print counttoday
		if counttoday == 0 :
			tradetime = timecheck.getyesday(tradetime)
			cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd where tradeDate=%s
						""",(tradetime))
			if cursor.rowcount > 0:
				break			
		#print tradetime
		i += 1
	return tradetime

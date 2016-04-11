import his
import time
todaydate = time.strftime('%Y-%m-%d')
import datetime
now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_nyr = yes_time.strftime('%Y-%m-%d')
pre_yes_time = now_time + datetime.timedelta(days=-2)
pre_yes_time_nyr = pre_yes_time.strftime('%Y-%m-%d')

import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_equ",charset='utf8' )
dbmkt = MySQLdb.connect("127.0.0.1","root","root","db_mkt",charset='utf8' )
cursor = db.cursor()
curmkt = dbmkt.cursor()

def getrealtimetick():
	cursor.execute("""select code from tb_list limit 30""")

	codelist = cursor.fetchall()

	for i in codelist:
		#print i[0]
		his.realtimetick(i[0])

def getweekday(uptime):
	tradetime = uptime
	a = time.localtime()
	weekday = time.strftime("%w",a)
		
	if weekday == '6':
		tradetime = yes_time_nyr
	elif weekday == '0':
		tradetime = pre_yes_time_nyr
	return tradetime

def ifgetrealtimetick():
	tradetime = getweekday(todaydate)
	if (tradetime != todaydate):	
		sql = """create table temp_id as (select distinct(date) from tb_tickrealtime)
		"""
		curmkt.execute(sql)
		count = curmkt.execute('show columns from temp_id like %s',(tradetime))
		if count == 0:
			getrealtimetick()
		sql = """
				drop table temp_id
		"""
		curmkt.execute(sql)
	else:
		getrealtimetick()
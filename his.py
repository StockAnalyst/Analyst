#-*- coding: UTF-8 -*-  
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
from sqlalchemy import create_engine
import tushare as  ts
engine = create_engine('mysql://root:root@127.0.0.1/db_mkt?charset=utf8')
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
#获取个股历史交易数据（包括均线数据）,数据类型，默认D=日k线 
#df = ts.get_h_data(ktype='D')
def hist(code):
	#df = ts.get_hist_data('sh')
	df = ts.get_hist_data(code)
	df.insert(0,'uploadtime',nowtime)
	df.insert(0,'code',code)
	#df.insert(0,'index',1)
	#df.set_index('index')
	#df.to_excel('E:/Anaconda/getdata/hissh1.xlsx')
	df.to_sql('mkt_his',engine,if_exists='append')
#hist('000001')

#大盘指数的全部历史数据(去年今日到今日)
def histindex(code):
	dfindex = ts.get_h_data(code,index = True)
	dfindex.insert(0,'uploadtime',nowtime)
	dfindex.insert(0,'code',code)
	
	def insertidindex():
		sql = """ALTER TABLE mkt_histindex 
				ADD histindex_id int(20) not null auto_increment ,
				ADD primary key (histindex_id)"""
		cursor.execute(sql)
	counttb = cursor.execute('show tables like \'mkt_histindex\'') 
	if counttb == 0:
		dfindex.to_sql('mkt_histindex',engine)
		countindex = cursor.execute('show columns from mkt_histindex like \'histindex_id\'') 
		if countindex == 0:
			insertidindex()
	else:
		dfindex.to_sql('mkt_histindex',engine,if_exists='append')

#histindex('399106')

#获取历史复权数据，分为前复权和后复权数据，接口提供股票上市以来所有历史数据，
#默认为前复权。如果不设定开始和结束日期，则返回近一年的复权数据
#autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
def histfuquan(code,autype):
	dffq = ts.get_h_data(code,autype = autype)
	dffq.insert(0,'uploadtime',nowtime)
	dffq.insert(0,'code',code)
	dffq.to_sql('mkt_histfuquan',engine,if_exists='append')
	def insertidfq():
		sql = """ALTER TABLE mkt_histfuquan 
				ADD histfq_id int(20) not null auto_increment ,
				ADD primary key (histfq_id)"""
		cursor.execute(sql)
	countfq = cursor.execute('show columns from mkt_histfuquan like \'histfq_id\'') 
	if countfq == 0:
		insertidfq()

#histfuquan('002337','')

#获取个股以往交易历史的分笔数据明细，通过分析分笔数据，
#可以大致判断资金的进出情况
#code：股票代码，即6位数字代码
#date：日期，格式YYYY-MM-DD
def insertidtick():
	sql = """ALTER TABLE mkt_tick 
			ADD tick_id int(20) not null auto_increment ,
			ADD primary key (tick_id)"""
	cursor.execute(sql)
def tick(code,date):
	dftick = ts.get_tick_data(code,date=date)
	dftick.insert(0,'uploadtime',nowtime)
	dftick.insert(0,'code',code)
	dftick.to_sql('mkt_tick',engine,if_exists='append')
	
	counttick = cursor.execute('show columns from mkt_tick like \'tick_id\'') 
	if counttick == 0:
		insertidtick()

def ticktoday(code):
	dftick = ts.get_today_ticks(code)
	dftick.insert(0,'uploadtime',nowtime)
	dftick.insert(0,'code',code)
	dftick.to_sql('mkt_tick',engine,if_exists='append')
	counttick = cursor.execute('show columns from mkt_tick like \'tick_id\'') 
	if counttick == 0:
		insertidtick()

#ticktoday('601333')

#获取实时分笔数据，可以实时取得股票当前报价和成交信息
#参数6位数字股票代码，或者指数代码（sh=上证指数 sz=深圳成指 hs300=沪深300指数
# sz50=上证50 zxb=中小板 cyb=创业板） 可输入的类型：str、list、set或者pandas的Series对象
def realtimetick(code):
	df = ts.get_realtime_quotes(code)
	df.insert(0,'uploadtime',nowtime)
	#df.insert(0,'code',code)
	df.to_sql('mkt_tickrealtime',engine,if_exists='append')
	def insertid():
		sql = """ALTER TABLE mkt_tickrealtime 
				ADD realtimetick_id int(20) not null auto_increment ,
				ADD primary key (realtimetick_id)"""
		cursor.execute(sql)
	countfq = cursor.execute('show columns from mkt_tickrealtime like \'realtimetick_id\'') 
	if countfq == 0:
		insertid()
	
	sql = """create table temp_id as (select realtimetick_id, code,date,time,count(distinct code,date,time) from mkt_tickrealtime group by code,date,time)
		"""
	cursor.execute(sql)
	sql = """
				delete from mkt_tickrealtime where realtimetick_id not in(select realtimetick_id from temp_id)
		"""
	cursor.execute(sql)
	sql = """
				drop table temp_id
		"""
	cursor.execute(sql)
	'''sql = """
				delete from mkt_tickrealtime where time>'15:10:00'
		"""
	cursor.execute(sql)'''
#realtimetick(['sh','sz','hs300','sz50','zxb','cyb'])
#获取实时指数：

#上证指数
#ts.get_realtime_quotes('sh')
#上证指数 深圳成指 沪深300指数 上证50 中小板 创业板
#ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])
#或者混搭
#ts.get_realtime_quotes(['sh','600848'])
#realtimetick('000001')
'''
指数k线数据：
ts.get_hist_data('sh'）#获取上证指数k线数据，其它参数与个股一致，下同
ts.get_hist_data('sz'）#获取深圳成指k线数据
ts.get_hist_data('hs300'）#获取沪深300指数k线数据
ts.get_hist_data('sz50'）#获取上证50指数k线数据
ts.get_hist_data('zxb'）#获取中小板指数k线数据
ts.get_hist_data('cyb'）#获取创业板指数k线数据
'''
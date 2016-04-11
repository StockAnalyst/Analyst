#-*- coding: UTF-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from sqlalchemy import create_engine
import tushare as ts
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_mkt?charset=utf8')
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
fd = ts.Fund()
#Fund(self, etfLof='', listStatusCd='', secID='', ticker='', category='', operationMode='', field=''):
#获取基金的基本档案信息，包含基金名称、交易代码、分级情况、所属类别、保本情况、上市信息、相关机构、投资描述等信息。
#收录了2005年以来的历史数据，数据更新频率为不定期。
#etfLof: ETF或LOF型基金
def fund():
	global dfetf
	global dflof
	dfetf = fd.Fund(etfLof='ETF',field='')
	dfetf.insert(0,'uploadtime',nowtime)
	dflof = fd.Fund(etfLof='LOF',field='')
	dflof.insert(0,'uploadtime',nowtime)
	fund_tosql()
#dflof.drop('9',errors='ignore')
#lof数据插入数据库过程中编码格式出错。。。。
#dflof.to_excel('C:/Users/xiaoya/Anaconda/getdata/fundlof2.xlsx')


# 创建数据表SQL语句,添加主键id
def insertid():
	sql = """ALTER TABLE fund_fund 
			ADD fund_id int(20) not null auto_increment ,
			ADD primary key (fund_id)"""
	cursor.execute(sql)
def createtb():
	dfetf.to_sql('fund_fund',engine)
	#dflof.to_sql('fund_fund',engine)
	count = cursor.execute('show columns from fund_fund like \'fund_id\'') 
	if count == 0:
		insertid()
def fund_tosql():
	counttb = cursor.execute('show tables like \'fund_fund\'') 
	if counttb == 0:
		createtb()
	else:
		dfetf.to_sql('fund_fund',engine,if_exists='append')
		#dflof.to_sql('fund_fund',engine,if_exists='append')
		sql = """create table temp_id as (select fund_id, ticker, count(distinct ticker) from fund_fund group by ticker)
		"""
		cursor.execute(sql)
		sql = """
				delete from fund_fund where fund_id not in(select fund_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)



todaydate = time.strftime('%Y%m%d')
import datetime
now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_nyr = yes_time.strftime('%Y%m%d')
#FundNav(self, dataDate='', secID='', ticker='', beginDate='', endDate='', field=''):
#获取某只基金的历史净值数据(货币型、短期理财债券型除外),包括了单位份额净值、累计净值与复权净值。
#收录了2005年以来的历史数据，数据更新频率为日。不输入日期则默认获取近一年以来的历史数据。
#dfnav = fd.FundNav(dataDate='20151107',field='')
def fundnav(update):
	global dfnav
	dfnav = fd.FundNav(dataDate=update,field='')
	#dfnav = fd.FundNav(dataDate=yes_time_nyr,field='')
	dfnav.insert(0,'uploadtime',nowtime)
	fundnav_tosql()

# 创建数据表SQL语句,添加主键id
def insertidnav():
	sql = """ALTER TABLE fund_fundnav 
			ADD fundnav_id int(20) not null auto_increment ,
			ADD primary key (fundnav_id)"""
	cursor.execute(sql)
def createtbnav():
	dfnav.to_sql('fund_fundnav',engine)
	count = cursor.execute('show columns from fund_fundnav like \'fundnav_id\'') 
	if count == 0:
		insertidnav()
def fundnav_tosql():
	counttbnav = cursor.execute('show tables like \'fund_fundnav\'') 
	if counttbnav == 0:
		createtbnav()
	else:
		dfnav.to_sql('fund_fundnav',engine,if_exists='append')
		sql = """create table temp_id as (select fundnav_id, ticker, count(distinct ticker,endDate) from fund_fundnav group by ticker,endDate)
		"""
		cursor.execute(sql)
		sql = """
				delete from fund_fundnav where fundnav_id not in(select fundnav_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)
		'''
		#dfnav.to_sql('fund_fundnav',engine,if_exists='append')
		sql = """create table temp_date as (select distinct endDate from fund_fundnav)
		"""
		cursor.execute(sql)
		countdate = cursor.execute('select * from temp_date where endDate=\'2015-11-05\'')
		if countdate = 0:
			dfnav.to_sql('fund_fundnav',engine,if_exists='append')
			
		else
			sql = """create table temp_id as (select fundnav_id, ticker, count(distinct ticker,endDate) from fund_fundnav group by ticker,endDate)
			"""
			cursor.execute(sql)
			sql = """
					delete from fund_fundnav where fundnav_id not in(select fundnav_id from temp_id)
			"""
			cursor.execute(sql)
			sql = """
					drop table temp_id
			"""
			cursor.execute(sql)
		sql = """
					drop table temp_date
			"""
			cursor.execute(sql)
			'''


#FundDivm(self, dataDate='', secID='', ticker='', beginDate='', endDate='', field=''):
#获取某只货币型基金或短期理财债券型基金的历史收益情况，包含了每万份收益，七日年化收益率等信息。
#收录了2005年以来的历史数据，数据更新频率为日。不输入日期则默认获取近一年以来的历史数据。
def funddivm(update):
	global dfdivm
	dfdivm = fd.FundDivm(dataDate=update,field='')
	#dfdivm = fd.FundDivm(dataDate=yes_time_nyr,field='')
	dfdivm.insert(0,'uploadtime',nowtime)
	funddivm_tosql()

# 创建数据表SQL语句,添加主键id
def insertiddivm():
	sql = """ALTER TABLE fund_funddivm 
			ADD funddivm_id int(20) not null auto_increment ,
			ADD primary key (funddivm_id)"""
	cursor.execute(sql)
def createtbdivm():
	dfdivm.to_sql('fund_funddivm',engine)
	count = cursor.execute('show columns from fund_funddivm like \'funddivm_id\'') 
	if count == 0:
		insertiddivm()
def funddivm_tosql():
	counttbdivm = cursor.execute('show tables like \'fund_funddivm\'') 
	if counttbdivm == 0:
		createtbdivm()
	else:
		dfdivm.to_sql('fund_funddivm',engine,if_exists='append')
		sql = """create table temp_id as (select funddivm_id, ticker, count(distinct ticker,endDate) from fund_funddivm group by ticker,endDate)
		"""
		cursor.execute(sql)
		sql = """
				delete from fund_funddivm where funddivm_id not in(select funddivm_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)



#FundAssets(self, reportDate='', secID='', ticker='', beginDate='', endDate='', field=''):
#获取基金定期披露的资产配置情况，包含了资产总值、资产净值，以及资产总值中权益类、固定收益类、现金及其他四种资产的市值与占比情况。
#收录了2005年以来的历史数据，数据更新频率为季度。获取方式支持：
#1）输入一个或多个secID/ticker，并输入beginDate和endDate，可以查询到指定基金，一段时间的资产配置；
#2）输入reportDate,不输入其他参数，可以查询到输入日期的全部基金资产配置
def fundassets():
	global dfassets
	dfassets = fd.FundAssets(reportDate='20141231',field='')
	dfassets.insert(0,'uploadtime',nowtime)
	fundassets_tosql()

# 创建数据表SQL语句,添加主键id
def insertidassets():
	sql = """ALTER TABLE fund_fundassets 
			ADD fundassets_id int(20) not null auto_increment ,
			ADD primary key (fundassets_id)"""
	cursor.execute(sql)
def createtbassets():
	dfassets.to_sql('fund_fundassets',engine)
	count = cursor.execute('show columns from fund_fundassets like \'fundassets_id\'') 
	if count == 0:
		insertidassets()
def fundassets_tosql():
	counttbassets = cursor.execute('show tables like \'fund_fundassets\'') 
	if counttbassets == 0:
		createtbassets()
	else:
		dfassets.to_sql('fund_fundassets',engine,if_exists='append')
		sql = """create table temp_id as (select fundassets_id, ticker, count(distinct ticker,reportDate) from fund_fundassets group by ticker,reportDate)
		"""
		cursor.execute(sql)
		sql = """
				delete from fund_fundassets where fundassets_id not in(select fundassets_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)


#FundHoldings(self, reportDate='', secID='', ticker='', beginDate='', endDate='', secType='', field=''):
#获取基金定期披露的持仓明细，包含所持有的股票、债券、基金的持仓明细数据。收录了2005年以来的历史数据，数据更新频率为季度。获取方式支持：
#1）输入一个或多个secID/ticker，并输入beginDate和endDate，可以查询到指定基金，一段时间的基金持仓；
#2）输入reportDate,不输入其他参数，可以查询到输入日期的全部基金持仓数据。
def fundholdings():
	global dfholdings
	dfholdings = fd.FundHoldings(reportDate='20141231',field='')
	dfholdings.insert(0,'uploadtime',nowtime)
	fundholdings_tosql()

# 创建数据表SQL语句,添加主键id
def insertidholdings():
	sql = """ALTER TABLE fund_fundholdings 
			ADD fundholdings_id int(20) not null auto_increment ,
			ADD primary key (fundholdings_id)"""
	cursor.execute(sql)
def createtbholdings():
	dfholdings.to_sql('fund_fundholdings',engine)
	count = cursor.execute('show columns from fund_fundholdings like \'fundholdings_id\'') 
	if count == 0:
		insertidholdings()
def fundholdings_tosql():
	counttbholdings = cursor.execute('show tables like \'fund_fundholdings\'') 
	if counttbholdings == 0:
		createtbholdings()
	else:
		dfholdings.to_sql('fund_fundholdings',engine,if_exists='append')
		sql = """create table temp_id as (select fundholdings_id, ticker, count(distinct ticker,reportDate) from fund_fundholdings group by ticker,reportDate)
		"""
		cursor.execute(sql)
		sql = """
				delete from fund_fundholdings where fundholdings_id not in(select fundholdings_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)



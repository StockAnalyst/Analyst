#-*- coding: UTF-8 -*-  

from sqlalchemy import create_engine
import tushare as ts
import time
import timecheck
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_mkt?charset=utf8')
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

todaydate = time.strftime('%Y-%m-%d')
a = time.localtime()
now_hm = time.strftime("%H%M",a)
nowhm = time.strftime("%H:%M",a)
st = ts.Market()
#沪深股票日线行情
#MktEqud(self, secID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#获取沪深AB股日行情信息，默认日期区间是过去1年，包含昨收价、开盘价、最高价、最低价、收盘价、成交量、成交金额等字段，每日15:30更新

def mktequd(update):
	global df
	df = st.MktEqud(tradeDate=update,field='')
	#df = st.MktEqud(tradeDate='20151110',field='')
	df.insert(0,'uploadtime',nowtime)
	mktequd_tosql()
	'''
#df = st.MktEqud(tradeDate=yes_time_nyr,field='')
df = st.MktEqud(tradeDate='20151110',field='')
df.insert(0,'uploadtime',nowtime)
mktequd_tosql()'''
#期货日线行情
#MktFutd(self, secID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#获取四大期货交易所期货合约、上海黄金交易所黄金(T+D)、白银(T+D)以及国外主要期货连续合约行情信息。 默认日期区间是过去一年。日线数据第一次更新为交易结束后（如遇线路不稳定情况数据可能存在误差），第二次更新为18:00pm，其中主力合约是以连续三个交易日持仓量最大为基准计算的。
def mktfutd(update):
	global dffutd
	dffutd = st.MktFutd(tradeDate=update,field='')
	#dffutd = st.MktFutd(tradeDate='20151110',field='')
	dffutd.insert(0,'uploadtime',nowtime)
	mktfutd_tosql()
#指数日线行情
#MktIdxd(self, indexID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#获取指数日线行情信息，包含昨收价、开盘价、最高价、最低价、收盘价、成交量、成交金额等字段，默认日期区间是过去1年，其中沪深指数行情每日15:30更新。
def mktidxd(update):
	global dfidxd
	dfidxd = st.MktIdxd(tradeDate=update,field='')
	#dfidxd = st.MktIdxd(tradeDate='20151110',field='')
	dfidxd.insert(0,'uploadtime',nowtime)
	mktidxd_tosql()

#沪深大宗交易
#MktBlockd(self, secID='', ticker='', tradeDate='', assetClass='', beginDate='', endDate='', field=''):
#获取沪深交易所交易日大宗交易成交价，成交量等信息。
def mktblockd(update):
	global dfblockd
	dfblockd = st.MktBlockd(tradeDate=update,field='')
	#dfblockd = st.MktBlockd(tradeDate='20151110',field='')
	dfblockd.insert(0,'uploadtime',nowtime)
	mktblockd_tosql()

#债券回购交易日行情
#MktRepod(self, secID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#获取债券回购交易开、收、高、低，成交等日行情信息，每日16:00前更新
def mktrepod(update):
	global dfrepod
	dfrepod = st.MktRepod(tradeDate=update,field='')
	#dfrepod = st.MktRepod(tradeDate='20151110',field='')
	dfrepod.insert(0,'uploadtime',nowtime)
	mktrepod_tosql()
#债券日行情
#MktBondd(self, secID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#获取债券交易开、收、高、低，成交等日行情信息，每日16:00前更新
def mktbondd(update):
	global dfbondd
	dfbondd = st.MktBondd(tradeDate=update,field='')
	#dfbondd = st.MktBondd(tradeDate='20151110',field='')
	dfbondd.insert(0,'uploadtime',nowtime)
	mktbondd_tosql()
#港股日行情
#MktHKEqud(self, secID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#获取香港交易所股票开、收、高、低，成交等日行情信息，每日17:00前更新
'''def mkthkequd(update):
	global dfhkequd
	dfhkequd = st.MktHKEqud(tradeDate=update,field='')
	#dfhkequd = st.MktHKEqud(tradeDate='20151110',field='')
	dfhkequd.insert(0,'uploadtime',nowtime)
	mkthkequd_tosql()
	'''
#基金日行情
#MktFundd(self, secID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#获取基金买卖交易开、收、高、低，成交等日行情信息，每日16:00前更新。
def mktfundd(update):
	global dffundd
	dffundd = st.MktFundd(tradeDate=update,field='')
	'''if dffundd.empty:
		intupdate = int(update)
		update = str(intupdate - 1)
		dffundd = st.MktFundd(tradeDate=update,field='')'''
	#dffundd = st.MktFundd(tradeDate='20151110',field='')
	dffundd.insert(0,'uploadtime',nowtime)
	mktfundd_tosql()
#期权日行情
# MktOptd(self, optID='', secID='', ticker='', tradeDate='', beginDate='', endDate='', field=''):
#主要记录上交所期权行情，包含昨结算、昨收盘、开盘价、最高价、最低价、收盘价、结算价、成交量、成交金额、持仓量等字段，每日16:00前更新。
def mktoptd(update):
	global dfoptd
	dfoptd = st.MktOptd(tradeDate=update,field='')
	#dfoptd = st.MktOptd(tradeDate='20151110',field='')
	dfoptd.insert(0,'uploadtime',nowtime)
	mktoptd_tosql()
#实时行情，一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
def mktall(update):
	global dfall
	dfall = ts.get_today_all()
	dfall.insert(0,'uploadtime',nowtime)
	mktall_tosql()
#大盘指数实时行情列表
def mktindex(update):
	#dfindex = ts.get_index()
	inputtradetime = timecheck.getweekday(update,'0930')
	
	def inserttable(dfindex,hm):
		dfindex.insert(0,'uploadtime',nowtime)
		dfindex.insert(1,'tradeDate',inputtradetime)
		dfindex.insert(2,'tradeTimehm',hm)
		def insertidindex():
			sql = """ALTER TABLE mkt_mktindex 
					ADD mktindex_id int(20) not null auto_increment ,
					ADD primary key (mktindex_id)"""
			cursor.execute(sql)
		countindex = cursor.execute('show columns from mkt_mktindex like \'mktindex_id\'') 
		if countindex == 0:
			insertidindex()
		else:
			dfindex.to_sql('mkt_mktindex',engine,if_exists='append')
	
	#timeArray = time.strptime(tradetime,'%Y%m%d')
	#inputtradetime = time.strftime('%Y-%m-%d',timeArray)
	def notrealdata():
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktindex group by tradeDate order by tradeDate desc
						""")
		tradetimesql = cursor.fetchone()
		count = cursor.rowcount
		if count == 0:
			dfindex = ts.get_index()
			inserttable(dfindex,'15:00')
		elif inputtradetime != tradetimesql[0]:
			dfindex = ts.get_index()
			#dfindex.insert(2,'tradeTimehm','15:00')
			inserttable(dfindex,'15:00')
		
		#print "notreal"
	def notrealdatanoon():
		cursor.execute("""SELECT distinct(tradeTimehm) FROM mkt_mktindex where tradeDate=%s order by tradeTimehm desc
						""",(inputtradetime))
		tradetimesql = cursor.fetchone()
		count = cursor.rowcount
		print count
		print tradetimesql[0]
		if count == 0:
			dfindex = ts.get_index()
			inserttable(dfindex,'11:30')
		elif(tradetimesql[0] !='11:30'):
			dfindex = ts.get_index()
			inserttable(dfindex,'11:30')
			
	def notrealdatanight():
		cursor.execute("""SELECT distinct(tradeTimehm) FROM mkt_mktindex where tradeDate=%s order by tradeTimehm desc
						""",(inputtradetime))
		tradetimesql = cursor.fetchone()
		print tradetimesql[0]
		count = cursor.rowcount
		if count == 0:
			dfindex = ts.get_index()
			inserttable(dfindex,'15:00')
		if(tradetimesql[0] !='15:00'):
			dfindex = ts.get_index()
			#dfindex.insert(2,'tradeTimehm','15:00')
			inserttable(dfindex,'15:00')
			
	def realdata():
		dfindex = ts.get_index()
		#dfindex.insert(2,'tradeTimehm',nowhm)
		inserttable(dfindex,nowhm)
		#print "real"

	if inputtradetime == todaydate:
		start_hm_a = '0830'
		end_hm_a = '1130'
		start_hm_p = '1300'
		end_hm_p = '1500'
		#中午休市时间
		if(timecheck.compare_hourmin(now_hm,end_hm_a,start_hm_p)):
			notrealdatanoon()
		#开市时间
		elif(timecheck.compare_hourmin(now_hm,start_hm_a,end_hm_a) or timecheck.compare_hourmin(now_hm,start_hm_p,end_hm_p)):
			realdata()
		#晚上停市时间
		#if(int(now_hm) > int(end_hm_p)):
		else:
			notrealdatanight()
	else:
		notrealdata()


'''
# 创建数据表SQL语句,添加主键id
def insertid(tbname,idname):
	sql = """ALTER TABLE '%s' 
			ADD '%s' bigint(20) not null auto_increment ,
			ADD primary key ('%s')""" %(tbname,idname,idname)
	cursor.execute(sql)
def ifinsertid(tbname,idname):
	count = cursor.execute('show columns from \'%s\' like \'\'%s\'\'') %(tbname,idname)
	if count == 0:
		insertid()

'''
def mktequd_tosql():
	df.to_sql('mkt_mktequd',engine,if_exists='append')
	#print "over1"
	def insertid():
		sql = """ALTER TABLE mkt_mktequd 
				ADD mktequd_id int(20) not null auto_increment ,
				ADD primary key (mktequd_id)"""
		cursor.execute(sql)

	count = cursor.execute('show columns from mkt_mktequd like \'mktequd_id\'') 
	if count == 0:
		insertid()
	'''	
	sql = """create table temp_id as (select mktequd_id, ticker,tradeDate, count(distinct ticker,tradeDate) from mkt_mktequd group by ticker,tradeDate)
		"""
	cursor.execute(sql)
	sql = """
				delete from mkt_mktequd where mktequd_id not in(select mktequd_id from temp_id)
		"""
	cursor.execute(sql)
	sql = """
				drop table temp_id
		"""
	cursor.execute(sql)
	'''	

def mktfutd_tosql():
	dffutd.to_sql('mkt_mktfutd',engine,if_exists='append')
	def insertidfutd():
		sql = """ALTER TABLE mkt_mktfutd 
				ADD mktfutd_id int(20) not null auto_increment ,
				ADD primary key (mktfutd_id)"""
		cursor.execute(sql)

	countfutd = cursor.execute('show columns from mkt_mktfutd like \'mktfutd_id\'') 
	if countfutd == 0:
		insertidfutd()
#ifinsertid('mkt_mktfutd','mktfutd_id')
def mktidxd_tosql():
	dfidxd.to_sql('mkt_mktidxd',engine,if_exists='append')
	def insertididxd():
		sql = """ALTER TABLE mkt_mktidxd 
				ADD mktidxd_id int(20) not null auto_increment ,
				ADD primary key (mktidxd_id)"""
		cursor.execute(sql)

	countidxd = cursor.execute('show columns from mkt_mktidxd like \'mktidxd_id\'') 
	if countidxd == 0:
		insertididxd()
#ifinsertid('mkt_mktidxd','mktidxd_id')
def mktblockd_tosql():
	dfblockd.to_sql('mkt_mktblockd',engine,if_exists='append')
	def insertidblockd():
		sql = """ALTER TABLE mkt_mktblockd 
				ADD mktblockd_id int(20) not null auto_increment ,
				ADD primary key (mktblockd_id)"""
		cursor.execute(sql)

	countblockd = cursor.execute('show columns from mkt_mktblockd like \'mktblockd_id\'') 
	if countblockd == 0:
		insertidblockd()
#ifinsertid('mkt_mktblockd','mktblockd_id')
def mktrepod_tosql():
	dfrepod.to_sql('mkt_mktrepod',engine,if_exists='append')
	def insertidrepod():
		sql = """ALTER TABLE mkt_mktrepod 
				ADD mktrepod_id int(20) not null auto_increment ,
				ADD primary key (mktrepod_id)"""
		cursor.execute(sql)

	countrepod = cursor.execute('show columns from mkt_mktrepod like \'mktrepod_id\'') 
	if countrepod == 0:
		insertidrepod()
#ifinsertid('mkt_mktrepod','mktrepod_id')
def mktbondd_tosql():
	dfbondd.to_sql('mkt_mktbondd',engine,if_exists='append')
	def insertidbondd():
		sql = """ALTER TABLE mkt_mktbondd 
				ADD mktbondd_id int(20) not null auto_increment ,
				ADD primary key (mktbondd_id)"""
		cursor.execute(sql)

	countbondd = cursor.execute('show columns from mkt_mktbondd like \'mktbondd_id\'') 
	if countbondd == 0:
		insertidbondd()
#ifinsertid('mkt_mktbondd','mktbondd_id')

def mktall_tosql():
	dfall.to_sql('mkt_mktall',engine,if_exists='append')
	def insertidall():
		sql = """ALTER TABLE mkt_mktall 
				ADD mktall_id int(20) not null auto_increment ,
				ADD primary key (mktall_id)"""
		cursor.execute(sql)

	countall = cursor.execute('show columns from mkt_mktall like \'mktall_id\'') 
	if countall == 0:
		insertidall()
#ifinsertid('mkt_mktall','mktall_id')
def mktfundd_tosql():
	dffundd.to_sql('mkt_mktfundd',engine,if_exists='append')
	def insertidfundd():
		sql = """ALTER TABLE mkt_mktfundd 
				ADD mktfundd_id int(20) not null auto_increment ,
				ADD primary key (mktfundd_id)"""
		cursor.execute(sql)

	countfundd = cursor.execute('show columns from mkt_mktfundd like \'mktfundd_id\'') 
	if countfundd == 0:
		insertidfundd()
#ifinsertid('mkt_mktfundd','mktfundd_id')
def mktoptd_tosql():
	dfoptd.to_sql('mkt_mktoptd',engine,if_exists='append')
	def insertidoptd():
		sql = """ALTER TABLE mkt_mktoptd 
				ADD mktoptd_id int(20) not null auto_increment ,
				ADD primary key (mktoptd_id)"""
		cursor.execute(sql)

	countoptd = cursor.execute('show columns from mkt_mktoptd like \'mktoptd_id\'') 
	if countoptd == 0:
		insertidoptd()
#ifinsertid('mkt_mktoptd','mktoptd_id')


#获取失败
'''
def mkthkequd_tosql():
	dfhkequd.to_sql('mkt_mkthkequd',engine,if_exists='append')
	def insertidequd():
		sql = """ALTER TABLE mkt_mkthkequd 
				ADD mkthkequd_id int(20) not null auto_increment ,
				ADD primary key (mkthkequd_id)"""
		cursor.execute(sql)

	countequd = cursor.execute('show columns from mkt_mkthkequd like \'mkthkequd_id\'') 
	if countequd == 0:
		insertidequd()
#ifinsertid('mkt_mkthkequd','mkthkequd_id')
'''

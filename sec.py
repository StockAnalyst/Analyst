#-*- coding: UTF-8 -*-  

from sqlalchemy import create_engine
import tushare as ts
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_sec?charset=utf8')
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_sec" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

mt = ts.Master()

#证券编码及基本上市信息。。不同证券类型数据分别获取
#SecID(self, assetClass='', cnSpell='', partyID='', ticker='', field='')
def secid():
	global df
	global dfb
	global dff
	global dfidx
	global dffu
	global dfop
	df = mt.SecID(assetClass='E',field='')
	dfb = mt.SecID(assetClass='B',field='')
	dff = mt.SecID(assetClass='F',field='')
	dfidx = mt.SecID(assetClass='IDX',field='')
	dffu = mt.SecID(assetClass='FU',field='')
	dfop = mt.SecID(assetClass='OP',field='')
	secid_tosql()

#交易所交易日历
#TradeCal(self, exchangeCD='', beginDate='', endDate='', field='')
def tradecal():
	global dfcd
	dfcd = mt.TradeCal(exchangeCD='XSHG,XSHE,CCFX,XDCE,XSGE,XZCE,XHKG',field='')
	dfcd.insert(0,'uploadtime',nowtime)
	tradecal_tosql()

#证券板块成分
#SecTypeRel(self, secID='', ticker='', typeID='', field='')
def typerel():
	global dftyperel
	dftyperel = mt.SecTypeRel(field='')
	dftyperel.insert(0,'uploadtime',nowtime)
	typerel_tosql()

#证券板块分类列表
#SecType(self, field='')
def type():
	global dftype
	dftype = mt.SecType(field='')
	dftype.insert(0,'uploadtime',nowtime)
	type_tosql()

#地域分类
#SecTypeRegion(self, field='')
def typeregion():
	global dftyperegion
	dftyperegion = mt.SecTypeRegion(field='')
	dftyperegion.insert(0,'uploadtime',nowtime)
	typeregion_tosql()

#概念分类
def typeconcept():
	global dftypeconcept
	dftypeconcept = ts.get_concept_classified()
	dftypeconcept.insert(0,'uploadtime',nowtime)
	typeconcept_tosql()

#行业分类
def typeindustry():
	global dftypeindustry
	dftypeindustry = ts.get_industry_classified()
	dftypeindustry.insert(0,'uploadtime',nowtime)
	typeindustry_tosql()
	
#地域分类,省份
def typearea():
	global dftypearea
	dftypearea = ts.get_area_classified()
	dftypearea.insert(0,'uploadtime',nowtime)
	typearea_tosql()


#存入数据库
#tb_secid
#插入id
def insertid():
	sql = """ALTER TABLE tb_secid 
			ADD secid_id bigint(20) not null auto_increment ,
			ADD primary key (secid_id)"""
	cursor.execute(sql)
def createtb():
	df.to_sql('tb_secid',engine)
	dfb.to_sql('tb_secid',engine,if_exists='append')
	dff.to_sql('tb_secid',engine,if_exists='append')
	dfidx.to_sql('tb_secid',engine,if_exists='append')
	dffu.to_sql('tb_secid',engine,if_exists='append')
	dfop.to_sql('tb_secid',engine,if_exists='append')
	#插入当前时间
	sql = """ALTER TABLE tb_secid 
	ADD uploadtime TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
	"""
	cursor.execute(sql)
	count = cursor.execute('show columns from tb_secid like \'secid_id\'') 
	if count == 0:
		insertid()
def secid_tosql():
	counttb = cursor.execute('show tables like \'tb_secid\'') 
	if counttb == 0:
		createtb()
	else:
		df.to_sql('tb_secid',engine,if_exists='append')
		dfb.to_sql('tb_secid',engine,if_exists='append')
		dff.to_sql('tb_secid',engine,if_exists='append')
		dfidx.to_sql('tb_secid',engine,if_exists='append')
		dffu.to_sql('tb_secid',engine,if_exists='append')
		dfop.to_sql('tb_secid',engine,if_exists='append')

		sql = """create table temp_id as (select secid_id, ticker, count(distinct ticker) from tb_secid group by ticker)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_secid where secid_id not in(select secid_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

#tb_tradecal
def insertidtradecal():
	sql = """ALTER TABLE tb_tradecal 
			ADD tradecal_id bigint(20) not null auto_increment ,
			ADD primary key (tradecal_id)"""
	cursor.execute(sql)
def createtbtradecal():
	dfcd.to_sql('tb_tradecal',engine)
	count = cursor.execute('show columns from tb_tradecal like \'tradecal_id\'') 
	if count == 0:
		insertidtradecal()
def tradecal_tosql():
	counttbtradecal = cursor.execute('show tables like \'tb_tradecal\'') 
	if counttbtradecal == 0:
		createtbtradecal()
	else:
		dfcd.to_sql('tb_tradecal',engine,if_exists='append')
		sql = """create table temp_id as (select tradecal_id, calendarDate,exchangeCD, count(distinct calendarDate,exchangeCD) from tb_tradecal group by calendarDate,exchangeCD)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_tradecal where tradecal_id not in(select tradecal_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

#tb_typerel
def insertidtyperel():
	sql = """ALTER TABLE tb_typerel 
			ADD typerel_id bigint(20) not null auto_increment ,
			ADD primary key (typerel_id)"""
	cursor.execute(sql)
def createtbtyperel():
	dftyperel.to_sql('tb_typerel',engine)
	insertidtyperel()
def typerel_tosql():
	counttbtyperel = cursor.execute('show tables like \'tb_typerel\'') 
	if counttbtyperel == 0:
		createtbtyperel()
	else:
		dftyperel.to_sql('tb_typerel',engine,if_exists='append')
		sql = """create table temp_id as (select typerel_id, typeID,secID, count(distinct typeID,secID) from tb_typerel group by typeID,secID)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_typerel where typerel_id not in(select typerel_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

#tb_type
def insertidtype():
	sql = """ALTER TABLE tb_type 
			ADD type_id bigint(20) not null auto_increment ,
			ADD primary key (type_id)"""
	cursor.execute(sql)
def createtbtype():
	dftype.to_sql('tb_type',engine)
	insertidtype()
def type_tosql():
	counttbtype = cursor.execute('show tables like \'tb_type\'') 
	if counttbtype == 0:
		createtbtype()
	else:
		dftype.to_sql('tb_type',engine,if_exists='append')
		sql = """create table temp_id as (select type_id, typeID, count(distinct typeID) from tb_type group by typeID)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_type where type_id not in(select type_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

#tb_typeregion
def insertidtyperegion():
	sql = """ALTER TABLE tb_typeregion 
			ADD typeregion_id bigint(20) not null auto_increment ,
			ADD primary key (typeregion_id)"""
	cursor.execute(sql)
def createtbtyperegion():
	dftyperegion.to_sql('tb_typeregion',engine)
	insertidtyperegion()
def typeregion_tosql():
	counttbtyperegion = cursor.execute('show tables like \'tb_typeregion\'') 
	if counttbtyperegion == 0:
		createtbtyperegion()
	else:
		dftyperegion.to_sql('tb_typeregion',engine,if_exists='append')
		sql = """create table temp_id as (select typeregion_id, typeID, count(distinct typeID) from tb_typeregion group by typeID)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_typeregion where typeregion_id not in(select typeregion_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

#tb_typeconcept
def insertidtypeconcept():
	sql = """ALTER TABLE tb_typeconcept
			ADD typeconcept_id bigint(20) not null auto_increment ,
			ADD primary key (typeconcept_id)"""
	cursor.execute(sql)
def createtbtypeconcept():
	dftypeconcept.to_sql('tb_typeconcept',engine)
	insertidtypeconcept()
def typeconcept_tosql():
	counttbtypeconcept = cursor.execute('show tables like \'tb_typeconcept\'') 
	if counttbtypeconcept == 0:
		createtbtypeconcept()
	else:
		dftypeconcept.to_sql('tb_typeconcept',engine,if_exists='append')
		sql = """create table temp_id as (select typeconcept_id, code,c_name, count(distinct code,c_name) from tb_typeconcept group by code,c_name)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_typeconcept where typeconcept_id not in(select typeconcept_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)
	
#tb_typeindustry
def insertidtypeindustry():
	sql = """ALTER TABLE tb_typeindustry
			ADD typeindustry_id bigint(20) not null auto_increment ,
			ADD primary key (typeindustry_id)"""
	cursor.execute(sql)
def createtbtypeindustry():
	dftypeindustry.to_sql('tb_typeindustry',engine)
	insertidtypeindustry()
def typeindustry_tosql():
	counttbtypeindustry = cursor.execute('show tables like \'tb_typeindustry\'') 
	if counttbtypeindustry == 0:
		createtbtypeindustry()
	else:
		dftypeindustry.to_sql('tb_typeindustry',engine,if_exists='append')
		sql = """create table temp_id as (select typeindustry_id, code,c_name, count(distinct code,c_name) from tb_typeindustry group by code,c_name)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_typeindustry where typeindustry_id not in(select typeindustry_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

#tb_typearea
def insertidtypearea():
	sql = """ALTER TABLE tb_typearea
			ADD typearea_id bigint(20) not null auto_increment ,
			ADD primary key (typearea_id)"""
	cursor.execute(sql)
def createtbtypearea():
	dftypearea.to_sql('tb_typearea',engine)
	insertidtypearea()
def typearea_tosql():
	counttbtypearea = cursor.execute('show tables like \'tb_typearea\'') 
	if counttbtypearea == 0:
		createtbtypearea()
	else:
		dftypearea.to_sql('tb_typearea',engine,if_exists='append')
		sql = """create table temp_id as (select typearea_id, code,c_name, count(distinct code,c_name) from tb_typearea group by code,c_name)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_typearea where typearea_id not in(select typearea_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

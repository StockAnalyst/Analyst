#-*- coding: UTF-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from sqlalchemy import create_engine
import tushare as ts
#import pandas as pd
#import numpy as np
import time
#nowtime = datetime.datetime.now()
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_equ?charset=utf8')

eq = ts.Equity()

import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_equ" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

#股票列表: 获取沪深上市公司基本情况
def stock():
	dflist = ts.get_stock_basics()
	dflist.insert(0,'uploadtime',nowtime)
	dflist.to_sql('tb_list',engine,if_exists='append')
	#dflist.to_excel('E:/Anaconda/getdata/test.xlsx')
	def insertid():
		sql = """ALTER TABLE tb_list 
				ADD list_id int(20) not null auto_increment ,
				ADD primary key (list_id)"""
		cursor.execute(sql)
	count = cursor.execute('show columns from tb_list like \'list_id\'') 
	if count == 0:
		insertid()
	sql = """create table temp_id as (select list_id, code, count(distinct code) from tb_list group by code)
		"""
	cursor.execute(sql)
	sql = """
				delete from tb_list where list_id not in(select list_id from temp_id)
		"""
	cursor.execute(sql)
	sql = """
				drop table temp_id
		"""
	cursor.execute(sql)

#Equ(self, equTypeCD='', secID='', ticker='', listStatusCD='', field=''):
#获取股票的基本信息，包含股票交易代码及其简称、股票类型、上市状态、上市板块、上市日期等；上市状态为最新数据，不显示历史变动信息。
#A股B股
def equ():
	global dfab
	dfab = eq.Equ(equTypeCD='A,B',field='')
	dfab.insert(0,'uploadtime',nowtime)
	equ_tosql()

# 创建数据表SQL语句,添加主键id
def insertid():
	sql = """ALTER TABLE tb_equ 
			ADD equ_id int(20) not null auto_increment ,
			ADD primary key (equ_id)"""
	cursor.execute(sql)
def createtb():
	dfab.to_sql('tb_equ',engine)
	count = cursor.execute('show columns from tb_equ like \'equ_id\'') 
	if count == 0:
		insertid()
def equ_tosql():
	counttb = cursor.execute('show tables like \'tb_equ\'') 
	if counttb == 0:
		createtb()
	else:
		dfab.to_sql('tb_equ',engine,if_exists='append')
		sql = """create table temp_id as (select equ_id, ticker, count(distinct ticker) from tb_equ group by ticker)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_equ where equ_id not in(select equ_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)



#EquAllot(self, isAllotment='', secID='', ticker='', beginDate='', endDate='', field=''):
#获取股票历次配股的基本信息，包含每次配股方案的内容、方案进度、历史配股预案公布次数以及最终是否配股成功。
#0:最终配股不成功,1:最终配股成功
def equallot():
	global dfallot
	dfallot = eq.EquAllot(isAllotment='0,1',field='')
	dfallot.insert(0,'uploadtime',nowtime)
	equallot_tosql()

def insertidallot():
	sql = """ALTER TABLE tb_equallot 
			ADD equallot_id int(20) not null auto_increment ,
			ADD primary key (equallot_id)"""
	cursor.execute(sql)
def createtballot():
	dfallot.to_sql('tb_equallot',engine)
	sql = """ALTER TABLE 'tb_equallot' 
	modify column 'frCurrencyCD' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'recordDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'exRightsDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'payBeginDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'payEndDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'listDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
	"""
	cursor.execute(sql)
	count = cursor.execute('show columns from tb_equallot like \'equallot_id\'') 
	if count == 0:
		insertidallot()
def equallot_tosql():
	counttballot = cursor.execute('show tables like \'tb_equallot\'') 
	if counttballot == 0:
		createtballot()
	else:
		dfallot.to_sql('tb_equallot',engine,if_exists='append')
		sql = """create table temp_id as (select equallot_id, ticker, count(distinct ticker,listDate) from tb_equallot group by ticker,listDate)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_equallot where equallot_id not in(select equallot_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)



#EquDiv(self, eventProcessCD='', exDivDate='', secID='', ticker='', beginDate='', endDate='', field=''):
#获取股票历次分红(派现、送股、转增股)的基本信息，包含历次分红预案的内容、实施进展情况以及历史宣告分红次数。
#eventProcessCD分红方案的实施进程，可选：1-董事会预案，2-股东大会通过，3-股东大会否决，6-方案实施，7-停止实施。
def equdiv():
	global dfdiv
	dfdiv = eq.EquDiv(eventProcessCD='1,2,3,6,7',field='')
	dfdiv.insert(0,'uploadtime',nowtime)
	equdiv_tosql()

def insertiddiv():
	sql = """ALTER TABLE tb_equdiv 
			ADD equdiv_id int(20) not null auto_increment ,
			ADD primary key (equdiv_id)"""
	cursor.execute(sql)
def createtbdiv():
	dfdiv.to_sql('tb_equdiv',engine)
	count = cursor.execute('show columns from tb_equdiv like \'equdiv_id\'') 
	if count == 0:
		insertiddiv()
	sql = """
	ALTER TABLE 'tb_equdiv' 
	modify column 'frCurrencyCD' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'recordDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'exDivDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'bLastTradeDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'payCashDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL, 
	modify column 'bonusShareListDate' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
	modify column 'ftdAfExdiv' TEXT CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL
	"""
	cursor.execute(sql)
def equdiv_tosql():
	counttbdiv = cursor.execute('show tables like \'tb_equdiv\'') 
	if counttbdiv == 0:
		createtbdiv()
	else:
		dfdiv.to_sql('tb_equdiv',engine,if_exists='append')
		sql = """create table temp_id as (select equdiv_id, ticker, count(distinct ticker,recordDate) from tb_equdiv group by ticker,recordDate)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_equdiv where equdiv_id not in(select equdiv_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)



# EquIPO(self, eventProcessCD='', secID='', ticker='', field=''):
#获取股票首次公开发行上市的基本信息，包含股票首次公开发行的进程及发行结果。
#eventProcessCD:股票首次公开发行进程，可选进程有：9——上市，10——撤销上市，11——正在发行，12——暂缓发行，13——发行结束待上市。
def equipo():
	global dfipo
	dfipo = eq.EquIPO(eventProcessCD='9,10,11,12,13',field='')
	dfipo.insert(0,'uploadtime',nowtime)
	equipo_tosql()

def insertidipo():
	sql = """ALTER TABLE tb_equipo 
			ADD equipo_id int(20) not null auto_increment ,
			ADD primary key (equipo_id)"""
	cursor.execute(sql)
def createtbipo():
	dfipo.to_sql('tb_equipo',engine)
	count = cursor.execute('show columns from tb_equipo like \'equipo_id\'') 
	if count == 0:
		insertidipo()
def equipo_tosql():
	counttbipo = cursor.execute('show tables like \'tb_equipo\'') 
	if counttbipo == 0:
		createtbipo()
	else:
		dfipo.to_sql('tb_equipo',engine,if_exists='append')
		sql = """create table temp_id as (select equipo_id, ticker, count(distinct ticker) from tb_equipo group by ticker)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_equipo where equipo_id not in(select equipo_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)


#EquRetud(self, listStatusCD='', secID='', ticker='', beginDate='', dailyReturnNoReinvLower='', dailyReturnNoReinvUpper='', 
#dailyReturnReinvLower='', dailyReturnReinvUpper='', endDate='', isChgPctl='', field=''):
#获取股票每日回报率的基本信息，包含交易当天的上市状态、日行情以及除权除息事项的基本数据。
#listStatusCD:上市状态，可选状态有:L-上市，S-暂停，DE-终止上市，UN-未上市，默认为L。
def equretud():
	global dfretudl
	todaydate = time.strftime('%Y%m%d')
	dfretudl = eq.EquRetud(listStatusCD='L,S,DE,UN',beginDate='20130101',endDate=todaydate,field='')
	dfretudl.insert(0,'uploadtime',nowtime)
	equretud_tosql()

def insertidretud():
	sql = """ALTER TABLE tb_equretud 
			ADD equretud_id int(20) not null auto_increment ,
			ADD primary key (equretud_id)"""
	cursor.execute(sql)
def createtbretud():
	dfretudl.to_sql('tb_equretud',engine)
	count = cursor.execute('show columns from tb_equretud like \'equretud_id\'') 
	if count == 0:
		insertidretud()
def equretud_tosql():
	counttbretud = cursor.execute('show tables like \'tb_equretud\'') 
	if counttbretud == 0:
		createtbretud()
	else:
		dfretudl.to_sql('tb_equretud',engine,if_exists='append')
		sql = """create table temp_id as (select equretud_id, ticker, count(distinct ticker,tradeDate) from tb_equretud group by ticker,tradeDate)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_equretud where equretud_id not in(select equretud_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

#FstTotal(self, beginDate='', endDate='', exchangeCD='', field=''):
#获取上海、深圳交易所公布的每个交易日的融资融券交易汇总的信息，包括成交量、成交金额。本交易日可获取前一交易日的数据。
def fsttotal():
	global dffsttotal
	dffsttotal = eq.FstTotal(field='')
	dffsttotal.insert(0,'uploadtime',nowtime)
	fsttotal_tosql()

def insertidtotal():
	sql = """ALTER TABLE tb_fsttotal 
			ADD fsttotal_id int(20) not null auto_increment ,
			ADD primary key (fsttotal_id)"""
	cursor.execute(sql)
def createtbtotal():
	dffsttotal.to_sql('tb_fsttotal',engine)
	count = cursor.execute('show columns from tb_fsttotal like \'fsttotal_id\'') 
	if count == 0:
		insertidtotal()
def fsttotal_tosql():
	counttbtotal = cursor.execute('show tables like \'tb_fsttotal\'') 
	if counttbtotal == 0:
		createtbtotal()
	else:
		dffsttotal.to_sql('tb_fsttotal',engine,if_exists='append')
		sql = """create table temp_id as (select fsttotal_id, tradeDate, count(distinct tradeDate,exchangeCD) from tb_fsttotal group by tradeDate,exchangeCD)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_fsttotal where fsttotal_id not in(select fsttotal_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

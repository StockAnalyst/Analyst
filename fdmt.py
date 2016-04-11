#-*- coding: UTF-8 -*-  

from sqlalchemy import create_engine
import tushare as ts
#import pandas as pd
#import numpy as np
import time
#nowtime = datetime.datetime.now()
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_fdmt?charset=utf8')

import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_fdmt" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

###################
#按年度、季度获取盈利能力数据
def getprofit(year,quarter):
	dfprofit = ts.get_profit_data(year,quarter)
	dfprofit.insert(0,'uploadtime',nowtime)
	dfprofit.insert(1,'year',year)
	dfprofit.insert(2,'quarter',quarter)
	dfprofit.to_sql('tb_profit',engine,if_exists='append')
#按年度、季度获取营运能力数据
def getoperation(year,quarter):
	dfoperation = ts.get_operation_data(year,quarter)
	dfoperation.insert(0,'uploadtime',nowtime)
	dfoperation.insert(1,'year',year)
	dfoperation.insert(2,'quarter',quarter)
	dfoperation.to_sql('tb_operation',engine,if_exists='append')	
#按年度、季度获取成长能力数据
def getgrowth(year,quarter):
	dfgrowth = ts.get_growth_data(year,quarter)
	dfgrowth.insert(0,'uploadtime',nowtime)
	dfgrowth.insert(1,'year',year)
	dfgrowth.insert(2,'quarter',quarter)
	dfgrowth.to_sql('tb_growth',engine,if_exists='append')
#按年度、季度获取偿债能力数据
def getdebtpaying(year,quarter):
	dfdebtpaying = ts.get_debtpaying_data(year,quarter)
	dfdebtpaying.insert(0,'uploadtime',nowtime)
	dfdebtpaying.insert(1,'year',year)
	dfdebtpaying.insert(2,'quarter',quarter)
	dfdebtpaying.to_sql('tb_debtpaying',engine,if_exists='append')
#按年度、季度获取现金流量数据
def getcashflow(year,quarter):
	dfcashflow = ts.get_cashflow_data(year,quarter)
	dfcashflow.insert(0,'uploadtime',nowtime)
	dfcashflow.insert(1,'year',year)
	dfcashflow.insert(2,'quarter',quarter)
	dfcashflow.to_sql('tb_cashflow',engine,if_exists='append')


bd = ts.Fundamental()

#FdmtEe(self, reportType='', secID='', ticker='', beginDate='', endDate='', publishDateBegin='', publishDateEnd='', field=''):
#获取2007年及以后年度上市公司披露的业绩快报中的主要财务指标等其他数据，
#包括本期，去年同期，及本期与期初数值同比数据。每季证券交易所披露相关公告时更新数据，
#公司ipo时发布相关信息也会同时更新。每日9：00前完成证券交易所披露的数据更新，中午发布公告每日12：45前完成更新。
#获取2010年到2015年的年报数据，截止到2014年12月31日。
def fdmtee():
	#global dfeea
	dfeea = bd.FdmtEe(reportType='A',beginDate='20100101', endDate='20141231',field='')
	dfeea.insert(1,'uploadtime',nowtime)
	#global dfee2
	#按三季报获取2015年数据
	dfee2 = bd.FdmtEe(reportType='CQ3',beginDate='20150101', endDate='20151231',field='')
	dfee2.insert(1,'uploadtime',nowtime)
	#global dfee3
	#按第三季报获取2015年数据
	dfee3 = bd.FdmtEe(reportType='Q3',beginDate='20150101', endDate='20151231',field='')
	dfee3.insert(1,'uploadtime',nowtime)
	#global dfees
	#按半年报获取2015年数据
	dfees = bd.FdmtEe(reportType='S1',beginDate='20150101', endDate='20151231',field='')
	dfees.insert(1,'uploadtime',nowtime)
	#global dfeeq
	#按第一季报获取2015年数据
	dfeeq = bd.FdmtEe(reportType='Q1',beginDate='20150101', endDate='20151231',field='')
	dfeeq.insert(1,'uploadtime',nowtime)

# 创建数据表SQL语句,添加主键id

	dfeea.to_sql('tb_fdmtee',engine,if_exists='append')
	dfee2.to_sql('tb_fdmtee',engine,if_exists='append')
	dfee3.to_sql('tb_fdmtee',engine,if_exists='append')
	dfees.to_sql('tb_fdmtee',engine,if_exists='append')
	dfeeq.to_sql('tb_fdmtee',engine,if_exists='append')

	def insertid():
		sql = """ALTER TABLE tb_fdmtee 
				ADD fdmt_id int(20) not null auto_increment ,
				ADD primary key (fdmt_id)"""
		cursor.execute(sql)

	count = cursor.execute('show columns from tb_fdmtee like \'fdmt_id\'') 
	if count == 0:
		insertid()

	sql = """create table temp_id as (select fdmt_id, secID,publishDate, count(distinct secID,publishDate,) from tb_fdmtee group by secID,publishDate,)
		"""
	cursor.execute(sql)
	sql = """
				delete from tb_fdmtee where fdmt_id not in(select fdmt_id from temp_id)
		"""
	cursor.execute(sql)
	sql = """
				drop table temp_id
		"""
	cursor.execute(sql)


"""
FdmtEf(self, reportType='', secID='', ticker='', beginDate='', endDate='', 
               forecastType='', publishDateBegin='', publishDateEnd='', field=''):
1、获取2007年及以后年度上市公司披露的公告中的预期下一报告期收入、净利润、归属于母公司净利润、基本每股收益及其幅度变化数据。
2、上市公司对经营成果科目的预计情况数据一般为其上限与下限，上限取值为公告中披露该科目中绝对值较大值，下限取值为公告中披露该科目中绝对值较小值。
3、数值为"正"代表该公司预计盈利，数值为"负"代表该公司预计亏损。若上下限"正"、"负"符号不同，代表该公司盈利亏损情况尚不确定。
4、业绩预期类型以公告中文字披露预期类型为准，若公告中未有文字披露预期类型，则根据数据情况判断预期类型。
5、每季证券交易所披露相关公告时更新数据，公司ipo时发布相关信息也会同时更新。每日9：00前完成证券交易所披露的数据更新，中午发布公告每日12：45前完成更新。
"""
def fdmtef():
	
	dfef = bd.FdmtEf(reportType='A',beginDate='20140101',endDate='20150101',field='')
	dfef.insert(1,'uploadtime',nowtime)
	dfef.to_sql('tb_fdmtef',engine,if_exists='append')
	#按三季报获取2015年数据
	dfef2 = bd.FdmtEf(reportType='CQ3',beginDate='20150101', endDate='20151231',field='')
	dfef2.insert(1,'uploadtime',nowtime)
	dfef2.to_sql('tb_fdmtef',engine,if_exists='append')

	#按第三季报获取2015年数据
	dfef3 = bd.FdmtEf(reportType='Q3',beginDate='20150101', endDate='20151231',field='')
	dfef3.insert(1,'uploadtime',nowtime)
	dfef3.to_sql('tb_fdmtef',engine,if_exists='append')

	#按半年报获取2015年数据
	dfefs = bd.FdmtEf(reportType='S1',beginDate='20150101', endDate='20151231',field='')
	dfefs.insert(1,'uploadtime',nowtime)
	dfefs.to_sql('tb_fdmtef',engine,if_exists='append')

	#按第一季报获取2015年数据
	dfefq = bd.FdmtEf(reportType='Q1',beginDate='20150101', endDate='20151231',field='')
	dfefq.insert(1,'uploadtime',nowtime)
	dfefq.to_sql('tb_fdmtef',engine,if_exists='append')

	# 创建数据表SQL语句,添加主键id
	def insertid():
		sql = """ALTER TABLE tb_fdmtef 
				ADD fdmtef_id int(20) not null auto_increment ,
				ADD primary key (fdmtef_id)"""
		cursor.execute(sql)

	count = cursor.execute('show columns from tb_fdmtef like \'fdmtef_id\'') 
	if count == 0:
		insertid()

	sql = """create table temp_id as (select fdmtef_id, secID,publishDate, count(distinct secID,publishDate,) from tb_fdmtef group by secID,publishDate,)
		"""
	cursor.execute(sql)
	sql = """
				delete from tb_fdmtef where fdmtef_id not in(select fdmtef_id from temp_id)
		"""
	cursor.execute(sql)
	sql = """
				drop table temp_id
		"""
	cursor.execute(sql)
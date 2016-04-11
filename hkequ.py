#-*- coding: UTF-8 -*-  

from sqlalchemy import create_engine
import tushare as ts
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_hkequ?charset=utf8')
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_hkequ" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
#HKEqu(self, listStatusCD='', secID='', ticker='', field=''):
#获取香港交易所上市股票的基本信息，包含股票交易代码及其简称、股票类型、上市状态、上市板块、上市日期等；上市状态为最新状态。
#listStatusCD:上市状态，可选状态有:L-上市，S-暂停，DE-终止上市，UN-未上市。
hk = ts.HKequity()
def hkequ():
	global dfl
	dfl = hk.HKEqu(listStatusCD='L,DE,UN,S',field='')
	dfl.insert(0,'uploadtime',nowtime)
	hkequ_tosql()

# 创建数据表SQL语句,添加主键id
def insertid():
	sql = """ALTER TABLE tb_hkequ 
			ADD hkequ_id int(20) not null auto_increment ,
			ADD primary key (hkequ_id)"""
	cursor.execute(sql)

def createtb():
	dfl.to_sql('tb_hkequ',engine)
	count = cursor.execute('show columns from tb_hkequ like \'hkequ_id\'') 
	if count == 0:
		insertid()
def hkequ_tosql():
	counttb = cursor.execute('show tables like \'tb_hkequ\'') 
	if counttb == 0:
		createtb()
	else:
		dfl.to_sql('tb_hkequ',engine,if_exists='append')
		sql = """create table temp_id as (select hkequ_id, ticker, count(distinct ticker) from tb_hkequ group by ticker)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_hkequ where hkequ_id not in(select hkequ_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)


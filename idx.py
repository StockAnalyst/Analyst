#-*- coding: UTF-8 -*-  

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
fd = ts.Idx()


#Idx(self, secID='', ticker='', field=''):
#获取国内外指数的基本要素信息，包括指数名称、指数代码、发布机构、发布日期、基日、基点等。
def idx():
	global df
	df = fd.Idx(field='')
	df.insert(0,'uploadtime',nowtime)
	idx_tosql()

# 创建数据表SQL语句,添加主键id
def insertid():
	sql = """ALTER TABLE tb_idx 
			ADD idx_id int(20) not null auto_increment ,
			ADD primary key (idx_id)"""
	cursor.execute(sql)
def createtb():
	df.to_sql('tb_idx',engine)
	count = cursor.execute('show columns from tb_idx like \'idx_id\'') 
	if count == 0:
		insertid()
def idx_tosql():
	counttb = cursor.execute('show tables like \'tb_idx\'') 
	if counttb == 0:
		createtb()
	else:
		df.to_sql('tb_idx',engine,if_exists='append')
		sql = """create table temp_id as (select idx_id, secID, count(distinct secID) from tb_idx group by secID)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_idx where idx_id not in(select idx_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

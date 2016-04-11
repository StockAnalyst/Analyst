#-*- coding: UTF-8 -*-  

from sqlalchemy import create_engine
import tushare as ts
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_opt?charset=utf8')
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect("127.0.0.1","root","root","db_opt" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

#Opt(self, contractStatus='', optID='', secID='', ticker='', varSecID='', varticker='', field=''):
#获取期权合约编码，交易代码，交易市场，标的等相关信息
#contractStatus合约状态，UN-未上市、L-上市、S-暂停上市、DE-退市
fd = ts.Options()
def opt():
	global df
	df = fd.Opt(contractStatus='L,DE,UN,S', field='')
	df.insert(0,'uploadtime',nowtime)
	opt_tosql()

# 创建数据表SQL语句,添加主键id
def insertid():
	sql = """ALTER TABLE tb_opt 
			ADD opt_id int(20) not null auto_increment ,
			ADD primary key (opt_id)"""
	cursor.execute(sql)

def createtb():
	df.to_sql('tb_opt',engine)
	count = cursor.execute('show columns from tb_opt like \'opt_id\'') 
	if count == 0:
		insertid()
def opt_tosql():
	counttb = cursor.execute('show tables like \'tb_opt\'') 
	if counttb == 0:
		createtb()
	else:
		df.to_sql('tb_opt',engine,if_exists='append')
		sql = """create table temp_id as (select opt_id, optID, count(distinct optID) from tb_opt group by optID)
		"""
		cursor.execute(sql)
		sql = """
				delete from tb_opt where opt_id not in(select opt_id from temp_id)
		"""
		cursor.execute(sql)
		sql = """
				drop table temp_id
		"""
		cursor.execute(sql)

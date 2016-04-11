# -*- coding: utf-8 -*- 
###########################################################################
##dzhStockList.py 大智慧证券列表数据处理
###########################################################################


import struct
import binascii
import os
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_dzh",charset='utf8' )
cursor = db.cursor()

#从index.dat中获取证券代码列表
def codelist():
	
	path = 'D:/dzh/dzh_gtja/internet/tcpipdata/index.dat'
	size = os.path.getsize(path)
	amount = size/9

	file_object = open(path,'rb')  
	for i in xrange(0,amount):
		
		stocknum = struct.unpack("h",file_object.read(2))
		code = binascii.b2a_qp(file_object.read(6))
		split00 = struct.unpack("c",file_object.read(1))

		listdata = []
		listdata.append(stocknum[0])
		listdata.append(code)
		listdata.append(nowtime)
		cursor.execute("""INSERT INTO stock_list(stocknum,code,uploadtime) VALUES (%s,%s,%s)
					""",listdata)
		

#从init.dat中获取证券名称列表
def namelist():
	path = 'D:/dzh/dzh_gtja/internet/tcpipdata/init.dat'
	size = os.path.getsize(path)
	amount = (size-28)/32
	#证券数量，28bit头部
	print amount

	file_object = open(path,'rb') 
	latestdate = binascii.b2a_qp(file_object.read(8))
	unknown = struct.unpack("h",file_object.read(2))
	amountnum = struct.unpack("h",file_object.read(2))
	unknownn = file_object.read(16)
	print latestdate
	#amountnum[0]=amount
	#print amountnum

	for i in xrange(0,amount):
			
		#证券名称
		namebina = file_object.read(8)
		u = namebina.decode('GBK')
		name = u.encode('UTF-8')
		#print name
		#cmd中输出中文要加decode：print name.decode('UTF-8')
		
		#证券代码
		code = binascii.b2a_qp(file_object.read(6))
		#print code
		#证券代码类型:
		#0x1F 0x00一般证券（场内交易的股票和基金等）1f00:31
		#0x1E 0x00 证券指数（上证指数、深圳）1e00:30
		#0x20 0x00 证券指数（沪深300指数等）2000:32
		codetypeint = struct.unpack("h",file_object.read(2))
		codetype=''
		if codetypeint[0] == 30:
			codetype += '证券指数(上证指数,深圳)'
		elif codetypeint[0] == 31:
			codetype += '一般证券'
		else:
			codetype += '证券指数(沪深300)'
		#print codetype.decode("utf-8")
		#print codetype
		#昨天收盘
		close = struct.unpack('l',file_object.read(4))
		#print close[0]*1000
		#昨天的5日平均成交量(手)
		pervol5days = struct.unpack('l',file_object.read(4))
		#print pervol5days[0]
		#总股本(单位手)
		totalshares = struct.unpack('l',file_object.read(4))
		#print totalshares[0]
		#流通股(单位手)
		tradableshares = struct.unpack('l',file_object.read(4))
		#print tradableshares[0]

		listdata = []
		listdata.append(name)
		listdata.append(code)
		listdata.append(codetype)
		listdata.append(close[0]*1000)
		listdata.append(pervol5days[0])
		listdata.append(totalshares[0])
		listdata.append(tradableshares[0])
		listdata.append(nowtime)
		cursor.execute("""INSERT INTO stock_info(name,code,codetype,close,pervol5days,totalshares,tradableshares,uploadtime) 
			VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
					""",listdata)
	#for i in xrange(0,amountnum[0]):


#namelist()
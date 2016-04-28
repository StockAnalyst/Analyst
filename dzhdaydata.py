# -*- coding: utf-8 -*- 
###########################################################################
##dzhdaydata.py 大智慧上深股日线数据处理
###########################################################################
from sqlalchemy import create_engine
import os
import struct
import datetime
import pandas as pd
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
engine = create_engine('mysql://root:root@127.0.0.1/db_dzh?charset=utf8')

import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_dzh",charset='utf8' )
cursor = db.cursor()

#获取目录下所有文件列表名，形如['000001.day', '000002.day']
def get_recursive_file_list(path):
	current_files = os.listdir(path)
	all_files = []
	for file_name in current_files:
		#full_file_name = os.path.join(path, file_name)#全路径名
		full_file_name = file_name
		all_files.append(full_file_name)
	
		if os.path.isdir(full_file_name):
			next_level_files = get_recursive_file_list(full_file_name)
			all_files.extend(next_level_files)
	
	return all_files


#上海，深圳股票日线数据
def getdata(pathname):
	all_file_names = get_recursive_file_list(pathname)
	data1 = {'tradedate':[],'openPrice':[],'highestPrice':[],'lowestPrice':[],'closePrice':[],'turnoverValue':[],'turnoverVol':[],'san':[],'uploadtime':[],'code':[],'stocktype':[]}
	if pathname == 'D:/dzh/dzh_gtja/data/SHase/Day/':
		stocktype = 'sh'
	elif pathname == 'D:/dzh/dzh_gtja/data/SZnse/Day/':
		stocktype = 'sz'

	nums = len(all_file_names)
	#nums = 3
	for i in xrange(0,nums):
		name =  all_file_names[i].split('.')
		code = "%s" %name[0]
		#print code
		#file_object = open('D:/dzh/dzh_gtja/data/SHase/Day/000001.day','rb')  
		filepath = pathname + all_file_names[i]
		timestamp = os.path.getmtime(filepath)
		date = datetime.datetime.fromtimestamp(timestamp)
		if(date.strftime('%Y-%m-%d')=='2016-04-14'):
			try:
				file_object = open(filepath,'rb')
				size = os.path.getsize(filepath)
				amount = size/40
				print amount
				#print filepath,date.strftime('%Y-%m-%d')
				for i in range(0,amount):
				
					dataday1 = struct.unpack("llllllllll",file_object.read(4*10))
					gettradetime = dataday1[0]
					timeArray = time.strptime(str(gettradetime),'%Y%m%d')
					tradetime = time.strftime('%Y-%m-%d',timeArray)
					data1['tradedate'].append(tradetime)
					#print data1['tradedate']
					data1['openPrice'].append(dataday1[1]/1000.000)
					
					data1['highestPrice'].append(dataday1[2]/1000.000)
					data1['lowestPrice'].append(dataday1[3]/1000.000)
					data1['closePrice'].append(dataday1[4]/1000.000)
					data1['turnoverValue'].append(dataday1[5]/10.000)
					data1['turnoverVol'].append(dataday1[6])
					data1['san'].append(dataday1[7])
					data1['uploadtime'].append(nowtime)
					data1['code'].append(code)
					data1['stocktype'].append(stocktype)
					#cursor.execute("""INSERT INTO sh_dayline VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')
					#""",data1)
					
			except Exception, e:
				print('File Error:'+str(e))	
			finally:
				file_object.close()
		
	data1frame = pd.DataFrame(data1)
	#print data1frame
	data1frame.to_sql('sh_dayline',engine,if_exists='append')		
			#print all_file_names[i]
			#print dataday1
			#print dataday2

if __name__ == '__main__':
	getdata('D:/dzh/dzh_gtja/data/SHase/Day/')
	getdata('D:/dzh/dzh_gtja/data/SZnse/Day/')
	#getdataSZ()
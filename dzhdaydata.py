# -*- coding: utf-8 -*- 
###########################################################################
##dzhdaydata.py 大智慧上深股日线数据处理
###########################################################################

import os
import struct
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
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


#上海股票日线数据
def getdataSH():
	all_file_names = get_recursive_file_list('D:/dzh/dzh_gtja/data/SHase/Day/')
	nums = len(all_file_names)
	#nums = 3
	for i in xrange(0,nums):
		name =  all_file_names[i].split('.')
		code = "%s" %name[0]
		#print code
		#file_object = open('D:/dzh/dzh_gtja/data/SHase/Day/000001.day','rb')  
		try:
			file_object = open('D:/dzh/dzh_gtja/data/SHase/Day/'+all_file_names[i],'rb')  
			try:
				dataday1 = struct.unpack("llllllllll",file_object.read(4*10))
			#	dataday2 = struct.unpack("llllllllll",file_object.read(4*10))
			
			except Exception, e:
				print('File Error day1:'+all_file_names[i]+str(e))
			else:
				data1 = []
				data1.append(dataday1[0]) 
				data1.append(dataday1[1]/1000.000)
				data1.append(dataday1[2]/1000.000)
				data1.append(dataday1[3]/1000.000)
				data1.append(dataday1[4]/1000.000)
				data1.append(dataday1[5]/10.000)
				data1.append(dataday1[6])
				data1.append(dataday1[7])
				data1.append(dataday1[8])
				data1.append(dataday1[9])
				data1.append(nowtime)
				data1.append(code)
				
				cursor.execute("""INSERT INTO sh_dayline VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')
				""",data1)
			try:
				dataday2 = struct.unpack("llllllllll",file_object.read(4*10))
			except Exception, e:
				print('File Error day2:'+all_file_names[i]+str(e))
			else:	
				data2 = []
				data2.append(dataday2[0]) 
				data2.append(dataday2[1]/1000.000)
				data2.append(dataday2[2]/1000.000)
				data2.append(dataday2[3]/1000.000)
				data2.append(dataday2[4]/1000.000)
				data2.append(dataday2[5]/10.000)
				data2.append(dataday2[6])
				data2.append(dataday2[7])
				data2.append(dataday2[8])
				data2.append(dataday2[9])
				data2.append(nowtime)
				data2.append(code)
				cursor.execute("""INSERT INTO sh_dayline VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')
				""",data2)
		except Exception, e:
			print('File Error:'+str(e))	
		finally:
			file_object.close()
		#dataday1 = struct.unpack("llllllllll",file_object.read(4*10))
		#dataday2 = struct.unpack("llllllllll",file_object.read(4*10))
		
		
		#print all_file_names[i]
		#print dataday1
		#print dataday2

#深圳股票日线数据
def getdataSZ():
	all_file_names = get_recursive_file_list('D:/dzh/dzh_gtja/data/SZnse/Day/')
	nums = len(all_file_names)
	#nums = 3
	for i in xrange(0,nums):
		name =  all_file_names[i].split('.')
		code = "%s" %name[0]
		try:	
			file_object = open('D:/dzh/dzh_gtja/data/SZnse/Day/'+all_file_names[i],'rb')  
			try:
				dataday1 = struct.unpack("llllllllll",file_object.read(4*10))
			except Exception, e:
				print('File Error day1:'+all_file_names[i]+str(e))
			else:	
				data1 = []
				data1.append(dataday1[0]) 
				data1.append(dataday1[1]/1000.000)
				data1.append(dataday1[2]/1000.000)
				data1.append(dataday1[3]/1000.000)
				data1.append(dataday1[4]/1000.000)
				data1.append(dataday1[5]/10.000)
				data1.append(dataday1[6])
				data1.append(dataday1[7])
				data1.append(dataday1[8])
				data1.append(dataday1[9])
				data1.append(nowtime)
				data1.append(code)
				
				cursor.execute("""INSERT INTO sz_dayline VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')
				""",data1)
			try:	
				dataday2 = struct.unpack("llllllllll",file_object.read(4*10))
			except Exception, e:
				print('File Error day2:'+all_file_names[i]+str(e))
			else:	
				data2 = []
				data2.append(dataday2[0]) 
				data2.append(dataday2[1]/1000.000)
				data2.append(dataday2[2]/1000.000)
				data2.append(dataday2[3]/1000.000)
				data2.append(dataday2[4]/1000.000)
				data2.append(dataday2[5]/10.000)
				data2.append(dataday2[6])
				data2.append(dataday2[7])
				data2.append(dataday2[8])
				data2.append(dataday2[9])
				data2.append(nowtime)
				data2.append(code)
				cursor.execute("""INSERT INTO sz_dayline VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')
				""",data2)
				#print dataday1
				#print dataday2
		except Exception, e:
			print('File Error:'+str(e))	
		finally:
			file_object.close()

if __name__ == '__main__':
	getdataSH()
	getdataSZ()
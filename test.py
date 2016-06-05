#!usr/bin/python
#-*- coding:UTF-8 -*-
#import timecheck
#print timecheck.getyesday('2016-04-07')
import pandas as pd
import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_dzh",charset='utf8' )

cursor = db.cursor()
def df():
		
	'''
	#?
	cursor.execute("""SELECT * FROM sh_dayline where tradedate='20160111' limit 10
	""")
	data = cursor.fetchall()'''
	data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
	        'year': [2000, 2001, 2002, 2001, 2002],
	        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
	frame = pd.DataFrame(data)
	print frame
	print frame.ix[0,['year']].values#选择行和列
	print frame.ix[2]#选择单行
	print frame.ix[:,'year']#选择单列
	frame2 = frame.ix[:,['year','pop']]
	print frame2
	#print frame.values#values属性转为数组格式
	#print frame.values[0][2]
	#print type(data)
	#print frame['year']
	#print frame
	'''
	raw_data = {
	        'subject_id': ['1', '2', '3', '4', '5'],
	        'first_name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'], 
	        'last_name': ['Anderson', 'Ackerman', 'Ali', 'Aoni', 'Atiches']}
	df_a = pd.DataFrame(raw_data, columns = ['subject_id', 'first_name', 'last_name'])
	raw_data = {
	        'subject_id': ['4', '5', '6', '7', '8'],
	        'first_name': ['Alice', 'Brian', 'Bran', 'Bryce', 'Betty'], 
	        'last_name': ['Aoni', 'Black', 'Balwner', 'Brice', 'Btisan']}
	df_b = pd.DataFrame(raw_data, columns = ['subject_id', 'first_name', 'last_name'])
	print pd.merge(df_a, df_b, on='subject_id', how='outer',suffixes=('_left', '_right'))
	'''
def list():
	list1 = [[1,2,3,4],[5,6,7,8]]
	list2 = []
	list3 = []
	for i in range(0,2):
		list2.append(list1[i][2])
	list3.extend(list1[0][2:])
	'''print list3
	print list2
	print max(list2)'''
	createVar = locals()
	for i in range(0,9):
		createVar['a%s'%i] = []
	for b in range(10):
		c = 'a%d = %d'%(b,b)
	exec c
	print a1,a2
list()
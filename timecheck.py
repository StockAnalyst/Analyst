#!user/bin/python
#-*- coding: UTF-8 -*- 
import time
import datetime
#global struct_time,yes_time_nyr,pre_yes_time_nyr,pre_pre_yes_time_nyr
#now_time = 
def getpredate(uptime):
	
	global struct_time 
	struct_time = time.strptime(uptime,'%Y-%m-%d')#元组格式
	#转为datetime格式
	now_time = datetime.datetime(struct_time.tm_year,struct_time.tm_mon,struct_time.tm_mday)
	#print now_time
	yes_time = now_time + datetime.timedelta(days=-1)
	global yes_time_nyr 
	yes_time_nyr = yes_time.strftime('%Y-%m-%d')
	#print yes_time_nyr
	pre_yes_time = now_time + datetime.timedelta(days=-2)
	global pre_yes_time_nyr 
	pre_yes_time_nyr = pre_yes_time.strftime('%Y-%m-%d')
	pre_pre_yes_time = now_time + datetime.timedelta(days=-3)
	global pre_pre_yes_time_nyr
	pre_pre_yes_time_nyr = pre_pre_yes_time.strftime('%Y-%m-%d')
#getpredate('2016-04-07')


def compare_hourmin(now_hm,start_hm,end_hm):
	#minute = time.strftime("%M",a)
	now_hm_int = int(now_hm)
	start_hm_int = int(start_hm)
	end_hm_int = int(end_hm)
	if((now_hm_int >= start_hm_int) and (now_hm_int <= end_hm_int)):
		return True
	else:return False

#获取昨天时间
def getyesday(uptime):
	getpredate(uptime)
	tradetime = uptime
	'''a = time.localtime()
	weekday = time.strftime("%w",a)
	hours = time.strftime("%H",a)'''
	weekday = struct_time.tm_wday
	if weekday == '1':
		tradetime = pre_pre_yes_time_nyr
	else:
		tradetime = yes_time_nyr
	
	return tradetime

#获取上一个非周末时间,更新时间为hm，若在更新时间之前，则返回上一交易日数据
def getweekday(uptime,hm):
	tradetime = uptime
	getpredate(uptime)
	a = time.localtime()
	weekday = time.strftime("%w",a)
	now_hm = time.strftime("%H%M",a)
	#hm = '1530'
	if weekday == '6':
		tradetime = yes_time_nyr
	elif weekday == '0':
		tradetime = pre_yes_time_nyr
	elif weekday == '1' and (int(now_hm) < int(hm)):#周一15:30之前，返回上周五数据
		tradetime = pre_pre_yes_time_nyr
	elif int(now_hm) < int(hm):
		tradetime = yes_time_nyr
	return tradetime

def chgtimefor(tradetime):
	timeArray = time.strptime(tradetime,'%Y-%m-%d')
	inputtradetime = time.strftime('%Y%m%d',timeArray)
	return inputtradetime


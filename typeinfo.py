#!usr/bin/python
#-*- coding: UTF-8 -*-
import pandas as pd
import time
todaydate = time.strftime('%Y-%m-%d')
import timecheck
import checktddata
from connect_db import cursor
from sqlalchemy import create_engine
engine = create_engine('mysql://root:root@127.0.0.1/db_mkt?charset=utf8')

#from typedata import industry 
import typedata



def calindustry(data,count,typeindustry):
	ch_pt_all=neg_capital_all=market_per_all=weight_ch_pt_all=turnoverRate_all=turnoverVol_all=turnoverValue_all=pe_all = 0
	count_chpt = 0.0
	for i in range(0,count):
		neg_capital_i = data[i][10] 	#流通股本=流通市值/收盘价
		neg_capital_all += neg_capital_i 	#板块总流通股本
		turnoverValue_all += data[i][5]		#总成交额
		if data[i][9] > 0:
			count_chpt += 1 	#涨幅为正加1

	for i in range(0,count):
		ch_pt_i = data[i][9]	#涨幅=(最新价-昨收价)/昨收价
		
		
		ch_pt_all += ch_pt_i	#涨幅和
		neg_capital_i = data[i][10] 
		
		weight_ch_pt_i = ch_pt_i * neg_capital_i / neg_capital_all	#权涨幅
		weight_ch_pt_all += weight_ch_pt_i
		turnoverVol_all += data[i][4]	#总成交量
		market_per = data[i][5] / turnoverValue_all		#市场比=个股交易额/总成交额
		market_per_all += market_per
		turnoverRate_all += data[i][6] 	#总换手率
		if data[i][7] == None:
			data[i][7] = 0
		pe_all += data[i][7]	#总市盈率

	avg_ch_pt = "%.3f" % (ch_pt_all / count * 100)	#均涨幅 (涨幅*100%)
	avg_weight_ch_pt = "%.3f" % (weight_ch_pt_all / count * 100)#均权涨幅
	#turnoverVol_all
	max_chpt_name = data[0][8]
	count_chpt_per = count_chpt / count 	#涨股比,涨幅为正的占所有交易个股的比例
	#print count_chpt_per
	avg_market_per = "%.3f" % (market_per_all / count * 100	)#均市场比
	avg_turnoverRate = "%.3f" % (turnoverRate_all / count * 100) #均换手率
	avg_pe = pe_all / count  	#均市盈率
	#print type(typeindustry)
	per_industry = [typeindustry.decode('utf-8'),avg_ch_pt,avg_weight_ch_pt,turnoverVol_all,
	max_chpt_name,count_chpt_per,avg_market_per,avg_turnoverRate,avg_pe]
	
	return per_industry

def gettypei(typei,datatb_name):
	
	typeindustry = typei.encode('utf8')
	cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd group by tradeDate order by tradeDate desc limit 1
			""")
	tradetimesql = cursor.fetchone()
	tradeDate = tradetimesql[0]
	if datatb_name == 'sec_typearea':
		cursor.execute("""SELECT area,ticker,preClosePrice,closePrice,turnoverVol,turnoverValue,turnoverRate,PE,secShortName,
		(closePrice-preClosePrice)/preClosePrice,negMarketValue/closePrice
				FROM mkt_mktequd,sec_typearea
				WHERE area = %s AND code = concat(ticker,'') AND tradeDate = %s
				order by (closePrice-preClosePrice)/preClosePrice desc
			""",(typeindustry,tradeDate))
	elif datatb_name == 'sec_typeindustry':
		cursor.execute("""SELECT c_name,ticker,preClosePrice,closePrice,turnoverVol,turnoverValue,turnoverRate,PE,secShortName,
		(closePrice-preClosePrice)/preClosePrice,negMarketValue/closePrice
			FROM mkt_mktequd,sec_typeindustry
			WHERE c_name = %s AND code = concat(ticker,'') AND tradeDate = %s
			order by (closePrice-preClosePrice)/preClosePrice desc
			""",(typeindustry,tradeDate))
	elif datatb_name == 'sec_typeconcept':
		cursor.execute("""SELECT c_name,ticker,preClosePrice,closePrice,turnoverVol,turnoverValue,turnoverRate,PE,secShortName,
		(closePrice-preClosePrice)/preClosePrice,negMarketValue/closePrice
			FROM mkt_mktequd,sec_typeconcept
			WHERE c_name = %s AND code = concat(ticker,'') AND tradeDate = %s
			order by (closePrice-preClosePrice)/preClosePrice desc
			""",(typeindustry,tradeDate))
	#流通股本=流通市值/收盘价
	data = cursor.fetchall()
	#print type(data)
	count = cursor.rowcount
	print count
	data1 = [[] for i in range(count)]
	k=0
	for datalist in data:
		for j in range(0,11):
			data1[k].append(datalist[j])
		k=k+1

	return calindustry(data1,count,typeindustry)
def typeinfo(countind,caltb_name,datatb_name,type_name):
	
	#countind = 49
	type_info = [[] for i in range(countind)]
	for i in range(0,countind):
		if type_name == 'industry':
			type_info[i].extend(gettypei(typedata.industry[i],datatb_name))
		elif type_name == 'area':
			type_info[i].extend(gettypei(typedata.area[i],datatb_name))
		elif type_name == 'concept':
			type_info[i].extend(gettypei(typedata.concept[i],datatb_name))
		
	#print type_info
	#print type(type_info[0][0])
	#print type_info[0][0]
	typeindustryinfo = []
	avg_ch_pt = []
	avg_weight_ch_pt = []
	turnoverVol_all = []
	max_chpt_name = []
	count_chpt_per = []
	avg_market_per = []
	avg_turnoverRate = []
	avg_pe = []
	for i in range(0,countind):
		typeindustryinfo.append(type_info[i][0])
		avg_ch_pt.append(type_info[i][1])
		avg_weight_ch_pt.append(type_info[i][2])
		turnoverVol_all.append(type_info[i][3])
		max_chpt_name.append(type_info[i][4])
		count_chpt_per.append(type_info[i][5])
		avg_market_per.append(type_info[i][6])
		avg_turnoverRate.append(type_info[i][7])
		avg_pe.append(type_info[i][8])
		#print typeindustryinfo
	
	type_infodata = {'typeinfo':typeindustryinfo,
	'avg_ch_pt':avg_ch_pt,'avg_weight_ch_pt':avg_weight_ch_pt,'turnoverVol_all':turnoverVol_all,
	'max_chpt_name':max_chpt_name,'count_chpt_per':count_chpt_per,
	'avg_market_per':avg_market_per,'avg_turnoverRate':avg_turnoverRate,'avg_pe':avg_pe

	}
	frame = pd.DataFrame(type_infodata,columns=['typeinfo',
	'avg_ch_pt','avg_weight_ch_pt','turnoverVol_all',
	'max_chpt_name','count_chpt_per',
	'avg_market_per','avg_turnoverRate','avg_pe'])
	tradetime = timecheck.getweekday(todaydate,'1530')
	frame.insert(8,'tradetime',tradetime)
	#print frame
	frame.to_sql('%s' % (caltb_name),engine,if_exists='append')
	#print typeindustryinfo,avg_pe
	return type_info
#typeinfo(46,'cal_industryinfo','sec_typeindustry','industry')
#typeinfo(32,'cal_areainfo','sec_typearea','area')
#typeinfo(156,'cal_conceptinfo','sec_typeconcept','concept')
#-*- coding:utf-8 -*-
import pandas as pd
from WindPy import *
import datetime
import time
nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
from sqlalchemy import create_engine
engine = create_engine('mysql://root:root@127.0.0.1/db_dzh?charset=utf8')

w.start()
#print w.isconnected()
#data=w.wsd("600000.SH","close,amt")
#data = w.wset("sectorconstituent","date=20160425;sectorid=a001010100000000")
#data = w.wsd("000001.SZ","industry_CSRC12,industry_gics,industry_gicscode", "2016-03-26", "2016-04-24", "industryType=1")
#data=w.wsd("000001.SZ", "open,high,low,close", "2016-04-25", "2016-04-26", "Fill=Previous")
#print fm
#print type(fm)
#实时数据
def getrealdata():
	wsq_data = w.wsq("000001.SZ", "rt_date,rt_time,rt_pre_close,rt_open,rt_high,rt_low,rt_last_amt,rt_last_vol,rt_last,rt_latest,rt_vol,rt_amt,rt_chg,rt_pct_chg,rt_high_limit,rt_low_limit,rt_swing,rt_vwap,rt_upward_vol,rt_downward_vol,rt_bsize_total,rt_asize_total,rt_vol_ratio,rt_turn,rt_pre_iopv,rt_iopv,rt_mkt_cap,rt_pre_oi,rt_oi,rt_pre_settle,rt_settle,rt_discount,rt_ask1,rt_ask2,rt_ask3,rt_ask5,rt_ask4,rt_bid1,rt_bid2,rt_bid3,rt_bid4,rt_bid5,rt_bsize1,rt_bsize2,rt_bsize3,rt_bsize4,rt_bsize5,rt_asize1,rt_asize2,rt_asize3,rt_asize4,rt_asize5,rt_mf_ratio,rt_activebuy_amt,rt_activesell_amt,rt_activesell_vol,rt_activenetin_vol,rt_activenetin_amt,rt_activeinvol_prop,rt_activeinflow_prop")
	fm_wsq=pd.DataFrame(wsq_data.Data,index=wsq_data.Fields,columns=wsq_data.Times)
	fm_wsq=fm_wsq.T #将矩阵转置
	fm_wsq.to_sql("wind_realdata",engine,if_exists="append")

#数据集 板块成分,输入板块id,日期，返回日期、wind代码和证券名称
#sectorid = 'a001010100000000'
#wset_bord = w.wset("sectorconstituent","date=20160427;sectorid=a001010100000000")
def getset():
	sectoridlist = ["1000009415000000","1000009417000000"]
	print len(sectoridlist)
	for i in range(0,len(sectoridlist)):
		
		wset_bord = w.wset("sectorconstituent","date=20160427;sectorid="+ sectoridlist[i])

		#print wset_bord.Data[1][0]
		data = {'date':wset_bord.Data[0],
				'win_code':wset_bord.Data[1],
				'sec_name':wset_bord.Data[2]
		}
		fm_wsetbord = pd.DataFrame(data)
		#fm_wsetbord=pd.DataFrame(wset_bord.Data,index=wset_bord.Fields,columns=wset_bord.Times)
		#fm_wsetbord=fm_wsetbord.T

		fm_wsetbord.insert(0,'uploadtime',nowtime)
		fm_wsetbord.insert(0,'sectorid',sectoridlist[i])
		fm_wsetbord.to_sql("wind_wsetbord",engine,if_exists="append")

#分钟序列WSI
def getwsi():
	wsi_data = w.wsi("000001.SZ,000002.SZ", "BIAS,BOLL,EXPMA,KDJ,MA,MACD,RSI,oi,pct_chg,chg,amt,volume,close,low,high,open", "2016-04-27 09:00:00", "2016-04-27 22:25:37", "BIAS_N=12;BOLL_N=26;BOLL_Width=2;BOLL_IO=1;EXPMA_N=12;KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=1;MA_N=5;MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=1;RSI_N=6")
	fm_wsi=pd.DataFrame(wsi_data.Data,index=wsi_data.Fields)
	fm_wsi=fm_wsi.T #将矩阵转置
	fm_wsi.insert(0,'uploadtime',nowtime)
	fm_wsi.to_sql("wind_wsidata",engine,if_exists="append")


def getwss():
	wss_data = w.wss("000001.SZ,000022.SZ,000029.SZ", "pct_chg_per,pct_chg_nd,avg_pct_chg_nd,low_per,max_close_per","startDate=20160326;endDate=20160426;days=-5;tradeDate=20160425;priceAdj=U")
	#print wss_data.Data[0]
	fm_wss=pd.DataFrame(wss_data.Data,index=wss_data.Fields)
	fm_wss=fm_wss.T #将矩阵转置
	fm_wss.insert(0,'uploadtime',nowtime)
	fm_wss.to_sql("wind_wssdata",engine,if_exists="append")

#getwss()

tradeDate = '20160510'
data1 = w.wss("000001.SZ","pct_chg_per","tradeDate=20160510")
data2 = w.wss("000001.SZ","pct_chg_per","tradeDate="+tradeDate)
data3 = w.wss("000001.SZ","pct_chg_per","tradeDate=%s"%(tradeDate))

print data1
print data2
print data3

field = "rt_low_limit"
data4 = w.wsq("000001.SZ","rt_pct_chg,%s"%(field))
print data4

def ResumeTradeDown(code): #复牌补跌和一字跌停
    fields = "maxupordown,pct_chg,turn,open,close,HIGH"
    lasttradeday = Lasttradeday()
    lasttradedate = lasttradeday.date()
    print lasttradedate
    tradeday = ["tradeDate=2016-05-13"]   # 如何将交易时间为最新?

    #tradeday = [ "tradeDate = lasttradedate"]
    data = w.wss(code, fields,tradeday)
    data = w.wss(code, fields,"tradeDate=2016-05-10")
    data1 = w.wss(code,fields)
    print data1
    df = DataFrame(data.Data,index=data.Fields,columns=data.Codes).T
    print df.head()
def Lasttradeday():
    data = w.tdays("")
    tday = data.Data[0]
    Lasttradeday = tday[-1]
    def Lasttradeday():
    data = w.tdays("")
    tday = data.Data[0]
    Lasttradeday = tday[-1]
   
def Lasttradeday():
    data = w.tdays("")
    tday = data.Data[0]
    Lasttradeday = tday[-1]
    #print Lasttradeday
    return Lasttradeday
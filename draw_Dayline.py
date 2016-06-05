#-*- coding:UTF-8 -*-
#!/usr/bin/env python
#FILE:当前版本绘图实例（只管绘图,转换模块单独在外）

import wx
import matplotlib as mpl
#在import pyplot 前 切换backend，避免报warning,但并没有什么效果
mpl.use('PS')
import numpy as np
import matplotlib.pylab as pl
import matplotlib.pyplot as plt

import MySQLdb
import MPL_transfer
import his
'''
#之前在建立数据库的时候，将date字段的类型设置成 DATE
conn = MySQLdb.connect(host ='localhost',port=3306,user='root',passwd='root',db='db_mkt')
#建立游标
cursor = conn.cursor()'''
from connect_db import cursor

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []

def drawDaylineDB(code):
    global x,y1,y2,y3,y4,y5,y6,y7
    x = []
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    y6 = []
    y7 = []
    cursor.execute("""SELECT distinct(code) FROM mkt_his WHERE code=%s""",(code))
    count = cursor.rowcount
    if count==0:
        his.hist(code)
        print "update data"

    #else:
    cursor.execute("""SELECT * FROM mkt_his WHERE code=%s""",(code))
    allDaylineData = cursor.fetchall()
    for daylineData in allDaylineData:    
        #第一列是时间，作为x轴
        x.append(daylineData[0])
    
        #下面分别是ma5,ma10,ma20
        y1.append(daylineData[10])
        y2.append(daylineData[11])
        y3.append(daylineData[12])

        #下面分别是volume,v_ma5,v_ma10,v_ma20
        y4.append(daylineData[7])
        y5.append(daylineData[13])
        y6.append(daylineData[14])
        y7.append(daylineData[15])
    
        #只取一年的数据（还是取所有的数据？由于现在图是可以调整的）
        if (len(x) >= 365):
            break

#设置中文字体
mpl.rcParams['font.sans-serif'] = ['SimHei']

class DrawFrame(wx.Frame):
    def __init__(self,lista,results,code):
        wx.Frame.__init__(self,None,-1,u'绘图'+str(code),size=(1000,800))
        self.code = str(code)
        print self.code
        print type(self.code)
        drawDaylineDB(self.code)
        self.BoxSizer=wx.BoxSizer(wx.VERTICAL)

        #311
        self.MPL1 = MPL_transfer.MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL1,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)        
        self.MPL1.plot(x,y1,'r',label='ma5')
        self.MPL1.plot(x,y2,'g',label='ma10')
        self.MPL1.plot(x,y3,'b',label='ma20')
        self.MPL1.title_MPL(u"单股票日线图")        
        #调整精度和显示范围，现在的想法是显示一年，精度为1个月，看看数据库怎么表示的
        #self.MPL1.xticker(10,1)
        #self.MPL1.xlim(735835,735857)
        self.MPL1.ylabel(u"MA值")
        self.MPL1.legend(loc = 'upper left')
        self.MPL1.UpdatePlot()

        #312
        self.MPL2 = MPL_transfer.MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL2,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)
        self.MPL2.bar(x,y4,color = 'k')
        self.MPL2.plot(x,y5,label='v_ma5')
        self.MPL2.plot(x,y6,label='v_ma10')
        self.MPL2.plot(x,y7,label='v_ma20')
        self.MPL2.title_MPL(u"单股票日Volume图")
        self.MPL2.ylabel(u"Volume值")
        self.MPL2.legend(loc = 'upper left')
        self.MPL2.UpdatePlot()

        #313(这些是统计参数,等数据处理后，再画图)
        print len(results)
        if len(results) != 0:
            print "111"
            self.MPL3 = MPL_transfer.MPL_Panel_base(self)
            self.BoxSizer.Add(self.MPL3,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)
            self.MPL3.plot(lista,results[0],label=results[2][0])
            self.MPL3.plot(lista,results[1],label=results[2][1])
            print "222"
            title = u'技术指标' + results[2][0]
            self.MPL3.title_MPL(title)
            self.MPL3.legend(loc = 'upper left')
            self.MPL3.UpdatePlot()
            
        self.SetSizer(self.BoxSizer)
        

    

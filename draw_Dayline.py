#-*- coding:UTF-8 -*-
#!/usr/bin/env python
#FILE:绘图

import wx
import numpy as np
import matplotlib as mpl
from matplotlib import pylab as pl
from matplotlib import pyplot as plt

import draw_Dayline_db
import MPL_transfer

#设置中文字体
mpl.rcParams['font.sans-serif'] = ['SimHei']


class DrawFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u'绘图',size=(1200,900))

        self.BoxSizer=wx.BoxSizer(wx.VERTICAL)

        #311
        self.MPL1 = MPL_transfer.MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL1,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)        
        self.MPL1.plot(draw_Dayline_db.x,draw_Dayline_db.y1,'r',label='ma5')
        self.MPL1.plot(draw_Dayline_db.x,draw_Dayline_db.y2,'g',label='ma10')
        self.MPL1.plot(draw_Dayline_db.x,draw_Dayline_db.y3,'b',label='ma20')
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
        self.MPL2.bar(draw_Dayline_db.x,draw_Dayline_db.y4,color = 'k')
        self.MPL2.plot(draw_Dayline_db.x,draw_Dayline_db.y5,label='v_ma5')
        self.MPL2.plot(draw_Dayline_db.x,draw_Dayline_db.y6,label='v_ma10')
        self.MPL2.plot(draw_Dayline_db.x,draw_Dayline_db.y7,label='v_ma20')
        self.MPL2.title_MPL(u"单股票日Volume图")
        self.MPL2.ylabel(u"Volume值")
        self.MPL2.legend(loc = 'upper left')
        self.MPL2.UpdatePlot()

        #313(这些是统计参数？等数据处理后，再画图)
        self.MPL3 = MPL_transfer.MPL_Panel_base(self)
        self.BoxSizer.Add(self.MPL3,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)

        self.SetSizer(self.BoxSizer)
        


#关闭游标，提交结果，断开数据库连接--这些是必须要做的
draw_Dayline_db.cur.close()
draw_Dayline_db.conn.commit()
draw_Dayline_db.conn.close()
    

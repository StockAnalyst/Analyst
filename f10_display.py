#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#FILE:f10个股资料界面

import wx
import MySQLdb

db =MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="db_mkt",charset="utf8")
cursor = db.cursor() 

class TestFrame1(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u'个股资料 F10',size=(600,400))
        panel = wx.Panel(self)
        
    #1.设置所有的窗口
        #第一部分是两个textctrl和十六个button
        fname = wx.TextCtrl(panel,-1,u'股票名称',pos=(15,15))
        fcode = wx.TextCtrl(panel,-1,u'SZ000001',pos=(15,45))

        Button001 = wx.Button(panel,-1,u'操盘必读')
        self.Bind(wx.EVT_BUTTON,self.On001,Button001)

        Button002 = wx.Button(panel,-1,u'财务透视')
        self.Bind(wx.EVT_BUTTON,self.On002,Button002)

        Button003 = wx.Button(panel,-1,u'主营构成')
        self.Bind(wx.EVT_BUTTON,self.On003,Button003)

        Button004 = wx.Button(panel,-1,u'行业新闻')
        self.Bind(wx.EVT_BUTTON,self.On004,Button004)

        Button005 = wx.Button(panel,-1,u'大事提醒')
        self.Bind(wx.EVT_BUTTON,self.On005,Button005)

        Button006 = wx.Button(panel,-1,u'八面来风')
        self.Bind(wx.EVT_BUTTON,self.On006,Button006)

        Button007 = wx.Button(panel,-1,u'公司概况')
        self.Bind(wx.EVT_BUTTON,self.On007,Button007)

        Button008 = wx.Button(panel,-1,u'管理层')
        self.Bind(wx.EVT_BUTTON,self.On008,Button008)

        Button009 = wx.Button(panel,-1,u'最新季报')
        self.Bind(wx.EVT_BUTTON,self.On009,Button009)
        
        Button010 = wx.Button(panel,-1,u'股东进出')
        self.Bind(wx.EVT_BUTTON,self.On010,Button010)

        Button011 = wx.Button(panel,-1,u'股本分红')
        self.Bind(wx.EVT_BUTTON,self.On011,Button011)

        Button012 = wx.Button(panel,-1,u'资料运作')
        self.Bind(wx.EVT_BUTTON,self.On012,Button012)

        Button013 = wx.Button(panel,-1,u'行业地位')
        self.Bind(wx.EVT_BUTTON,self.On013,Button013)

        Button014 = wx.Button(panel,-1,u'公司公告')
        self.Bind(wx.EVT_BUTTON,self.On014,Button014)

        Button015 = wx.Button(panel,-1,u'经营动态')
        self.Bind(wx.EVT_BUTTON,self.On015,Button015)

        Button016 = wx.Button(panel,-1,u'盈利预测')
        self.Bind(wx.EVT_BUTTON,self.On016,Button016)

        Button001.SetDefault()

        #第二部分是多行文本框(通过设置为self....说明其作用域是全局的)
        self.fmultitext = wx.TextCtrl(panel,-1,style=wx.TE_MULTILINE,pos=(15,100),size=(570,300))

        One = cursor.execute("""SELECT loc FROM tb_001 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)


        #这是mainsizer布局部分
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        #第一行firstSizer
        firstSizer = wx.BoxSizer(wx.HORIZONTAL)
        firstSizer.Add(fname)
        firstSizer.Add(Button001)
        firstSizer.Add(Button002)
        firstSizer.Add(Button003)
        firstSizer.Add(Button004)
        firstSizer.Add(Button005)
        firstSizer.Add(Button006)
        firstSizer.Add(Button007)
        firstSizer.Add(Button008)
        mainSizer.Add(firstSizer,0,wx.EXPAND,10)

        #第二行firstSizer
        secondSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondSizer.Add(fcode)
        secondSizer.Add(Button009)
        secondSizer.Add(Button010)
        secondSizer.Add(Button011)
        secondSizer.Add(Button012)
        secondSizer.Add(Button013)
        secondSizer.Add(Button014)
        secondSizer.Add(Button015)
        secondSizer.Add(Button016)
        mainSizer.Add(secondSizer,0,wx.EXPAND,10)

        mainSizer.Add(self.fmultitext,wx.EXPAND,wx.EXPAND,10)

        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def On001(self,event):
        #返回满足条件的数目
        #最好利用%的形参的方式，否则针对mysql数据库会时好时坏,同时这种形式便于传参
        One = cursor.execute("""SELECT loc FROM tb_001 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
        #返回满足条件的所有的条目
        #data = cursor.fetchall()
        #返回满足条件的第一条条目
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)
    
    def On002(self,event):
        One = cursor.execute("""SELECT loc FROM tb_002 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On003(self,event):
        One = cursor.execute("""SELECT loc FROM tb_003 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On004(self,event):
        One = cursor.execute("""SELECT loc FROM tb_004 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On005(self,event):
        One = cursor.execute("""SELECT loc FROM tb_005 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On006(self,event):
        One = cursor.execute("""SELECT loc FROM tb_006 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On007(self,event):
        One = cursor.execute("""SELECT loc FROM tb_007 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On008(self,event):
        One = cursor.execute("""SELECT loc FROM tb_008 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On009(self,event):
        One = cursor.execute("""SELECT loc FROM tb_009 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On010(self,event):
        One = cursor.execute("""SELECT loc FROM tb_010 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On011(self,event):
        One = cursor.execute("""SELECT loc FROM tb_011 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On012(self,event):
        One = cursor.execute("""SELECT loc FROM tb_012 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On013(self,event):
        One = cursor.execute("""SELECT loc FROM tb_013 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On014(self,event):
        One = cursor.execute("""SELECT loc FROM tb_014 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On015(self,event):
        One = cursor.execute("""SELECT loc FROM tb_015 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

    def On016(self,event):
        One = cursor.execute("""SELECT loc FROM tb_016 WHERE code=%s AND attr=%s""",("000001","SZ"))
        if One==0:
            pass
        else:
            data = cursor.fetchone()     
            f = open(data[0])
            txt = f.read()
            self.fmultitext.SetValue(txt)

'''    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    TestFrame1().Show()
    app.MainLoop()
    cursor.close()
    db.close()
'''

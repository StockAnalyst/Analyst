# -*- coding: utf-8 -*- 

###########################################################################
## mainpage
###########################################################################

import wx
import wx.grid

import mkt
import dayline
import dialogover
import dialoging
import pageupdate
import uprealtimetick


import tools_Dialog1
import tools_Dialog2
'''import upmkt
import upsec
import upfdmt
import upequ
import upfund
import uphkidxopt

import dialogmktequd
import dialogfundnav
import dialogsecid
'''
import time
todaydate = time.strftime('%Y-%m-%d')
import datetime
now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_nyr = yes_time.strftime('%Y-%m-%d')
pre_yes_time = now_time + datetime.timedelta(days=-2)
pre_yes_time_nyr = pre_yes_time.strftime('%Y-%m-%d')
pre_pre_yes_time = now_time + datetime.timedelta(days=-3)
pre_pre_yes_time_nyr = pre_pre_yes_time.strftime('%Y-%m-%d')
import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt",charset='utf8' )

cursor = db.cursor()
###########################################################################
## Class TestTable
###########################################################################
class TestTable(wx.grid.PyGridTableBase):#定义网格表
	def __init__(self,data,colLabels):
		wx.grid.PyGridTableBase.__init__(self)
		#self.colLabels =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
		#u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		#self.rowLabels = range(1,31)
		self.colLabels = colLabels
		self.data = data
		
	# these five are the required methods
	def GetNumberRows(self):
		return len(self.data)
		#return 30
	def GetNumberCols(self):
		return len(self.data[0])+1
	def IsEmptyCell(self, row, col):
		#return self.data.get((row, col)) is not None
		return False
	def GetValue(self, row, col):#为网格提供数据
		if self.data[row][col] is None:
			return ''
		else:
			return self.data[row][col]

	def SetValue(self, row, col, value):#给表赋值
		#self.data[(row,col)] = value
		pass
	def GetColLabelValue(self, col):#列标签
		return self.colLabels[col]
	#def GetRowLabelValue(self, row):#行标签
	#	return self.rowLabels[row]
	def MovePageDown():
		pass
	def MovePageUp():
		pass
###########################################################################
## Class MyFramemain
##沪深股票日行情
###########################################################################

class MyFramemain ( wx.Frame ):
	
	#定义获取数据
	#获取上一个非周末时间,更新时间为15:30，若在更新时间之前，则返回上一交易日数据
	def getweekday(uptime):
		tradetime = uptime
		a = time.localtime()
		weekday = time.strftime("%w",a)
		hours = time.strftime("%H",a)
		minute = time.strftime("%M",a)

		if weekday == '6':
			tradetime = yes_time_nyr
		elif weekday == '0':
			tradetime = pre_yes_time_nyr
		elif weekday == '1' and (hours < '15' or (hours == '15' and minute <'35')):#周一15:30之前，返回上周五数据
			tradetime = pre_pre_yes_time_nyr
		elif hours < '15' or (hours == '15' and minute <'35'):
			tradetime = yes_time_nyr
		return tradetime

	
	tradetime = getweekday(todaydate)
	cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd group by tradeDate order by tradeDate desc
					""")
	tradetimesql = cursor.fetchone()
	print tradetime
	print tradetimesql[0]
	if tradetime != tradetimesql[0] :
		'''
		app = wx.App()
		frame1 = dialoging.MyDialoging(parent=None)
		frame1.Show()
		app.MainLoop()'''
		#print tradetime
		timeArray = time.strptime(tradetime,'%Y-%m-%d')
		inputtradetime = time.strftime('%Y%m%d',timeArray)
		#print inputtradetime
		mkt.mktequd(inputtradetime)

		app = wx.App()
		#frame1.Close()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()
	cursor.execute("""select ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
						turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
			from mkt_mktequd where tradeDate = %s
			order by ticker asc
			limit 50
	""",(tradetime))

	datacode = cursor.fetchall()
	
	global data
	data = [[] for i in range(50)]
	k=0
	for datalist in datacode:
		for j in range(0,17):
			data[k].append(datalist[j])
		k=k+1
	#将ticker的显示数前面补0
	for i in range(0,50):
		data[i][0]= "%06d" % data[i][0]

	global colLabels
	colLabels =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
		u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"沪深股票日行情", pos = wx.DefaultPosition, size = wx.Size( 716,508 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		#id = frame.GetId()
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuupdb = wx.Menu()
		self.m_menuupdb.AppendSeparator()
		
		self.m_menuItemdb = wx.MenuItem( self.m_menuupdb, wx.ID_ANY, u"选择更新数据库", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuupdb.AppendItem( self.m_menuItemdb )
		
		self.m_menuupdb.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuupdb, u"更新数据库" ) 
		
		self.m_menuanal = wx.Menu()
		self.m_menuanal.AppendSeparator()
		
		self.m_menuItemanal1 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"报价分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal1 )
		
		self.m_menuItemanal2 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"即时分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal2 )
		
		self.m_menuItemanal3 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"技术分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal3 )
		
		self.m_menuItemanal4 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"报表分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal4 )
		
		self.m_menuanal.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuanal, u"分析" ) 
		
		self.m_menu19 = wx.Menu()
		self.m_menu19.AppendSeparator()
		
		self.m_menuItem47 = wx.MenuItem( self.m_menu19, wx.ID_ANY, u"期货日行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu19.AppendItem( self.m_menuItem47 )
		
		self.m_menu19.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menu19, u"显示" )

		self.m_menutools = wx.Menu()
                self.child1 = self.m_menutools.Append(-1,u'公式管理器','there are lots of formulas')
                self.child2 = self.m_menutools.Append(-1,u'模板管理器','there are lots of templates')
                self.m_menubar1.Append(self.m_menutools, u'工具')
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline33 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline33, 0, wx.EXPAND |wx.ALL, 5 )
		
		gSizer6 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"当前行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gSizer6.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_button119 = wx.Button( self.m_panel2, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button119, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		bSizer1.Add( gSizer6, 0, wx.EXPAND, 5 )
		
		self.m_staticline6 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer14 = wx.FlexGridSizer( 1, 1, 0, 0 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		########################		
		#创建网格表
		self.grid = wx.grid.Grid(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
		
		self.table = TestTable(data,colLabels)
		self.grid.SetTable(self.table, True)

		self.grid.EnableEditing( False )
		self.grid.EnableGridLines( True )
		self.grid.EnableDragGridSize( True )
		#self.grid.SetColSize( 8, 100 )
		#self.grid.AutoSizeColumns()
		#self.grid.AutoSizeRows()
		self.grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer14.Add( self.grid, 1, wx.ALL|wx.EXPAND, 5 )
		bSizer1.Add( fgSizer14, 1, wx.EXPAND, 5 )
		#########################

		
		self.m_staticline17 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel2.SetSizer( bSizer1 )
		self.m_panel2.Layout()
		bSizer1.Fit( self.m_panel2 )
		bSizer6.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.OnUpdata, id = self.m_menuItemdb.GetId() )
		self.Bind( wx.EVT_MENU, self.Onbaojia, id = self.m_menuItemanal1.GetId() )
		self.Bind( wx.EVT_MENU, self.Onjishi, id = self.m_menuItemanal2.GetId() )
		self.Bind( wx.EVT_MENU, self.Onjishu, id = self.m_menuItemanal3.GetId() )
		self.Bind( wx.EVT_MENU, self.Onbaobiao, id = self.m_menuItemanal4.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktfutd, id = self.m_menuItem47.GetId() )
		self.Bind(wx.EVT_MENU,self.OnChild1,self.child1)
                self.Bind(wx.EVT_MENU,self.OnChild2,self.child2)
		self.m_button119.Bind( wx.EVT_BUTTON, self.Onrefresh )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnUpdata( self, event ):
		app = wx.App()
		frame = pageupdate.MyFrameupdata(parent=None)
		frame.Show()
		app.MainLoop()

		event.Skip()
	
	def Onbaojia( self, event ):
		event.Skip()
	
	def Onjishi( self, event ):
		event.Skip()
	
	def Onjishu( self, event ):
		dayline.drawhist('000001')
		event.Skip()
	
	def Onbaobiao( self, event ):
		event.Skip()
	
	def Onmktfutd( self, event ):
		#self.frame = MyFramemain(parent=None)
		#self.frame.Show(False)
		#MyApp.close(self)
		self.Destroy()
		self.frame2 = MyFramefutd(parent=None)
		self.frame2.Show()
	#	event.Skip()

	def OnChild1(self,event):
                dlg = tools_Dialog1.SubclassDialog1()
                if dlg.ShowModal() == wx.ID_CANCEL:
                    print "cancel1"
                else:
                    print "OK1"
                #dlg = wx.SingleChoiceDialog(None,'which formula do you select?',
                 #                           'formulas manager',['3','2'])
                #if dlg.ShowModal() == wx.ID_OK:
                  #  reponse = dlg.GetStringSelection()
                #这里必须要销毁，否接不能够正常结束
                dlg.Destroy()

        def OnChild2(self,event):
                dlg = tools_Dialog2.SubclassDialog2()
                if dlg.ShowModal() == wx.ID_CANCEL:
                    print "cancel2"
                else:
                    print "OK2"
                dlg.Destroy()

	#刷新页面
	def Onrefresh( self, event ):

		self.m_panel2.Refresh()
		#event.Skip()
	
###########################################################################
## Class MyFramefutd
##期货日行情
###########################################################################

class MyFramefutd ( wx.Frame ):
	
	#定义获取数据
	#获取上一个非周末时间,更新时间为18:00，若在更新时间之前，则返回上一交易日数据
	def getweekday(uptime):
		tradetime = uptime
		a = time.localtime()
		weekday = time.strftime("%w",a)
		hours = time.strftime("%H",a)
		if weekday == '6':#周六
			tradetime = yes_time_nyr
		elif weekday == '0':#周日
			tradetime = pre_yes_time_nyr
		elif weekday == '1' and hours < '18':#周一18点之前，返回上周五数据
			tradetime = pre_pre_yes_time_nyr
		elif hours < '18':
			tradetime = yes_time_nyr
		return tradetime

	tradetime = getweekday(todaydate)
	cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfutd group by tradeDate order by tradeDate desc
					""")
	tradetimesql = cursor.fetchone()
	
	if tradetime != tradetimesql[0]:
		
		#app = wx.App()
		#frame1 = dialoging.MyDialoging(parent=None)
		#frame1.Show()
		#app.MainLoop()
		timeArray = time.strptime(tradetime,'%Y-%m-%d')
		inputtradetime = time.strftime('%Y%m%d',timeArray)
		
		mkt.mktfutd(inputtradetime)

		app = wx.App()
		#frame1.Close()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()
	cursor.execute("""select ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,preSettlePrice,
		closePrice,settlePrice,turnoverVol,turnoverValue,openInt,CHG,CHGPct,tradeDate
			from mkt_mktfutd where tradeDate = %s
			order by ticker asc
			limit 474
	""",(tradetime))

	datacode = cursor.fetchall()
	
	global data1
	data1 = [[] for i in range(474)]
	k=0
	for datalist in datacode:
		for j in range(0,15):
			data1[k].append(datalist[j])
		k=k+1
	global colLabels1
	colLabels1 =[u"合约代码",u"合约简称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"昨日结算价",u"今日收盘价",
	u"今日结算价",u"成交量",u"成交金额",u"持仓量",u"涨跌",u"涨跌幅",u"交易日期"]	

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"实时行情", pos = wx.DefaultPosition, size = wx.Size( 716,508 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuupdb = wx.Menu()
		self.m_menuupdb.AppendSeparator()
		
		self.m_menuItemdb = wx.MenuItem( self.m_menuupdb, wx.ID_ANY, u"选择更新数据库", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuupdb.AppendItem( self.m_menuItemdb )
		
		self.m_menuupdb.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuupdb, u"更新数据库" ) 
		
		self.m_menuanal = wx.Menu()
		self.m_menuanal.AppendSeparator()
		
		self.m_menuItemanal1 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"报价分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal1 )
		
		self.m_menuItemanal2 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"即时分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal2 )
		
		self.m_menuItemanal3 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"技术分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal3 )
		
		self.m_menuItemanal4 = wx.MenuItem( self.m_menuanal, wx.ID_ANY, u"报表分析", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuanal.AppendItem( self.m_menuItemanal4 )
		
		self.m_menuanal.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuanal, u"分析" ) 
		
		self.m_menu19 = wx.Menu()
		self.m_menu19.AppendSeparator()
		
		self.m_menuItem47 = wx.MenuItem( self.m_menu19, wx.ID_ANY, u"期货日行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu19.AppendItem( self.m_menuItem47 )
		
		self.m_menu19.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menu19, u"显示" )

		self.m_menutools = wx.Menu()
                self.child1 = self.m_menutools.Append(-1,u'公式管理器','there are lots of formulas')
                self.child2 = self.m_menutools.Append(-1,u'模板管理器','there are lots of templates')
                self.m_menubar1.Append(self.m_menutools, u'工具')
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline33 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline33, 0, wx.EXPAND |wx.ALL, 5 )
		
		gSizer6 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"当前行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gSizer6.Add( self.m_staticText1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_button119 = wx.Button( self.m_panel2, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer6.Add( self.m_button119, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		bSizer1.Add( gSizer6, 0, wx.EXPAND, 5 )
		
		self.m_staticline6 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer14 = wx.FlexGridSizer( 1, 1, 0, 0 )
		fgSizer14.SetFlexibleDirection( wx.BOTH )
		fgSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		########################		
		#创建网格表
		self.grid = wx.grid.Grid(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
		
		self.table = TestTable(data1,colLabels1)
		self.grid.SetTable(self.table, True)

		self.grid.EnableEditing( False )
		self.grid.EnableGridLines( True )
		self.grid.EnableDragGridSize( True )
		#self.grid.SetColSize( 8, 100 )
		#self.grid.AutoSizeColumns()
		#self.grid.AutoSizeRows()
		self.grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer14.Add( self.grid, 1, wx.ALL|wx.EXPAND, 5 )
		bSizer1.Add( fgSizer14, 1, wx.EXPAND, 5 )
		#########################

		
		self.m_staticline17 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel2.SetSizer( bSizer1 )
		self.m_panel2.Layout()
		bSizer1.Fit( self.m_panel2 )
		bSizer6.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.OnUpdata, id = self.m_menuItemdb.GetId() )
		self.Bind( wx.EVT_MENU, self.Onbaojia, id = self.m_menuItemanal1.GetId() )
		self.Bind( wx.EVT_MENU, self.Onjishi, id = self.m_menuItemanal2.GetId() )
		self.Bind( wx.EVT_MENU, self.Onjishu, id = self.m_menuItemanal3.GetId() )
		self.Bind( wx.EVT_MENU, self.Onbaobiao, id = self.m_menuItemanal4.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktfutd, id = self.m_menuItem47.GetId() )
		self.Bind(wx.EVT_MENU,self.OnChild1,self.child1)
                self.Bind(wx.EVT_MENU,self.OnChild2,self.child2)
		self.m_button119.Bind( wx.EVT_BUTTON, self.Onrefresh )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnUpdata( self, event ):
		app = wx.App()
		frame = pageupdate.MyFrameupdata(parent=None)
		frame.Show()
		app.MainLoop()

		event.Skip()
	
	def Onbaojia( self, event ):
		event.Skip()
	
	def Onjishi( self, event ):
		event.Skip()
	
	def Onjishu( self, event ):
		dayline.drawhist('000001')
		event.Skip()
	
	def Onbaobiao( self, event ):
		event.Skip()
	
	def Onmktfutd( self, event ):
		#self.frame = MyFramefutd(parent=None)
		#self.frame.Show()
		self.Refresh()
		event.Skip()

	def OnChild1(self,event):
                dlg = tools_Dialog1.SubclassDialog1()
                if dlg.ShowModal() == wx.ID_CANCEL:
                    print "cancel1"
                else:
                    print "OK1"
                #dlg = wx.SingleChoiceDialog(None,'which formula do you select?',
                 #                           'formulas manager',['3','2'])
                #if dlg.ShowModal() == wx.ID_OK:
                  #  reponse = dlg.GetStringSelection()
                #这里必须要销毁，否接不能够正常结束
                dlg.Destroy()

        def OnChild2(self,event):
                dlg = tools_Dialog2.SubclassDialog2()
                if dlg.ShowModal() == wx.ID_CANCEL:
                    print "cancel2"
                else:
                    print "OK2"
                dlg.Destroy()

	#刷新页面
	def Onrefresh( self, event ):

		#self.m_panel2.Refresh()
		event.Skip()



class MyApp(wx.App):

	def OnInit(self):
                #启动提示
                provider = wx.CreateFileTipProvider('tips.py',0)
                wx.ShowTip(None,provider,True)
		self.frame = MyFramemain(parent=None)
		self.frame.Show(True)
		#self.SetTopWindow(self.frame)
		return True
	def close(self):
		#self.frame.Close()
		self.Destroy()


if __name__ == '__main__':
	#app = wx.App()
	#frame = MyFramemain(parent=None)
	#frame.Show()
	app = MyApp(0)
	app.MainLoop()	

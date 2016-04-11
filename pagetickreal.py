# -*- coding: utf-8 -*- 

###########################################################################
## 期货日行情显示page
###########################################################################

import wx
import wx.grid

import dayline
import dialogover
import dialoging
import pageupdate
import uprealtimetick
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

import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt",charset='utf8' )
dbequ = MySQLdb.connect("127.0.0.1","root","root","db_equ",charset='utf8' )

cursor = db.cursor()
cursorequ = dbequ.cursor()
###########################################################################
## Class TestTable
###########################################################################
class TestTable(wx.grid.PyGridTableBase):#定义网格表
	def __init__(self,data):
		wx.grid.PyGridTableBase.__init__(self)
		self.colLabels =[u"股票代码",u"股票名称",u"现价",u"开盘价",u"最高价",u"最低价",u"昨日收盘价",u"成交量",u"成交金额",u"交易日期",u"时间",u"所属行业"]
		self.rowLabels = range(1,31)
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
	def GetRowLabelValue(self, row):#行标签
		return self.rowLabels[row]
	
###########################################################################
## Class MyFramemain
###########################################################################

class MyFramemain ( wx.Frame ):
	#################################
	'''app = wx.App()
	frame1 = dialoging.MyDialoging(parent=None)
	frame1.Show()
	app.MainLoop()
	'''
	uprealtimetick.ifgetrealtimetick()
	app = wx.App()
	#frame1.Hide()
	frame = dialogover.MyDialogover(parent=None)
	frame.Show()
	app.MainLoop()
	#定义获取数据
	#获取上一个非周末时间
	def getweekday(uptime):
		tradetime = uptime
		a = time.localtime()
		weekday = time.strftime("%w",a)
		
		if weekday == '6':
			tradetime = yes_time_nyr
		elif weekday == '0':
			tradetime = pre_yes_time_nyr
		return tradetime

	tradetime = getweekday(todaydate)
	
	cursor.execute("""select code,name,price,open,high,low,pre_close,volume,amount,date,time
			from tb_tickrealtime where date = %s
			order by  uploadtime DESC,code asc
			limit 30
	""",(tradetime))

	datacode = cursor.fetchall()

	global data
	#data = [[]] * 30
	data = [[] for i in range(30)]
	k=0
	for datalist in datacode:
		for j in range(0,11):
			#data[0].append(datacode[j])
			data[k].append(datalist[j])
		
		#if (len(data)>=30):
		#	break
		k=k+1
	
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
		
		'''
		self.m_grid1 = wx.grid.Grid( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.m_grid1.CreateGrid( 20, 12 )
		self.m_grid1.EnableEditing( True )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( True )
		self.m_grid1.SetMargins( 0, 0 )
		
		# Columns
		self.m_grid1.SetColSize( 0, 80 )
		self.m_grid1.SetColSize( 1, 80 )
		self.m_grid1.SetColSize( 2, 80 )
		self.m_grid1.SetColSize( 3, 80 )
		self.m_grid1.SetColSize( 4, 93 )
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelSize( 30 )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		'''
		#创建网格表
		self.grid = wx.grid.Grid(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
		
		self.table = TestTable(data)
		self.grid.SetTable(self.table, True)

		self.grid.EnableEditing( False )
		self.grid.EnableGridLines( True )
		self.grid.EnableDragGridSize( True )
		self.grid.SetColSize( 8, 100 )
		#self.grid.AutoSizeColumns()
		#self.grid.AutoSizeRows()
		self.grid.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer14.Add( self.grid, 1, wx.ALL|wx.EXPAND, 5 )
		bSizer1.Add( fgSizer14, 1, wx.EXPAND, 5 )

		'''
		# Rows
		self.m_grid1.SetRowSize( 0, 20 )
		self.m_grid1.SetRowSize( 1, 20 )
		self.m_grid1.SetRowSize( 2, 20 )
		self.m_grid1.SetRowSize( 3, 20 )
		self.m_grid1.SetRowSize( 4, 20 )
		self.m_grid1.AutoSizeRows()
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelSize( 80 )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		fgSizer14.Add( self.m_grid1, 1, wx.ALL|wx.EXPAND, 5 )
		'''
		

		
		
		self.m_staticline17 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )
		'''
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button6 = wx.Button( self.m_panel2, wx.ID_ANY, u"button", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_button6, 0, wx.ALIGN_RIGHT|wx.ALL|wx.BOTTOM, 5 )
		
		bSizer1.Add( bSizer17, 0, wx.ALIGN_RIGHT, 5 )
		
		self.m_staticline18 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline18, 0, wx.EXPAND |wx.ALL, 5 )
		'''
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
	
	#刷新页面
	def Onrefresh( self, event ):

		self.m_panel2.Refresh()
		#event.Skip()
	



if __name__ == '__main__':
	app = wx.App()
	frame = MyFramemain(parent=None)
	frame.Show()
	app.MainLoop()	

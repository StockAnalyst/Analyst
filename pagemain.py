# -*- coding: utf-8 -*- 

###########################################################################
## mainpage
###########################################################################

import wx
import wx.grid

import timecheck
import checktddata
import mkt
import dayline
import dialogover
import dialoging
import pageupdate
import uprealtimetick
import dbinfo
import draw_Dayline

import tools_Dialog1
import tools_Dialog2
import f10_display
import f10_with_processbar_final

import typedata 
import typeinfo

import time
todaydate = time.strftime('%Y-%m-%d')
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
		return len(self.data[0])
	def IsEmptyCell(self, row, col):
		#return self.data.get((row, col)) is not None
		return False
	def GetValue(self, row, col):#为网格提供数据
		if self.data[row][col] is None:
			return ''
		else:
			return self.data[row][col]

	def SetValue(self, row, col, value):#给表赋值
		self.data[(row,col)] = value
		#pass
	def GetColLabelValue(self, col):#列标签
		return self.colLabels[col]
	#def GetRowLabelValue(self, row):#行标签
	#	return self.rowLabels[row]
	def MovePageDown():
		pass
	def MovePageUp():
		pass

	
###############################################
###排序模块
###############################################
def sortMin(data,col,dataSort):
    data_temp = []
    for data1 in data:
        data_temp.append(data1)
    while len(data_temp):
        min1 = data_temp[0]
        for data1 in data_temp:
            if data1[col] < min1[col]:
                min1 = data1
        #dataSortBigger[col].append(min1)
        dataSort.append(min1)
        data_temp.remove(min1)

#按照从小到大排序
class LineupTableBigger(wx.grid.PyGridTableBase): 
    
    def __init__(self,dataSort,colLabels):
        wx.grid.PyGridTableBase.__init__(self)
        self.colLabels = colLabels
        self.dataSort = dataSort

    def GetNumberRows(self):
        return len(self.dataSort)    
    def GetNumberCols(self):
        return len(self.dataSort[0])
    def GetColLabelValue(self,col):
        return self.colLabels[col]
    def IsEmptyCell(self,row,col):
        return False
    def GetValue(self,row,col):
        return self.dataSort[row][col]
    def SetValue(self,row,col,value):
        pass

#按照从大到小排序
def sortMax(data,col,dataSortSmaller):
    data_temp = []
    for data1 in data:
        data_temp.append(data1)
    while len(data_temp):
        max1 = data_temp[0]
        for data1 in data_temp:
            if data1[col] > max1[col]:
                max1 = data1
        #dataSortSmaller[col].append(max1)
        dataSortSmaller.append(max1)
        data_temp.remove(max1)

#按照从大到小排序
class LineupTableSmaller(wx.grid.PyGridTableBase): 
    
    def __init__(self,dataSortSmaller,colLabels):
        wx.grid.PyGridTableBase.__init__(self)
        self.colLabels = colLabels
        self.dataSortSmaller = dataSortSmaller

    def GetNumberRows(self):
        return len(self.dataSortSmaller)
    def GetNumberCols(self):
        return len(self.dataSortSmaller[0])
    def GetColLabelValue(self,col):
        return self.colLabels[col]
    def IsEmptyCell(self,row,col):
        return False
    def GetValue(self,row,col):
        return self.dataSortSmaller[row][col]
    def SetValue(self,row,col,value):
        pass


###########################################################################
## Class MyFramemain
##main:沪深股票日行情
###########################################################################

class MyFramemain ( wx.Frame ):

	def __init__( self, parent ):
		
		#定义获取数据
		tradetime = timecheck.getweekday(todaydate,'1530')
		#cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd group by tradeDate order by tradeDate desc
		#				""")
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd where tradeDate=%s
						""",(tradetime))
		#tradetimesql = cursor.fetchone()
		#print tradetime
		#print tradetimesql[0]
		#if tradetime != tradetimesql[0] :
		counttoday = 0
		i = 0
		counttoday += cursor.rowcount
		print counttoday
		while (counttoday == 0 and i < 2):
			'''
			app = wx.App()
			frame1 = dialoging.MyDialoging(parent=None)
			frame1.Show()
			app.MainLoop()'''
			#print tradetime
			inputtradetime = timecheck.chgtimefor(tradetime)
			#print inputtradetime
			mkt.mktequd(inputtradetime)
			cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd where tradeDate=%s
						""",(tradetime))
			counttoday += cursor.rowcount
			print counttoday
			if counttoday == 0 :
				tradetime = timecheck.getyesday(tradetime)
				cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktequd where tradeDate=%s
						""",(tradetime))
				if cursor.rowcount > 0:
					break
			print tradetime
			i += 1
		
		'''app = wx.App()
		#frame1.Close()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()'''


		cursor.execute("""select ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				from mkt_mktequd where tradeDate = %s
				order by ticker asc
				limit 50
		""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		global data
		data = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,17):
				data[k].append(datalist[j])
			k=k+1
		#将ticker的显示数前面补0
		for i in range(0,count):
			data[i][0]= "%06d" % data[i][0]

		global colLabels
		colLabels =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
			u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
			
		#print len(colLabels)
		global colnum,dataSortBigger,dataSortSmaller
		colnum = len(data[0])
		#print colnum
		dataSortBigger = [[]for i in range(colnum)]
		dataSortSmaller = [[]for i in range(colnum)]
		
		for i in range(0,colnum):
			sortMin(data,i,dataSortBigger[i])
			sortMax(data,i,dataSortSmaller[i])
		#print dataSortBigger

		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"沪深股票日行情", pos = wx.DefaultPosition, size = wx.Size( 1200,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		#id = frame.GetId()
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuupdb = wx.Menu()
		self.m_menuupdb.AppendSeparator()
		
		self.m_menuItemdb = wx.MenuItem( self.m_menuupdb, wx.ID_ANY, u"选择更新数据库", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuupdb.AppendItem( self.m_menuItemdb )

		self.m_menuItemdbsta = wx.MenuItem( self.m_menuupdb, wx.ID_ANY, u"查看数据库状态", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuupdb.AppendItem( self.m_menuItemdbsta )
		
		self.m_menuupdb.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuupdb, u"数据库操作" ) 
		
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
		
		self.m_menuday = wx.Menu()
		self.m_menuday.AppendSeparator()
		self.m_menu11 = wx.Menu()
		self.m_menuItem79 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"全部沪深股", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem79 )
		
		self.m_menuItem4711 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"A股", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem4711 )
		
		self.m_menuItem481 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"中小板", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem481 )
		
		self.m_menuItem491 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"创业板", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem491 )
		
		self.m_menuItem501 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"B股", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem501 )
		'''
		self.m_menuItem511 = wx.MenuItem( self.m_menu11, wx.ID_ANY, u"三板", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu11.AppendItem( self.m_menuItem511 )
		'''
		self.m_menuday.AppendSubMenu( self.m_menu11, u"沪深股" )
		
		self.m_menu51 = wx.Menu()
		self.m_menuItem86 = wx.MenuItem( self.m_menu51, wx.ID_ANY, u"全部基金", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu51.AppendItem( self.m_menuItem86 )

		self.m_menuItem461 = wx.MenuItem( self.m_menu51, wx.ID_ANY, u"LOF", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu51.AppendItem( self.m_menuItem461 )
		
		self.m_menuItem531 = wx.MenuItem( self.m_menu51, wx.ID_ANY, u"ETF", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu51.AppendItem( self.m_menuItem531 )
		
		self.m_menuItem541 = wx.MenuItem( self.m_menu51, wx.ID_ANY, u"上证基金", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu51.AppendItem( self.m_menuItem541 )
		
		self.m_menuItem551 = wx.MenuItem( self.m_menu51, wx.ID_ANY, u"深证基金", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu51.AppendItem( self.m_menuItem551 )
		
		
		self.m_menuday.AppendSubMenu( self.m_menu51, u"基金" )
		
		self.m_menu251 = wx.Menu()
		self.m_menuItem87 = wx.MenuItem( self.m_menu251, wx.ID_ANY, u"全部债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu251.AppendItem( self.m_menuItem87 )
		
		self.m_menuItem92 = wx.MenuItem( self.m_menu251, wx.ID_ANY, u"银行间债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu251.AppendItem( self.m_menuItem92 )
		
		self.m_menuItem93 = wx.MenuItem( self.m_menu251, wx.ID_ANY, u"上证债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu251.AppendItem( self.m_menuItem93 )
		
		self.m_menuItem94 = wx.MenuItem( self.m_menu251, wx.ID_ANY, u"深证债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu251.AppendItem( self.m_menuItem94 )
		
		
		self.m_menuday.AppendSubMenu( self.m_menu251, u"债券" )
		
		self.m_menu261 = wx.Menu()
		self.m_menuItem88 = wx.MenuItem( self.m_menu261, wx.ID_ANY, u"全部期货", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu261.AppendItem( self.m_menuItem88 )
		'''
		self.m_menuItem95 = wx.MenuItem( self.m_menu261, wx.ID_ANY, u"中金所", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu261.AppendItem( self.m_menuItem95 )
		'''
		self.m_menuItem96 = wx.MenuItem( self.m_menu261, wx.ID_ANY, u"上海期货", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu261.AppendItem( self.m_menuItem96 )
		
		self.m_menuItem97 = wx.MenuItem( self.m_menu261, wx.ID_ANY, u"大连商品", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu261.AppendItem( self.m_menuItem97 )
		
		self.m_menuItem98 = wx.MenuItem( self.m_menu261, wx.ID_ANY, u"郑州商品", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu261.AppendItem( self.m_menuItem98 )
		
		
		self.m_menuday.AppendSubMenu( self.m_menu261, u"期货" )
		
		self.m_menu241 = wx.Menu()
		self.m_menuItem89 = wx.MenuItem( self.m_menu241, wx.ID_ANY, u"上证全部期权", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu241.AppendItem( self.m_menuItem89 )
		'''
		self.m_menuItem99 = wx.MenuItem( self.m_menu241, wx.ID_ANY, u"上证期权", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu241.AppendItem( self.m_menuItem99 )
		
		self.m_menuItem100 = wx.MenuItem( self.m_menu241, wx.ID_ANY, u"期权标的", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu241.AppendItem( self.m_menuItem100 )'''
		
		
		self.m_menuday.AppendSubMenu( self.m_menu241, u"期权" )
		
		self.m_menu221 = wx.Menu()
		self.m_menuday.AppendSubMenu( self.m_menu221, u"港股" )
		
		self.m_menuday.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuday, u"日行情显示" ) 
		
		self.m_menureal = wx.Menu()
		self.m_menureal.AppendSeparator()
		
		self.m_menuItem110 = wx.MenuItem( self.m_menureal, wx.ID_ANY, u"大盘指数实时行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menureal.AppendItem( self.m_menuItem110 )
		
		self.m_menuItem111 = wx.MenuItem( self.m_menureal, wx.ID_ANY, u"指数实时分笔", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menureal.AppendItem( self.m_menuItem111 )
		
		self.m_menu1 = wx.Menu()
		self.m_menuItem791 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"全部沪深股", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem791 )
		
		self.m_menuItem471 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"A股", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem471 )
		
		self.m_menuItem48 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"中小板", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem48 )
		
		self.m_menuItem49 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"创业板", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem49 )
		
		self.m_menuItem50 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"B股", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem50 )
		'''
		self.m_menuItem51 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"三板", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem51 )
		'''
		
		self.m_menureal.AppendSubMenu( self.m_menu1, u"沪深股" )
		
		self.m_menu5 = wx.Menu()

		self.m_menuItem861 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"全部基金", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.AppendItem( self.m_menuItem861 )

		self.m_menuItem46 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"LOF", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.AppendItem( self.m_menuItem46 )
		
		self.m_menuItem53 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"ETF", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.AppendItem( self.m_menuItem53 )
		
		self.m_menuItem54 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"上证基金", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.AppendItem( self.m_menuItem54 )
		
		self.m_menuItem55 = wx.MenuItem( self.m_menu5, wx.ID_ANY, u"深证基金", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu5.AppendItem( self.m_menuItem55 )
		
		
		self.m_menureal.AppendSubMenu( self.m_menu5, u"基金" )
		
		self.m_menu25 = wx.Menu()
		self.m_menuItem871 = wx.MenuItem( self.m_menu25, wx.ID_ANY, u"全部债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu25.AppendItem( self.m_menuItem871 )
		
		self.m_menuItem921 = wx.MenuItem( self.m_menu25, wx.ID_ANY, u"银行间债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu25.AppendItem( self.m_menuItem921 )
		
		self.m_menuItem931 = wx.MenuItem( self.m_menu25, wx.ID_ANY, u"上证债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu25.AppendItem( self.m_menuItem931 )
		
		self.m_menuItem941 = wx.MenuItem( self.m_menu25, wx.ID_ANY, u"深证债券", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu25.AppendItem( self.m_menuItem941 )
		
		self.m_menureal.AppendSubMenu( self.m_menu25, u"债券" )
		
		self.m_menu26 = wx.Menu()
		self.m_menuItem881 = wx.MenuItem( self.m_menu26, wx.ID_ANY, u"全部期货", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu26.AppendItem( self.m_menuItem881 )
		'''
		self.m_menuItem951 = wx.MenuItem( self.m_menu26, wx.ID_ANY, u"中金所", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu26.AppendItem( self.m_menuItem951 )'''
		
		self.m_menuItem961 = wx.MenuItem( self.m_menu26, wx.ID_ANY, u"上海期货", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu26.AppendItem( self.m_menuItem961 )
		
		self.m_menuItem971 = wx.MenuItem( self.m_menu26, wx.ID_ANY, u"大连商品", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu26.AppendItem( self.m_menuItem971 )
		
		self.m_menuItem981 = wx.MenuItem( self.m_menu26, wx.ID_ANY, u"郑州商品", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu26.AppendItem( self.m_menuItem981 )
		
		self.m_menureal.AppendSubMenu( self.m_menu26, u"期货" )
		
		self.m_menu24 = wx.Menu()
		self.m_menuItem891 = wx.MenuItem( self.m_menu24, wx.ID_ANY, u"上证全部期权", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu24.AppendItem( self.m_menuItem891 )
		'''
		self.m_menuItem991 = wx.MenuItem( self.m_menu24, wx.ID_ANY, u"上证期权", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu24.AppendItem( self.m_menuItem991 )
		
		self.m_menuItem1001 = wx.MenuItem( self.m_menu24, wx.ID_ANY, u"期权标的", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu24.AppendItem( self.m_menuItem1001 )'''
		
		self.m_menureal.AppendSubMenu( self.m_menu24, u"期权" )
		
		self.m_menu22 = wx.Menu()
		self.m_menureal.AppendSubMenu( self.m_menu22, u"港股" )
		
		self.m_menureal.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menureal, u"实时行情显示" ) 
		
		self.m_menuboard = wx.Menu()
		self.m_menuboard.AppendSeparator()
		
		self.m_menu211 = wx.Menu()
		self.m_menuItem106 = wx.MenuItem( self.m_menu211, wx.ID_ANY, u"全部行业板块", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu211.AppendItem( self.m_menuItem106 )
		
		self.m_menuboard.AppendSubMenu( self.m_menu211, u"行业板块" )
		
		self.m_menu171 = wx.Menu()
		self.m_menuItem107 = wx.MenuItem( self.m_menu171, wx.ID_ANY, u"全部地区板块", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu171.AppendItem( self.m_menuItem107 )
		
		self.m_menuboard.AppendSubMenu( self.m_menu171, u"地区板块" )
		
		self.m_menu81 = wx.Menu()
		self.m_menuItem109 = wx.MenuItem( self.m_menu81, wx.ID_ANY, u"全部概念板块", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu81.AppendItem( self.m_menuItem109 )
		
		self.m_menuboard.AppendSubMenu( self.m_menu81, u"概念板块" )
		
		self.m_menu161 = wx.Menu()
		self.m_menuItem108 = wx.MenuItem( self.m_menu161, wx.ID_ANY, u"全部指数", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu161.AppendItem( self.m_menuItem108 )
		'''
		self.m_menuItem110 = wx.MenuItem( self.m_menu161, wx.ID_ANY, u"大盘指数", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu161.AppendItem( self.m_menuItem110 )
		'''

		self.m_menuboard.AppendSubMenu( self.m_menu161, u"指数板块" )
		
		
		self.m_menuboard.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuboard, u"板块" ) 
		
		self.m_menutools = wx.Menu()
		self.m_menutools.AppendSeparator()
		self.child1 = self.m_menutools.Append(-1,u'公式管理器','there are lots of formulas')
		self.child2 = self.m_menutools.Append(-1,u'模板管理器','there are lots of templates')
		self.m_menutools.AppendSeparator()
		self.m_menubar1.Append(self.m_menutools, u'工具')
		
		'''self.menu4 = wx.Menu()
		self.child3 = wx.MenuItem(self.menu4,1,u'&个股数据\tF10')
        self.menu4.AppendItem(child3)
        self.menu4.AppendSeparator()
        self.child4 = wx.Menu()
        self.child4_1=self.child4.Append(-1,u'更新所有')
        self.child4_2=self.child4.Append(-1,u'更新SZ板块')
        self.child4_3=self.child4.Append(-1,u'更新SH板块')
        #注意区别的是，这里用appendmenu而不是appenditem
        self.menu4.AppendMenu(-1,u'更新个股资料',self.child4)
		self.m_menubar1.Append(self.menu4,u'微系统')
		self.SetMenuBar( self.m_menubar1 )
		'''
		self.m_menu18 = wx.Menu()
		self.m_menu18.AppendSeparator()
		
		self.m_menuItem942 = wx.MenuItem( self.m_menu18, wx.ID_ANY, u"个股数据\tF10", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu18.AppendItem( self.m_menuItem942 )
		
		self.m_menu17 = wx.Menu()
		self.m_menuItem952 = wx.MenuItem( self.m_menu17, wx.ID_ANY, u"更新所有", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu17.AppendItem( self.m_menuItem952 )
		
		self.m_menuItem962 = wx.MenuItem( self.m_menu17, wx.ID_ANY, u"更新SZ板块", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu17.AppendItem( self.m_menuItem962 )
		
		self.m_menuItem972 = wx.MenuItem( self.m_menu17, wx.ID_ANY, u"更新SH板块", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu17.AppendItem( self.m_menuItem972 )
		
		self.m_menu18.AppendSubMenu( self.m_menu17, u"更新个股资料" )
		
		self.m_menubar1.Append( self.m_menu18, u"微系统" ) 

		self.SetMenuBar( self.m_menubar1 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline33 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline33, 0, wx.EXPAND |wx.ALL, 5 )
		
		
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
		self.Bind( wx.EVT_MENU, self.OnDbinfo, id = self.m_menuItemdbsta.GetId() )
		self.Bind( wx.EVT_MENU, self.Onbaojia, id = self.m_menuItemanal1.GetId() )
		self.Bind( wx.EVT_MENU, self.Onjishi, id = self.m_menuItemanal2.GetId() )
		self.Bind( wx.EVT_MENU, self.Onjishu, id = self.m_menuItemanal3.GetId() )
		self.Bind( wx.EVT_MENU, self.Onbaobiao, id = self.m_menuItemanal4.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMktEqud, id = self.m_menuItem79.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAshare, id = self.m_menuItem4711.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSME, id = self.m_menuItem481.GetId() )
		self.Bind( wx.EVT_MENU, self.OnGEM, id = self.m_menuItem491.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBShare, id = self.m_menuItem501.GetId() )
		#self.Bind( wx.EVT_MENU, self.On3Board, id = self.m_menuItem511.GetId() )
		
		self.Bind( wx.EVT_MENU, self.OnMktFund, id = self.m_menuItem86.GetId() )
		self.Bind( wx.EVT_MENU, self.OnFundLOF, id = self.m_menuItem461.GetId() )
		self.Bind( wx.EVT_MENU, self.OnFundETF, id = self.m_menuItem531.GetId() )
		self.Bind( wx.EVT_MENU, self.OnFundShang, id = self.m_menuItem541.GetId() )
		self.Bind( wx.EVT_MENU, self.OnFundShen, id = self.m_menuItem551.GetId() )
		
		self.Bind( wx.EVT_MENU, self.OnMktBondd, id = self.m_menuItem87.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBonddbank, id = self.m_menuItem92.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBonddShang, id = self.m_menuItem93.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBonddShen, id = self.m_menuItem94.GetId() )
		
		self.Bind( wx.EVT_MENU, self.OnMktFutd, id = self.m_menuItem88.GetId() )
		#self.Bind( wx.EVT_MENU, self.OnFutdzjs, id = self.m_menuItem95.GetId() )
		self.Bind( wx.EVT_MENU, self.OnFutdsh, id = self.m_menuItem96.GetId() )
		self.Bind( wx.EVT_MENU, self.OnFutddl, id = self.m_menuItem97.GetId() )
		self.Bind( wx.EVT_MENU, self.OnFutdzz, id = self.m_menuItem98.GetId() )
		
		self.Bind( wx.EVT_MENU, self.OnMktOptd, id = self.m_menuItem89.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMktIndex, id = self.m_menuItem110.GetId() )
		self.Bind( wx.EVT_MENU, self.OnIndexReal, id = self.m_menuItem111.GetId() )
		
		self.Bind( wx.EVT_MENU, self.OnMktIdxd, id = self.m_menuItem108.GetId() )
		self.Bind( wx.EVT_MENU, self.OnTypeIndustry, id = self.m_menuItem106.GetId() )
		self.Bind( wx.EVT_MENU, self.OnTyeArea, id = self.m_menuItem107.GetId() )
		self.Bind( wx.EVT_MENU, self.OnTypeConcept, id = self.m_menuItem109.GetId() )
		self.Bind(wx.EVT_MENU,self.OnChild1,self.child1)
		self.Bind(wx.EVT_MENU,self.OnChild2,self.child2)
		self.Bind( wx.EVT_MENU, self.OnChild3, id = self.m_menuItem942.GetId() )
		self.Bind( wx.EVT_MENU, self.OnChild4_1, id = self.m_menuItem952.GetId() )
		self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK,lambda evt,dataSortBigger=dataSortBigger,colLabels=colLabels:self.OnLeftClick(evt,dataSortBigger,colLabels))
		self.grid.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK,lambda evt,dataSortSmaller=dataSortSmaller,colLabels=colLabels:self.OnRightClick(evt,dataSortSmaller,colLabels))
		#self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.OnShowType)
		self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.OnShowDayline)
		self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.OnChild3_1)

		'''
		rowindex = event.GetRow()
		colindex = event.GetCol()
		value = self.table.GetValue(rowindex,rowindex)
		print value
		self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,lambda evt,value=value:self.OnShowDayline)
		'''
	def __del__( self ):
		pass
	

	def OnLeftClick(self,event,dataSort,colLabels):
		for i in range(0,colnum):
			if event.GetCol()==i:
				self.grid.SetTable(LineupTableBigger(dataSort[i],colLabels))
				self.grid.AutoSize()
				self.grid.Refresh()

	def OnRightClick(self,event,dataSort,colLabels):
		for i in range(0,colnum):
			if event.GetCol()==i:
				self.grid.SetTable(LineupTableSmaller(dataSort[i],colLabels))
				self.grid.AutoSize()
				self.grid.Refresh()
	def allsort(self,colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,dtag):
		for i in range(0,colnum):
			sortMin(data1,i,dataSortBigger1[i])
			sortMax(data1,i,dataSortSmaller1[i])
		
		self.table = TestTable(data1,colLabels1)
		self.grid.SetTable(self.table, True)
		#self.grid.AutoSize()
		self.grid.Refresh()
		self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK,lambda evt,dataSortBigger1=dataSortBigger1,colLabels1=colLabels1:self.OnLeftClick(evt,dataSortBigger1,colLabels1))
		self.grid.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK,lambda evt,dataSortSmaller1=dataSortSmaller1,colLabels1=colLabels1:self.OnRightClick(evt,dataSortSmaller1,colLabels1))
		#if dtag == 1:
			#self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.OnShowType)
		#if dtag == 0:
		#	self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.OnShowDayline)
			

	# Virtual event handlers, overide them in your derived class
	#数据库更新页面
	def OnUpdata( self, event ):
		app = wx.App()
		frame = pageupdate.MyFrameupdata(parent=None)
		frame.Show()
		app.MainLoop()

		event.Skip()
	
	def OnDbinfo(self,event):
		pp = wx.App()
		frame = dbinfo.FrameDBinfo(parent=None)
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
	
	##全部沪深股日行情	
	def OnMktEqud( self, event ):
		self.table = TestTable(data,colLabels)
		self.grid.SetTable(self.table, True)
		#self.grid.AutoSize()
		self.grid.Refresh()

	##全部A股日行情
	def OnAshare( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1530')
		tradetime = checktddata.check_mktequd(tradetime)
		cursor.execute( """SELECT mkt_mktequd.ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				 FROM mkt_mktequd,type_ashare
				 WHERE tradeDate = %s
				 AND mkt_mktequd.ticker = type_ashare.tickerint
				 order by ticker asc
		""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,17):
				data1[k].append(datalist[j])
			k=k+1
		for i in range(0,count):
			data1[i][0]= "%06d" % data1[i][0]
		colLabels1 =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
			u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		#colLabels1 = colLabels	
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,0)
		
		#self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.OnShowDayline)
		

	##全部中小板日行情
	def OnSME( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1530')
		tradetime = checktddata.check_mktequd(tradetime)
		cursor.execute( """SELECT ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				 FROM mkt_mktequd 
				 WHERE tradeDate = %s
				 AND secID REGEXP '^002'
				 order by ticker asc
				 limit 100
		""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,17):
				data1[k].append(datalist[j])
			k=k+1
		for i in range(0,count):
			data1[i][0]= "%06d" % data1[i][0]
		colLabels1 =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
			u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,0)
		
	##全部创业板日行情
	def OnGEM( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1530')
		tradetime = checktddata.check_mktequd(tradetime)
		cursor.execute( """SELECT ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				 FROM mkt_mktequd 
				 WHERE tradeDate = %s
				 AND secID REGEXP '^300'
				 order by ticker asc
				 limit 100
		""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,17):
				data1[k].append(datalist[j])
			k=k+1
		for i in range(0,count):
			data1[i][0]= "%06d" % data1[i][0]
		colLabels1 =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
			u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,0)
		
	
	def OnBShare( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1530')
		tradetime = checktddata.check_mktequd(tradetime)
		cursor.execute( """SELECT mkt_mktequd.ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				 FROM mkt_mktequd,type_bshare
				 WHERE tradeDate = %s
				 AND mkt_mktequd.ticker = type_bshare.tickerint
				 order by ticker asc
		""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,17):
				data1[k].append(datalist[j])
			k=k+1
		for i in range(0,count):
			data1[i][0]= "%06d" % data1[i][0]
		colLabels1 =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
			u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		#colLabels1 = colLabels	
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,0)
		
	
	def On3Board( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1530')
		tradetime = checktddata.check_mktequd(tradetime)
		cursor.execute( """SELECT mkt_mktequd.ticker,mkt_mktequd.secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				 FROM mkt_mktequd,sec_typerel
				 WHERE tradeDate = %s
				 AND concat(mkt_mktequd.ticker,'') = sec_typerel.ticker and typeID = '101001001012'
				 order by ticker asc
		""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,17):
				data1[k].append(datalist[j])
			k=k+1
		for i in range(0,count):
			data1[i][0]= "%06d" % data1[i][0]
		colLabels1 =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
			u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		#colLabels1 = colLabels	
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,0)
		
	global colLabelsfund
	colLabelsfund =[u"基金交易代码",u"证券简称",u"昨日收盘价",u"今日开盘价",u"最高价",u"最低价",u"今日收盘价",
			u"成交量",u"成交金额",u"涨跌",u"涨跌幅",u"流通份额",u"累积复权因子",u"交易日期"]	
		
	##全部基金日行情
	def OnMktFund( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfundd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfundd(inputtradetime)
			'''app = wx.App()
			frame = dialogover.MyDialogover(parent=None)
			frame.Show()
			app.MainLoop()'''
			
		cursor.execute("""select ticker,secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,CHG,CHGPct,circulationShares,accumAdjFactor,tradeDate
					from mkt_mktfundd where tradeDate = %s
					order by ticker asc
					limit 606
			""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,14):
				data1[k].append(datalist[j])
			k=k+1
		
		
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfund,0)
	##LOF基金日行情
	def OnFundLOF( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfundd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfundd(inputtradetime)
			
		cursor.execute("""SELECT mkt_mktfundd.ticker,mkt_mktfundd.secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,CHG,CHGPct,circulationShares,accumAdjFactor,tradeDate
					FROM mkt_mktfundd,sec_typerel 
					where tradeDate = %s 
					AND CONCAT( mkt_mktfundd.ticker,'' ) = sec_typerel.ticker 
					AND typeID = '101003001001'
					order by ticker asc
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,14):
				data1[k].append(datalist[j])
			k=k+1
		
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfund,0)	
	##ETF基金日行情
	def OnFundETF( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfundd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfundd(inputtradetime)
			
		cursor.execute("""SELECT mkt_mktfundd.ticker,mkt_mktfundd.secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,CHG,CHGPct,circulationShares,accumAdjFactor,tradeDate
					FROM mkt_mktfundd,sec_typerel 
					where tradeDate = %s 
					AND CONCAT( mkt_mktfundd.ticker,'' ) = sec_typerel.ticker 
					AND typeID = '101003001002'
					order by ticker asc
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,14):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfund,0)	
	##上证基金日行情
	def OnFundShang( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfundd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfundd(inputtradetime)
			
		cursor.execute("""SELECT mkt_mktfundd.ticker,mkt_mktfundd.secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,CHG,CHGPct,circulationShares,accumAdjFactor,tradeDate
					FROM mkt_mktfundd,sec_typerel 
					where tradeDate = %s 
					AND CONCAT( mkt_mktfundd.ticker,'' ) = sec_typerel.ticker 
					AND typeID = '101003001003'
					order by ticker asc
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,14):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfund,0)	
	##深证基金日行情
	def OnFundShen( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfundd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfundd(inputtradetime)
			
		cursor.execute("""SELECT mkt_mktfundd.ticker,mkt_mktfundd.secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,CHG,CHGPct,circulationShares,accumAdjFactor,tradeDate
					FROM mkt_mktfundd,sec_typerel 
					where tradeDate = %s 
					AND CONCAT( mkt_mktfundd.ticker,'' ) = sec_typerel.ticker 
					AND typeID = '101003001004'
					order by ticker asc
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,14):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfund,0)	

	global colLabelsbondd
	colLabelsbondd =[u"债券交易代码",u"债券简称",u"昨日收盘价",u"今日开盘价",u"最高价",u"最低价",u"今日收盘价",
	u"成交量",u"成交金额",u"成交笔数",u"应计利息",u"到期收益率",u"交易日期"]	

	##全部债券日行情
	def OnMktBondd( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktbondd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktbondd(inputtradetime)
			'''app = wx.App()
			frame = dialogover.MyDialogover(parent=None)
			frame.Show()
			app.MainLoop()'''
			
		cursor.execute("""SELECT ticker,secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,dealAmount,accrInterest,YTM,tradeDate
					from mkt_mktbondd where tradeDate = %s
					order by ticker asc
					limit 100
			""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,13):
				data1[k].append(datalist[j])
			k=k+1
		
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsbondd,0)
	##银行间债券日行情
	def OnBonddbank( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktbondd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktbondd(inputtradetime)	
		cursor.execute("""SELECT mkt_mktbondd.ticker,mkt_mktbondd.secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,dealAmount,accrInterest,YTM,tradeDate
					from mkt_mktbondd,sec_typerel 
					where tradeDate = %s
					AND concat(mkt_mktbondd.ticker,'') = sec_typerel.ticker 
					AND typeID = '101004001001001'
					order by mkt_mktbondd.ticker asc
					limit 100
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,13):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsbondd,0)
	##上证债券日行情
	def OnBonddShang( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktbondd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktbondd(inputtradetime)	
		cursor.execute("""SELECT mkt_mktbondd.ticker,mkt_mktbondd.secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,dealAmount,accrInterest,YTM,tradeDate
					from mkt_mktbondd,sec_typerel 
					where tradeDate = %s
					AND concat(mkt_mktbondd.ticker,'') = sec_typerel.ticker 
					AND typeID = '101004001002001'
					order by mkt_mktbondd.ticker asc
					limit 100
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,13):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsbondd,0)
	##深证债券日行情
	def OnBonddShen( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktbondd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktbondd(inputtradetime)	
		cursor.execute("""SELECT mkt_mktbondd.ticker,mkt_mktbondd.secShortName,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,turnoverVol,turnoverValue,dealAmount,accrInterest,YTM,tradeDate
					from mkt_mktbondd,sec_typerel 
					where tradeDate = %s
					AND concat(mkt_mktbondd.ticker,'') = sec_typerel.ticker 
					AND typeID = '101004001003001'
					order by mkt_mktbondd.ticker asc
					limit 100
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,13):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsbondd,0)
	global colLabelsfutd
	colLabelsfutd =[u"合约代码",u"合约简称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"昨日结算价",u"今日收盘价",
		u"今日结算价",u"成交量",u"成交金额",u"持仓量",u"涨跌",u"涨跌幅",u"交易日期"]	
				
	##全部期货日行情	
	def OnMktFutd( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1800')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfutd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			#app = wx.App()
			#frame1 = dialoging.MyDialoging(parent=None)
			#frame1.Show()
			#app.MainLoop()
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfutd(inputtradetime)
			'''app = wx.App()
			#frame1.Close()
			frame = dialogover.MyDialogover(parent=None)
			frame.Show()
			app.MainLoop()'''
			
		cursor.execute("""SELECT ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,preSettlePrice,
				closePrice,settlePrice,turnoverVol,turnoverValue,openInt,CHG,CHGPct,tradeDate
					from mkt_mktfutd where tradeDate = %s
					order by ticker asc
					limit 474
			""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		#global data1
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,15):
				data1[k].append(datalist[j])
			k=k+1
		
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		#print dataSortBigger1[0]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfutd,0)
	##上期所期货日行情	
	def OnFutdsh( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1800')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfutd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfutd(inputtradetime)
		cursor.execute("""SELECT mkt_mktfutd.ticker,mkt_mktfutd.secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,preSettlePrice,
				closePrice,settlePrice,turnoverVol,turnoverValue,openInt,CHG,CHGPct,tradeDate
					FROM mkt_mktfutd,sec_typerel  
					WHERE tradeDate = %s
					AND mkt_mktfutd.ticker = sec_typerel.ticker 
					AND typeID = '101005002001'
					order by ticker asc
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,15):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfutd,0)
	##大商所期货日行情	
	def OnFutddl( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1800')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfutd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfutd(inputtradetime)
		cursor.execute("""SELECT mkt_mktfutd.ticker,mkt_mktfutd.secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,preSettlePrice,
				closePrice,settlePrice,turnoverVol,turnoverValue,openInt,CHG,CHGPct,tradeDate
					FROM mkt_mktfutd,sec_typerel  
					WHERE tradeDate = %s
					AND mkt_mktfutd.ticker = sec_typerel.ticker 
					AND typeID = '101005003001'
					order by ticker asc
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,15):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfutd,0)
	##郑商所期货日行情	
	def OnFutdzz( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1800')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktfutd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktfutd(inputtradetime)
		cursor.execute("""SELECT mkt_mktfutd.ticker,mkt_mktfutd.secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,preSettlePrice,
				closePrice,settlePrice,turnoverVol,turnoverValue,openInt,CHG,CHGPct,tradeDate
					FROM mkt_mktfutd,sec_typerel  
					WHERE tradeDate = %s
					AND mkt_mktfutd.ticker = sec_typerel.ticker 
					AND typeID = '101005004001'
					order by ticker asc
			""",(tradetime))
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,15):
				data1[k].append(datalist[j])
			k=k+1
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabelsfutd,0)
		
	##全部期权日行情
	def OnMktOptd( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktoptd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktoptd(inputtradetime)
			'''app = wx.App()
			frame = dialogover.MyDialogover(parent=None)
			frame.Show()
			app.MainLoop()'''
			
		cursor.execute("""select ticker,secShortName,preSettlePrice,preClosePrice,openPrice,highestPrice,lowestPrice,
				closePrice,settlPrice,turnoverVol,turnoverValue,openInt,tradeDate
					from mkt_mktoptd where tradeDate = %s
					order by ticker asc
					limit 156
			""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		#global data1
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,13):
				data1[k].append(datalist[j])
			k=k+1
		#global colLabels1
		colLabels1 =[u"合约交易代码",u"证券简称",u"前结算价",u"昨日收盘价",u"今日开盘价",u"最高价",u"最低价",u"今日收盘价",
			u"结算价",u"成交量",u"成交金额",u"持仓量",u"交易日期"]	

		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,0)
		
	
	##大盘指数实时行情
	def OnMktIndex( self, event ):
		
		tradetime = timecheck.getweekday(todaydate,'0930')
		#cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktindex group by tradeDate order by tradeDate desc
		#			""")
		#tradetimesql = cursor.fetchone()
		#if tradetime != tradetimesql[0]:
		#timeArray = time.strptime(tradetime,'%Y-%m-%d')
		#inputtradetime = time.strftime('%Y%m%d',timeArray)
		mkt.mktindex(todaydate)
		'''app = wx.App()
			frame = dialogover.MyDialogover(parent=None)
			frame.Show()
			app.MainLoop()'''
			
		cursor.execute("""SELECT code,name,preclose,open,high,
						low,close,volume,amount,`change`,tradeDate,tradeTimehm
					from mkt_mktindex where tradeDate = %s
					order by code asc
				
			""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		#print count
		#global data1
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,12):
				data1[k].append(datalist[j])
			k=k+1
		#global colLabels1
		colLabels1 =[u"指数代码",u"指数名称",u"昨收盘点位",u"今开盘点位",u"最高点位",u"最低点位",u"今收盘点位",
			u"成交量",u"成交金额(亿元)",u"涨跌幅",u"交易日期",u"交易时间"]	

		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,1)
	
	##指数实时分笔
	def OnIndexReal( self, event ):
		a = time.localtime()
		now_hm = time.strftime("%H%M",a)
		start_hm_a = '0830'
		end_hm_a = '1130'
		start_hm_p = '1300'
		end_hm_p = '1500'
		tradetime = timecheck.getweekday(todaydate,'0830')
		if timecheck.compare_hourmin(now_hm,start_hm_a,end_hm_a) or timecheck.compare_hourmin(now_hm,start_hm_p,end_hm_p):
			his.realtimetick(['sh','sz','hs300','sz50','zxb','cyb'])
		cursor.execute("""SELECT * from mkt_tickrealtime WHERE `date` = %s
			order by realtimetick_id desc limit 6
		""",(tradetime))
		
		datacode = cursor.fetchall()
		count = cursor.rowcount
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(2,34):
				data1[k].append(datalist[j])
			k=k+1
		colLabels1 =[u"股票名字",u"今日开盘价",u"昨日收盘价",u"当前价格",u"今日最高价",u"今日最低价",u"竞买价",
			u"竞卖价",u"成交量",u"成交金额",u"委买一(笔数)",u"委买一(价格)",u"委买二(笔数)",u"委买二(价格)",u"委买三(笔数)",u"委买三(价格)",u"委买四(笔数)",u"委买四(价格)",
			u"委买五(笔数)",u"委买五(价格)",u"委卖一(笔数)",u"委卖一(价格)",u"委卖二(笔数)",u"委卖二(价格)",u"委卖三(笔数)",u"委卖三(价格)",u"委卖四(笔数)",u"委卖四(价格)",
			u"委卖五(笔数)",u"委卖五(价格)",u"日期",u"时间",u"股票代码"]	

		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,1)
	


	##全部指数日行情
	def OnMktIdxd( self, event ):
		tradetime = timecheck.getweekday(todaydate,'1600')
		cursor.execute("""SELECT distinct(tradeDate) FROM mkt_mktidxd group by tradeDate order by tradeDate desc
					""")
		tradetimesql = cursor.fetchone()
		if tradetime != tradetimesql[0]:
			inputtradetime = timecheck.chgtimefor(tradetime)
			mkt.mktidxd(inputtradetime)
			'''app = wx.App()
			frame = dialogover.MyDialogover(parent=None)
			frame.Show()
			app.MainLoop()'''
			
		cursor.execute("""SELECT ticker,secShortName,porgFullName,preCloseIndex,openIndex,lowestIndex,
						highestIndex,closeIndex,turnoverVol,turnoverValue,CHG,CHGPct,tradeDate
					from mkt_mktidxd where tradeDate = %s
					order by ticker asc
					limit 847
			""",(tradetime))

		datacode = cursor.fetchall()
		count = cursor.rowcount
		#print count
		#global data1
		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,13):
				data1[k].append(datalist[j])
			k=k+1
		#global colLabels1
		colLabels1 =[u"指数代码",u"证券简称",u"发布机构全称",u"昨收盘指数",u"今开盘指数",u"最低价指数",u"最高价指数",u"今收盘指数",
			u"成交量",u"成交金额",u"涨跌",u"涨跌幅",u"交易日期"]	

		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,1)
	
	global tradetime_equ
	tradetime_equ = timecheck.getweekday(todaydate,'1530')
	##行业板块
	def OnTypeIndustry( self, event ):
		
		cursor.execute("""SELECT distinct(tradetime) FROM cal_industryinfo group by tradetime order by tradetime desc
			""")
		tradetimesql = cursor.fetchone()
		
		if tradetimesql[0] == tradetime_equ:
			cursor.execute("""SELECT typeinfo,avg_ch_pt,avg_weight_ch_pt,turnoverVol_all,max_chpt_name,count_chpt_per,avg_market_per,avg_turnoverRate,avg_pe FROM cal_industryinfo WHERE tradetime=%s
			""",(tradetime_equ))
			datacode = cursor.fetchall()
			count = cursor.rowcount
			industry_info = [[] for i in range(count)]
			k=0
			for datalist in datacode:
				for j in range(0,9):
					industry_info[k].append(datalist[j])
				k=k+1
		else:
			#industry_info = typeindustry.industryinfo()
			industry_info = typeinfo.typeinfo(49,'cal_industryinfo','sec_typeindustry','industry')
		'''
		industry_info = [[] for i in range(10)]
		for i in range(0,10):
			industry_info[i].extend(typeindustry.getindustryi(industry[i])) 
		'''
		colLabels1 =[u"行业名称",u"均涨幅%",u"均权涨幅%",u"总成交量",
		u"领涨股",u"涨股比",u"均市场比%",u"均换手率%",u"均市盈率"]	

		colnum = 9
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,industry_info,colLabels1,1)
		self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,lambda evt,type_name='industry':self.OnShowType(evt,type_name))


		
	##地域板块
	def OnTyeArea( self, event ):
		#tradetime = timecheck.getweekday(todaydate,'1530')
		cursor.execute("""SELECT distinct(tradetime) FROM cal_areainfo group by tradetime order by tradetime desc
			""")
		tradetimesql = cursor.fetchone()
		if tradetimesql[0] == tradetime_equ:
			cursor.execute("""SELECT typeinfo,avg_ch_pt,avg_weight_ch_pt,turnoverVol_all,max_chpt_name,count_chpt_per,avg_market_per,avg_turnoverRate,avg_pe FROM cal_areainfo WHERE tradetime=%s
			""",(tradetime_equ))
			datacode = cursor.fetchall()
			count = cursor.rowcount
			area_info = [[] for i in range(count)]
			k=0
			for datalist in datacode:
				for j in range(0,9):
					area_info[k].append(datalist[j])
				k=k+1
		else:
	
			area_info = typeinfo.typeinfo(32,'cal_areainfo','sec_typearea','area')
		
		colLabels1 =[u"行业名称",u"均涨幅%",u"均权涨幅%",u"总成交量",
		u"领涨股",u"涨股比",u"均市场比%",u"均换手率%",u"均市盈率"]	

		colnum = 9
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,area_info,colLabels1,1)
		self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,lambda evt,type_name='area':self.OnShowType(evt,type_name))

	
	##概念板块
	def OnTypeConcept( self, event ):
		#tradetime = timecheck.getweekday(todaydate,'1530')
		cursor.execute("""SELECT distinct(tradetime) FROM cal_conceptinfo group by tradetime order by tradetime desc
			""")
		tradetimesql = cursor.fetchone()
		if tradetimesql[0] == tradetime_equ:
			cursor.execute("""SELECT typeinfo,avg_ch_pt,avg_weight_ch_pt,turnoverVol_all,max_chpt_name,count_chpt_per,avg_market_per,avg_turnoverRate,avg_pe FROM cal_conceptinfo WHERE tradetime=%s
			""",(tradetime_equ))
			datacode = cursor.fetchall()
			count = cursor.rowcount
			concept_info = [[] for i in range(count)]
			k=0
			for datalist in datacode:
				for j in range(0,9):
					concept_info[k].append(datalist[j])
				k=k+1
		else:
	
			concept_info = typeinfo.typeinfo(156,'cal_conceptinfo','sec_typeconcept','concept')
		
		colLabels1 =[u"行业名称",u"均涨幅%",u"均权涨幅%",u"总成交量",
		u"领涨股",u"涨股比",u"均市场比%",u"均换手率%",u"均市盈率"]	

		colnum = 9
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,concept_info,colLabels1,1)
		self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,lambda evt,type_name='concept':self.OnShowType(evt,type_name))


	#显示板块内股票信息		
	def OnShowType(self,event,type_name):
		print "OnShowType:" + str(event.GetRow())
		rowindex = event.GetRow()
		if type_name == 'industry':
			industry_name = typedata.industry[rowindex]
			cursor.execute("""SELECT ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				from mkt_mktequd,sec_typeindustry
				where c_name = %s AND code = concat(ticker,'') AND tradeDate = %s
				order by ticker asc
			""",(industry_name,tradetime_equ))
			datacode = cursor.fetchall()
			count = cursor.rowcount
				
		elif type_name == 'area':
			area_name = typedata.area[rowindex]
			cursor.execute("""SELECT ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				from mkt_mktequd,sec_typeindustry
				where area = %s AND code = concat(ticker,'') AND tradeDate = %s
				order by ticker asc
			""",(area_name,tradetime_equ))
			datacode = cursor.fetchall()
			count = cursor.rowcount
		elif type_name == 'concept':
			concept_name = typedata.concept[rowindex]
			cursor.execute("""SELECT ticker,secShortName,openPrice,highestPrice,lowestPrice,preClosePrice,closePrice,turnoverVol,turnoverValue,dealAmount,
							turnoverRate,negMarketValue,marketValue,PE,PE1,PB,tradeDate
				from mkt_mktequd,sec_typeindustry
				where c_name = %s AND code = concat(ticker,'') AND tradeDate = %s
				order by ticker asc
			""",(concept_name,tradetime_equ))
			datacode = cursor.fetchall()
			count = cursor.rowcount

		data1 = [[] for i in range(count)]
		k=0
		for datalist in datacode:
			for j in range(0,17):
				data1[k].append(datalist[j])
			k=k+1
			
		colLabels1 =[u"股票代码",u"股票名称",u"今日开盘价",u"最高价",u"最低价",u"昨日收盘价",u"今日收盘价",u"成交量",u"成交金额",u"成交笔数",
		u"日换手率",u"流通市值",u"总市值",u"滚动市盈率",u"市盈率",u"市净率",u"交易日期",u"所属行业",u"概念板块"]
		colnum = len(data1[0])
		dataSortBigger1 = [[]for i in range(colnum)]
		dataSortSmaller1 = [[]for i in range(colnum)]
		self.allsort(colnum,dataSortBigger1,dataSortSmaller1,data1,colLabels1,0)
	
	def OnShowDayline(self,event):
		rowindex = event.GetRow()
		colindex = event.GetCol()
		value = self.table.GetValue(rowindex,0)
		print value
		subframe = draw_Dayline.DrawFrame([],[],value)
		subframe.Show()


	
	def OnChild1(self,event):
		app = wx.App()
		#frame1.Close()
		dlg = tools_Dialog1.SubclassDialog1()
		#frame.Show()
		#app.MainLoop()
		#dlg = tools_Dialog1.SubclassDialog1()
		if dlg.ShowModal() == wx.ID_CANCEL:
			print "cancel1"
		else:
			print "OK1"
		dlg.Destroy()

	def OnChild2(self,event):
		app = wx.App()
		dlg = tools_Dialog2.SubclassDialog2()
		if dlg.ShowModal() == wx.ID_CANCEL:
			print "cancel2"
		else:
			print "OK2"
		dlg.Destroy()
	global now_value
	now_value = '000001'
	def OnChild3_1(self,event):
		global now_value
		rowindex = event.GetRow()
		colindex = event.GetCol()
		now_value = self.table.GetValue(rowindex,0)
		print now_value
		
	def OnChild3(self,event):
		value = now_value
		Subframe = f10_display.TestFrame1(value)
		Subframe.Show()

		#日志相关
		import loggerfun
		loggerfun.fun3()

	def OnChild4_1(self,event):
		f10_with_processbar_final.update_f10()


	
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
		#loggerfun.fun0_f()


if __name__ == '__main__':
	#app = wx.App()
	#frame = MyFramemain(parent=None)
	#frame.Show()
	app = MyApp(0)
	#日志相关father层次
	import loggerfun
	loggerfun.fun0_s()
	app.MainLoop()	
	loggerfun.fun0_f()

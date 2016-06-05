# -*- coding: utf-8 -*- 

import wx
#import dbdata
from connect_db import cursor
#dbdict = {'全部数据':'db_mkt','沪深股票数据':'equ','股票基本信息':'equ_equ','股票历次配股信息':'equ_equallot'}
from dbdata import dbdict

class FrameDBinfo(wx.Frame):
	def __init__(self,parent):
		wx.Frame.__init__(self, parent, title=u"数据库信息", size=(500,500))
		self.panel = wx.Panel(self, -1)
		self.multiLabel = wx.StaticText(self.panel, -1, u"数据库状态",pos=(300,10))
		self.multiText = wx.TextCtrl(self.panel, -1,
		pos=(300,30), size = (180,200), style=wx.TE_MULTILINE) #创建一个文本控件
		self.multiText.SetInsertionPoint(0) #设置插入点
		self.multiText.AppendText(u'数据表个数：')
		cursor.execute("""SELECT count(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'db_mkt' 
			""")
		countdb = cursor.fetchone()
		self.multiText.AppendText('' + str(countdb[0]))
		cursor.execute("""SELECT TABLE_NAME,UPDATE_TIME
							FROM information_schema.TABLES
							WHERE TABLE_SCHEMA = 'db_mkt'
							ORDER BY UPDATE_TIME desc
							limit 1
		""")
		latesttb = cursor.fetchone()
		self.multiText.AppendText(u'\n最近更新数据库：'+ str(latesttb[0]) + u'\n更新时间：'+ str(latesttb[1]))
			
		#multiText.AppendText('123')
		#NewButton = wx.Button(self,-1,u'新建',pos=(300,15))

		self.tree = wx.TreeCtrl(self.panel,size=(275,475))
		#增加一个根节点
		root = self.tree.AddRoot(u"全部数据")
		
		childequ = self.tree.AppendItem(root,u"沪深股票数据")
		self.tree.AppendItem(childequ,u"股票基本信息")
		self.tree.AppendItem(childequ,u"股票历次配股信息")
		self.tree.AppendItem(childequ,u"股票分红信息")
		self.tree.AppendItem(childequ,u"股票首次上市信息")
		self.tree.AppendItem(childequ,u"股票每日回报率")
		self.tree.AppendItem(childequ,u"沪深融资融券每日汇总信息")
		self.tree.AppendItem(childequ,u"股票列表")
		childfdmt = self.tree.AppendItem(root,u"基本面数据")
		self.tree.AppendItem(childfdmt,u"现金流量")
		self.tree.AppendItem(childfdmt,u"偿债能力")
		self.tree.AppendItem(childfdmt,u"业绩报告")
		self.tree.AppendItem(childfdmt,u"业绩预告")
		self.tree.AppendItem(childfdmt,u"成长能力")
		self.tree.AppendItem(childfdmt,u"营运能力")
		self.tree.AppendItem(childfdmt,u"盈利能力")
		childfund = self.tree.AppendItem(root,u"基金信息")
		self.tree.AppendItem(childfund,u"基金基本信息")
		self.tree.AppendItem(childfund,u"基金资产配置")
		self.tree.AppendItem(childfund,u"基金历史收益")
		self.tree.AppendItem(childfund,u"基金持仓明细")
		self.tree.AppendItem(childfund,u"基金历史净值")
		childmkt = self.tree.AppendItem(root,u"市场行情数据")
		self.tree.AppendItem(childmkt,u"历史行情数据")
		self.tree.AppendItem(childmkt,u"历史复权数据")
		self.tree.AppendItem(childmkt,u"大盘指数历史数据")
		self.tree.AppendItem(childmkt,u"实时行情")
		self.tree.AppendItem(childmkt,u"沪深大宗交易")
		self.tree.AppendItem(childmkt,u"债券日行情")
		self.tree.AppendItem(childmkt,u"沪深股票日行情")
		self.tree.AppendItem(childmkt,u"基金日行情")
		self.tree.AppendItem(childmkt,u"期货日行情")
		self.tree.AppendItem(childmkt,u"指数日行情")
		self.tree.AppendItem(childmkt,u"大盘指数实时行情")
		self.tree.AppendItem(childmkt,u"期权日行情")
		self.tree.AppendItem(childmkt,u"债券回购交易日行情")
		self.tree.AppendItem(childmkt,u"历史分笔")
		self.tree.AppendItem(childmkt,u"实时分笔")
		childsec = self.tree.AppendItem(root,u"证券概况")
		self.tree.AppendItem(childsec,u"证券编码及基本上市信息")
		self.tree.AppendItem(childsec,u"交易所交易日历")
		self.tree.AppendItem(childsec,u"证券板块")
		self.tree.AppendItem(childsec,u"地域分类(省)")
		self.tree.AppendItem(childsec,u"概念分类")
		self.tree.AppendItem(childsec,u"行业分类")
		self.tree.AppendItem(childsec,u"地域分类(市)")
		self.tree.AppendItem(childsec,u"证券板块成分")
		childhkequ = self.tree.AppendItem(root,u"港股信息")
		childidx = self.tree.AppendItem(root,u"指数信息")
		childopt = self.tree.AppendItem(root,u"期权信息")
		
		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
		
		#增加各种节点（通过文件）
		#self.AddTreeNodes(root,dbdata.tree)
		#self.Bind(wx.EVT_TREE_SEL_CHANGED,self.OnTreeSelChanged)
	'''
	def AddTreeNodes(self, parentItem, items):
		for item in items:
			if type(item) == str:
				self.tree.AppendItem(parentItem, item)
			else:
				newItem = self.tree.AppendItem(parentItem, item[0])
				self.AddTreeNodes(newItem,item[1])
	'''
	def GetItemText(self, item):
		if item:
			return self.tree.GetItemText(item)
		else:
			return ''
	def OnSelChanged(self, evt):
		item = self.GetItemText(evt.GetItem())
		#print type(item)
		tbname = dbdict[item.encode('utf8')]
		print type(tbname)
		if tbname == "db_mkt":
			pass
		elif tbname == "equ":
			self.multiText.Clear()
			self.multiText.AppendText(item +u'\n包含7个表')
		elif tbname == "fdmt":
			self.multiText.Clear()
			self.multiText.AppendText(item +u'\n包含7个表')
		elif tbname == "fund":
			self.multiText.Clear()
			self.multiText.AppendText(item +u'\n包含5个表')
		elif tbname == "mkt":
			self.multiText.Clear()
			self.multiText.AppendText(item +u'\n包含15个表')
		elif tbname == "sec":
			self.multiText.Clear()
			self.multiText.AppendText(item +u'\n包含8个表')
				
		else:
			self.multiText.Clear()
			
			cursor.execute("""SELECT TABLE_ROWS,UPDATE_TIME,DATA_LENGTH+INDEX_LENGTH
							FROM information_schema.TABLES
							WHERE TABLE_SCHEMA = 'db_mkt'
							AND information_schema.TABLES.TABLE_NAME = %s
			""",(tbname))
			#行数，最近更新时间，表大小
			tbinfo = cursor.fetchone()
			self.multiText.AppendText(item + u'表' + tbname +u'\n\n表记录数：' + str(tbinfo[0]) +'\n')
			self.multiText.AppendText(u'表最近更新时间：\n' + str(tbinfo[1]) +'\n')
			self.multiText.AppendText(u'表大小：' + str(tbinfo[2]/1024) +'K\n')


			#self.multiText.Refresh()

		print dbdict[item.encode('utf8')]
		print "OnSelChanged: ", self.GetItemText(evt.GetItem())
	
if __name__ == '__main__':
	app = wx.App()
	frame = FrameDBinfo(parent = None)
	frame.Show()
	app.MainLoop()	
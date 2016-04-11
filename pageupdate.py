# -*- coding: utf-8 -*- 

###########################################################################
## 更新控制界面
###########################################################################

import wx
import upmkt
import upsec
import upfdmt
import upequ
import upfund
import uphkidxopt
import mkt

import dialogmktequd
import dialogfundnav
import dialogsecid
import dialogover

import time
todaydate = time.strftime('%Y%m%d')
###########################################################################
## Class MyFrameupdata
###########################################################################

class MyFrameupdata ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"数据更新控制", pos = wx.DefaultPosition, size = wx.Size( 600,550 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menusec = wx.Menu()
		self.m_menusec.AppendSeparator()
		
		self.m_menuItemsec = wx.MenuItem( self.m_menusec, wx.ID_ANY, u"证券编码及基本上市信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menusec.AppendItem( self.m_menuItemsec )
		
		self.m_menuItemtradecal = wx.MenuItem( self.m_menusec, wx.ID_ANY, u"交易所交易日历", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menusec.AppendItem( self.m_menuItemtradecal )
		
		self.m_menuItemtyperel = wx.MenuItem( self.m_menusec, wx.ID_ANY, u"证券板块成分", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menusec.AppendItem( self.m_menuItemtyperel )
		
		self.m_menuItemtype = wx.MenuItem( self.m_menusec, wx.ID_ANY, u"证券板块分类列表", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menusec.AppendItem( self.m_menuItemtype )
		
		self.m_menuItemtyperegion = wx.MenuItem( self.m_menusec, wx.ID_ANY, u"地域分类", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menusec.AppendItem( self.m_menuItemtyperegion )
		
		self.m_menusec.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menusec, u"证券概况" ) 
		
		self.m_menumkt = wx.Menu()
		self.m_menumkt.AppendSeparator()
		
		self.m_menuItemmktequd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"沪深股票日线行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktequd )
		
		self.m_menuItemmktfutd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"期货日线行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktfutd )
		
		self.m_menuItemmktidxd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"指数日线行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktidxd )
		
		self.m_menuItemmktblockd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"沪深大宗交易", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktblockd )
		
		self.m_menuItemmktrepod = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"债券回购交易日行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktrepod )
		
		self.m_menuItemmktbondd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"债券日行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktbondd )
		
		self.m_menuItemmkthkequd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"港股日行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmkthkequd )
		
		self.m_menuItemmkfundd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"基金日行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmkfundd )
		
		self.m_menuItemmktoptd = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"期权日行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktoptd )
		
		self.m_menuItemmktall = wx.MenuItem( self.m_menumkt, wx.ID_ANY, u"实时行情", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menumkt.AppendItem( self.m_menuItemmktall )
		
		self.m_menumkt.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menumkt, u"市场行情数据" ) 
		
		self.m_menufdmt = wx.Menu()
		self.m_menufdmt.AppendSeparator()
		
		self.m_menuItemfdmtee = wx.MenuItem( self.m_menufdmt, wx.ID_ANY, u"业绩快报", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menufdmt.AppendItem( self.m_menuItemfdmtee )
		
		self.m_menuItemfdmtef = wx.MenuItem( self.m_menufdmt, wx.ID_ANY, u"业绩预告", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menufdmt.AppendItem( self.m_menuItemfdmtef )
		
		self.m_menufdmt.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menufdmt, u"基本面数据" ) 
		
		self.m_menuequ = wx.Menu()
		self.m_menuequ.AppendSeparator()
		
		self.m_menuItemequ = wx.MenuItem( self.m_menuequ, wx.ID_ANY, u"股票基本信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuequ.AppendItem( self.m_menuItemequ )
		
		self.m_menuItemequallot = wx.MenuItem( self.m_menuequ, wx.ID_ANY, u"股票配股信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuequ.AppendItem( self.m_menuItemequallot )
		
		self.m_menuItemequdiv = wx.MenuItem( self.m_menuequ, wx.ID_ANY, u"股票分红信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuequ.AppendItem( self.m_menuItemequdiv )
		
		self.m_menuItemequipo = wx.MenuItem( self.m_menuequ, wx.ID_ANY, u"股票首次上市信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuequ.AppendItem( self.m_menuItemequipo )
		
		self.m_menuItemequretud = wx.MenuItem( self.m_menuequ, wx.ID_ANY, u"股票每日回报率", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuequ.AppendItem( self.m_menuItemequretud )
		
		self.m_menuItemequfsttotal = wx.MenuItem( self.m_menuequ, wx.ID_ANY, u"沪深融资融券每日汇总信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuequ.AppendItem( self.m_menuItemequfsttotal )
		
		self.m_menuequ.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuequ, u"沪深股票信息" ) 
		
		self.m_menufund = wx.Menu()
		self.m_menufund.AppendSeparator()
		
		self.m_menuItemfund = wx.MenuItem( self.m_menufund, wx.ID_ANY, u"基金基本信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menufund.AppendItem( self.m_menuItemfund )
		
		self.m_menuItemfundnav = wx.MenuItem( self.m_menufund, wx.ID_ANY, u"基金历史净值", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menufund.AppendItem( self.m_menuItemfundnav )
		
		self.m_menuItemfunddivm = wx.MenuItem( self.m_menufund, wx.ID_ANY, u"基金历史收益", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menufund.AppendItem( self.m_menuItemfunddivm )
		
		self.m_menuItemfundassets = wx.MenuItem( self.m_menufund, wx.ID_ANY, u"基金资产配置", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menufund.AppendItem( self.m_menuItemfundassets )
		
		self.m_menuItemfundholdings = wx.MenuItem( self.m_menufund, wx.ID_ANY, u"基金持仓明细", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menufund.AppendItem( self.m_menuItemfundholdings )
		
		self.m_menufund.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menufund, u"基金信息" ) 
		
		self.m_menuidx = wx.Menu()
		self.m_menuidx.AppendSeparator()
		
		self.m_menuItemidx = wx.MenuItem( self.m_menuidx, wx.ID_ANY, u"指数基本信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuidx.AppendItem( self.m_menuItemidx )
		
		self.m_menuidx.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuidx, u"指数信息" ) 
		
		self.m_menuhkequ = wx.Menu()
		self.m_menuhkequ.AppendSeparator()
		
		self.m_menuItemhkequ = wx.MenuItem( self.m_menuhkequ, wx.ID_ANY, u"港股基本信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuhkequ.AppendItem( self.m_menuItemhkequ )
		
		self.m_menuhkequ.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuhkequ, u"港股信息" ) 
		
		self.m_menuopt = wx.Menu()
		self.m_menuopt.AppendSeparator()
		
		self.m_menuItemopt = wx.MenuItem( self.m_menuopt, wx.ID_ANY, u"期权基本信息", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuopt.AppendItem( self.m_menuItemopt )
		
		self.m_menuopt.AppendSeparator()
		
		self.m_menubar1.Append( self.m_menuopt, u"期权信息" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline9 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )
		
		gSizer1 = wx.GridSizer( 2, 2, 0, 0 )
		
		fgSizer3 = wx.FlexGridSizer( 12, 1, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText16 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"一键更新", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		fgSizer3.Add( self.m_staticText16, 0, wx.ALL, 5 )
		
		self.m_staticline26 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer3.Add( self.m_staticline26, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_button8 = wx.Button( self.m_panel2, wx.ID_ANY, u"更新证券概况", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button8, 0, wx.ALL, 5 )
		
		self.m_button9 = wx.Button( self.m_panel2, wx.ID_ANY, u"更新市场行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button9, 0, wx.ALL, 5 )
		
		self.m_button10 = wx.Button( self.m_panel2, wx.ID_ANY, u"更新基本面数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button10, 0, wx.ALL, 5 )
		
		self.m_button11 = wx.Button( self.m_panel2, wx.ID_ANY, u"更新沪深股票", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button11, 0, wx.ALL, 5 )
		
		self.m_button12 = wx.Button( self.m_panel2, wx.ID_ANY, u"更新基金信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button12, 0, wx.ALL, 5 )
		
		self.m_button13 = wx.Button( self.m_panel2, wx.ID_ANY, u"更新指数港股期权", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_button13, 0, wx.ALL, 5 )
		
		self.m_staticline24 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer3.Add( self.m_staticline24, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText20 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"实时数据更新：更新交易日实时数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		fgSizer3.Add( self.m_staticText20, 0, wx.ALL, 5 )
		
		self.m_buttonmktall = wx.Button( self.m_panel2, wx.ID_ANY, u"更新实时行情数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonmktall, 0, wx.ALL, 5 )
		
		self.m_buttontickreal = wx.Button( self.m_panel2, wx.ID_ANY, u"更新实时分笔数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttontickreal, 0, wx.ALL, 5 )
		
		gSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		fgSizer12 = wx.FlexGridSizer( 12, 1, 0, 0 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText13 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"日线数据更新：更新当天或上一交易日数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		fgSizer12.Add( self.m_staticText13, 0, wx.ALL, 5 )
		
		self.m_staticline25 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		fgSizer12.Add( self.m_staticline25, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_buttonmktequd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新沪深股票日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktequd, 0, wx.ALL, 5 )
		
		self.m_buttonmktfutd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新期货日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktfutd, 0, wx.ALL, 5 )
		
		self.m_buttonmktidxd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新指数日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktidxd, 0, wx.ALL, 5 )
		
		self.m_buttonmktblockd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新沪深大宗交易日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktblockd, 0, wx.ALL, 5 )
		
		self.m_buttonmktrepod = wx.Button( self.m_panel2, wx.ID_ANY, u"更新债券回购交易日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktrepod, 0, wx.ALL, 5 )
		
		self.m_buttonmktbondd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新债券日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktbondd, 0, wx.ALL, 5 )
		
		self.m_buttonmkthkequd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新港股日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmkthkequd, 0, wx.ALL, 5 )
		
		self.m_buttonmktfundd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新基金日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktfundd, 0, wx.ALL, 5 )
		
		self.m_buttonmktoptd = wx.Button( self.m_panel2, wx.ID_ANY, u"更新期权日行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_buttonmktoptd, 0, wx.ALL, 5 )
		
		gSizer1.Add( fgSizer12, 1, wx.EXPAND, 5 )
		
		bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.m_staticline11 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button6 = wx.Button( self.m_panel2, wx.ID_ANY, u"一键更新所有数据库", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_button6, 0, wx.ALIGN_RIGHT|wx.ALL|wx.BOTTOM, 5 )
		
		bSizer1.Add( bSizer17, 0, wx.ALIGN_RIGHT, 5 )
		
		self.m_staticline18 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline18, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel2.SetSizer( bSizer1 )
		self.m_panel2.Layout()
		bSizer1.Fit( self.m_panel2 )
		bSizer6.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.Onsec, id = self.m_menuItemsec.GetId() )
		self.Bind( wx.EVT_MENU, self.Ontradecal, id = self.m_menuItemtradecal.GetId() )
		self.Bind( wx.EVT_MENU, self.Ontyperel, id = self.m_menuItemtyperel.GetId() )
		self.Bind( wx.EVT_MENU, self.Ontype, id = self.m_menuItemtype.GetId() )
		self.Bind( wx.EVT_MENU, self.Ontyperegion, id = self.m_menuItemtyperegion.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktequd, id = self.m_menuItemmktequd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktfutd, id = self.m_menuItemmktfutd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktidxd, id = self.m_menuItemmktidxd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktblockd, id = self.m_menuItemmktblockd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktrepod, id = self.m_menuItemmktrepod.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktbondd, id = self.m_menuItemmktbondd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmkthkequd, id = self.m_menuItemmkthkequd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmkfundd, id = self.m_menuItemmkfundd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktoptd, id = self.m_menuItemmktoptd.GetId() )
		self.Bind( wx.EVT_MENU, self.Onmktall, id = self.m_menuItemmktall.GetId() )
		self.Bind( wx.EVT_MENU, self.Onfdmtee, id = self.m_menuItemfdmtee.GetId() )
		self.Bind( wx.EVT_MENU, self.Onfdmtef, id = self.m_menuItemfdmtef.GetId() )
		self.Bind( wx.EVT_MENU, self.Onequ, id = self.m_menuItemequ.GetId() )
		self.Bind( wx.EVT_MENU, self.Onequallot, id = self.m_menuItemequallot.GetId() )
		self.Bind( wx.EVT_MENU, self.Onequdiv, id = self.m_menuItemequdiv.GetId() )
		self.Bind( wx.EVT_MENU, self.Onequipo, id = self.m_menuItemequipo.GetId() )
		self.Bind( wx.EVT_MENU, self.Onequretud, id = self.m_menuItemequretud.GetId() )
		self.Bind( wx.EVT_MENU, self.Onequfsttotal, id = self.m_menuItemequfsttotal.GetId() )
		self.Bind( wx.EVT_MENU, self.Onfund, id = self.m_menuItemfund.GetId() )
		self.Bind( wx.EVT_MENU, self.Onfundnav, id = self.m_menuItemfundnav.GetId() )
		self.Bind( wx.EVT_MENU, self.Onfunddivm, id = self.m_menuItemfunddivm.GetId() )
		self.Bind( wx.EVT_MENU, self.Onfundassets, id = self.m_menuItemfundassets.GetId() )
		self.Bind( wx.EVT_MENU, self.Onfundholdings, id = self.m_menuItemfundholdings.GetId() )
		self.Bind( wx.EVT_MENU, self.Onidx, id = self.m_menuItemidx.GetId() )
		self.Bind( wx.EVT_MENU, self.Onhkequ, id = self.m_menuItemhkequ.GetId() )
		self.Bind( wx.EVT_MENU, self.Onopt, id = self.m_menuItemopt.GetId() )
		self.m_button8.Bind( wx.EVT_BUTTON, self.OnUpsec )
		self.m_button9.Bind( wx.EVT_BUTTON, self.OnUpmkt )
		self.m_button10.Bind( wx.EVT_BUTTON, self.OnUpfdmt )
		self.m_button11.Bind( wx.EVT_BUTTON, self.OnUpequ )
		self.m_button12.Bind( wx.EVT_BUTTON, self.OnUpfund )
		self.m_button13.Bind( wx.EVT_BUTTON, self.OnUpidx )
		self.m_buttonmktall.Bind( wx.EVT_BUTTON, self.Onmktall )
		self.m_buttontickreal.Bind( wx.EVT_BUTTON, self.Ontickreal )
		self.m_buttonmktequd.Bind( wx.EVT_BUTTON, self.Onequdtoday )
		self.m_buttonmktfutd.Bind( wx.EVT_BUTTON, self.Onfutdtoday )
		self.m_buttonmktidxd.Bind( wx.EVT_BUTTON, self.Onidxdtoday )
		self.m_buttonmktblockd.Bind( wx.EVT_BUTTON, self.Onblockdtoday )
		self.m_buttonmktrepod.Bind( wx.EVT_BUTTON, self.Onrepodtoday )
		self.m_buttonmktbondd.Bind( wx.EVT_BUTTON, self.Onbonddtoday )
		self.m_buttonmkthkequd.Bind( wx.EVT_BUTTON, self.Onhkequdtoday )
		self.m_buttonmktfundd.Bind( wx.EVT_BUTTON, self.Onfunddtoday )
		self.m_buttonmktoptd.Bind( wx.EVT_BUTTON, self.Onoptdtoday )
		self.m_button6.Bind( wx.EVT_BUTTON, self.Upalldb )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Onsec( self, event ):
		app = wx.App()
		frame = dialogsecid.MyDialogsecid(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	
	def Ontradecal( self, event ):
		event.Skip()
	
	def Ontyperel( self, event ):
		event.Skip()
	
	def Ontype( self, event ):
		event.Skip()
	
	def Ontyperegion( self, event ):
		event.Skip()
	
	def Onmktequd( self, event ):
		app = wx.App()
		frame = dialogmktequd.MyDialogmktequd(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	
	def Onmktfutd( self, event ):
		event.Skip()
	
	def Onmktidxd( self, event ):
		event.Skip()
	
	def Onmktblockd( self, event ):
		event.Skip()
	
	def Onmktrepod( self, event ):
		event.Skip()
	
	def Onmktbondd( self, event ):
		event.Skip()
	
	def Onmkthkequd( self, event ):
		event.Skip()
	
	def Onmkfundd( self, event ):
		event.Skip()
	
	def Onmktoptd( self, event ):
		event.Skip()
	
	def Onmktall( self, event ):
		event.Skip()
	
	def Onfdmtee( self, event ):
		event.Skip()
	
	def Onfdmtef( self, event ):
		event.Skip()
	
	def Onequ( self, event ):
		event.Skip()
	
	def Onequallot( self, event ):
		event.Skip()
	
	def Onequdiv( self, event ):
		event.Skip()
	
	def Onequipo( self, event ):
		event.Skip()
	
	def Onequretud( self, event ):
		event.Skip()
	
	def Onequfsttotal( self, event ):
		event.Skip()
	
	def Onfund( self, event ):
		event.Skip()
	
	def Onfundnav( self, event ):
		app = wx.App()
		frame = dialogfundnav.MyDialogfundnav(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	
	def Onfunddivm( self, event ):
		event.Skip()
	
	def Onfundassets( self, event ):
		event.Skip()
	
	def Onfundholdings( self, event ):
		event.Skip()
	
	def Onidx( self, event ):
		event.Skip()
	
	def Onhkequ( self, event ):
		event.Skip()
	
	def Onopt( self, event ):
		event.Skip()
####################################################	
	def OnUpsec( self, event ):
		upsec.upsecall()
		event.Skip()
	
	def OnUpmkt( self, event ):
		upmkt.upmktall()
		event.Skip()
	
	def OnUpfdmt( self, event ):
		upfdmt.upfdmtall()
		event.Skip()
	
	def OnUpequ( self, event ):
		upequ.upequall()
		event.Skip()
	
	def OnUpfund( self, event ):
		upfund.upfundall()
		event.Skip()
	
	def OnUpidx( self, event ):
		uphkidxopt.uphkidxoptall()
		event.Skip()
	

	def Ontickreal( self, event ):
		event.Skip()
	
	def Onequdtoday( self, event ):
		mkt.mktequd(todaydate)
		app = wx.App()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	
	def Onfutdtoday( self, event ):
		event.Skip()
	
	def Onidxdtoday( self, event ):
		event.Skip()
	
	def Onblockdtoday( self, event ):
		event.Skip()
	
	def Onrepodtoday( self, event ):
		event.Skip()
	
	def Onbonddtoday( self, event ):
		event.Skip()
	
	def Onhkequdtoday( self, event ):
		event.Skip()
	
	def Onfunddtoday( self, event ):
		event.Skip()
	
	def Onoptdtoday( self, event ):
		event.Skip()
	
	def Upalldb( self, event ):
		event.Skip()
	




if __name__ == '__main__':
	app = wx.App()
	frame = MyFrameupdata(parent=None)
	frame.Show()
	app.MainLoop()	

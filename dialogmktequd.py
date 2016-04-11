# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import mkt
import time
import datetime
import dialogover
###########################################################################
## Class MyDialogmktequd
###########################################################################

class MyDialogmktequd ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"沪深股票日线行情", pos = wx.DefaultPosition, size = wx.Size( 281,183 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer18 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer18.SetFlexibleDirection( wx.BOTH )
		fgSizer18.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText45 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"沪深股票日线行情", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText45.Wrap( -1 )
		fgSizer18.Add( self.m_staticText45, 0, wx.ALL, 5 )
		
		
		fgSizer18.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_button12 = wx.Button( self.m_panel6, wx.ID_ANY, u"更新当天数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer18.Add( self.m_button12, 0, wx.ALL, 5 )
		
		self.m_button13 = wx.Button( self.m_panel6, wx.ID_ANY, u"更新前一天数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer18.Add( self.m_button13, 0, wx.ALL, 5 )
		
		bSizer27.Add( fgSizer18, 1, wx.EXPAND, 5 )
		
		self.m_staticline30 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer27.Add( self.m_staticline30, 0, wx.EXPAND |wx.ALL, 5 )
		
		fgSizer20 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer20.SetFlexibleDirection( wx.BOTH )
		fgSizer20.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText47 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"请输入需要更新的日期，格式如20150101", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText47.Wrap( -1 )
		fgSizer20.Add( self.m_staticText47, 0, wx.ALL, 5 )
		
		
		fgSizer20.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		fgSizer23 = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizer23.SetFlexibleDirection( wx.BOTH )
		fgSizer23.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_textCtrl74 = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer23.Add( self.m_textCtrl74, 0, wx.ALL, 5 )
		
		self.m_button18 = wx.Button( self.m_panel6, wx.ID_ANY, u"更新该日期数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer23.Add( self.m_button18, 0, wx.ALL, 5 )
		
		fgSizer20.Add( fgSizer23, 1, wx.EXPAND, 5 )
		
		bSizer27.Add( fgSizer20, 1, wx.EXPAND, 5 )
		
		self.m_panel6.SetSizer( bSizer27 )
		self.m_panel6.Layout()
		bSizer27.Fit( self.m_panel6 )
		bSizer26.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer26 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button12.Bind( wx.EVT_BUTTON, self.Onmktequdtoday )
		self.m_button13.Bind( wx.EVT_BUTTON, self.Onmktequdpreday )
		self.m_textCtrl74.Bind( wx.EVT_TEXT_ENTER, self.Inputdate )
		self.m_button18.Bind( wx.EVT_BUTTON, self.Onmktequdoneday )
		self.inputdate=''
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Onmktequdtoday( self, event ):
		todaydate = time.strftime('%Y%m%d')
		mkt.mktequd(todaydate)
		app = wx.App()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	
	def Onmktequdpreday( self, event ):
		now_time = datetime.datetime.now()
		yes_time = now_time + datetime.timedelta(days=-1)
		yes_time_nyr = yes_time.strftime('%Y%m%d')
		mkt.mktequd(yes_time_nyr)

		app = wx.App()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	
	def Inputdate( self, event ):
		event.Skip()
	
	def Onmktequdoneday( self, event ):
		inputdate=self.m_textCtrl74.GetValue()
		#print inputdate
		mkt.mktequd(inputdate)
		#print "over"
		app = wx.App()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	


	
if __name__ == '__main__':
	#app = wx.PySimpleApp()
	app = wx.App()
	frame = MyDialogmktequd(parent=None)
	frame.Show()
	app.MainLoop()	


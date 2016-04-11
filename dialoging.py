# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class MyDialoging
###########################################################################

class MyDialoging ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 129,104 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel4 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText11 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"正在更新...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer10.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.m_gauge1 = wx.Gauge( self.m_panel4, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_gauge1.SetValue( 0 ) 
		bSizer10.Add( self.m_gauge1, 0, wx.ALL, 5 )
		
		self.m_panel4.SetSizer( bSizer10 )
		self.m_panel4.Layout()
		bSizer10.Fit( self.m_panel4 )
		bSizer9.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

if __name__ == '__main__':
	#app = wx.PySimpleApp()
	app = wx.App()
	frame = MyDialoging(parent=None)
	frame.Show()
	app.MainLoop()	

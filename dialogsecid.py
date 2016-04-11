# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import sec
import dialogover

###########################################################################
## Class MyDialogsecid
###########################################################################

class MyDialogsecid ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"证券编码及基本上市信息", pos = wx.DefaultPosition, size = wx.Size( 242,139 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer26 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel6 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer27 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline30 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer27.Add( self.m_staticline30, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer17 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText16 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"证券编码及基本上市信息", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		bSizer17.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_button18 = wx.Button( self.m_panel6, wx.ID_ANY, u"更新数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer17.Add( self.m_button18, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer27.Add( bSizer17, 1, wx.EXPAND, 5 )
		
		self.m_staticline13 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer27.Add( self.m_staticline13, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel6.SetSizer( bSizer27 )
		self.m_panel6.Layout()
		bSizer27.Fit( self.m_panel6 )
		bSizer26.Add( self.m_panel6, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.SetSizer( bSizer26 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button18.Bind( wx.EVT_BUTTON, self.Onupsecid )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Onupsecid( self, event ):
		sec.secid()
		app = wx.App()
		frame = dialogover.MyDialogover(parent=None)
		frame.Show()
		app.MainLoop()
		event.Skip()
	
if __name__ == '__main__':
	#app = wx.PySimpleApp()
	app = wx.App()
	frame = MyDialogsecid(parent=None)
	frame.Show()
	app.MainLoop()	


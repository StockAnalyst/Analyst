#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#FILE:公式管理器

import wx
import data
import formulas_write
import draw_Dayline

#公式管理器界面（包含显示所有公式+增删查改）
class SubclassDialog1(wx.Dialog):#自定义的
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u'公式管理器',size=(400,500))
        
        #所有按钮
        NewButton = wx.Button(self,-1,u'新建',pos=(300,15))
        self.Bind(wx.EVT_BUTTON,self.OnNew,NewButton)
        
        ChangeButton = wx.Button(self,-1,u'修正',pos=(300,45))
        self.Bind(wx.EVT_BUTTON,self.OnRevise,ChangeButton)
        
        DeleteButton = wx.Button(self,-1,u'删除',pos=(300,75))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,DeleteButton)
        
        FindButton = wx.Button(self,-1,u'查找',pos=(300,105))
        self.Bind(wx.EVT_BUTTON,self.OnFind,FindButton)
        
        ViewButton = wx.Button(self,wx.ID_OK,u'预览',pos=(300,135))
        self.Bind(wx.EVT_BUTTON,self.OnView,ViewButton)
        
        InputButton = wx.Button(self,-1,u'导入',pos=(300,195))
        self.Bind(wx.EVT_BUTTON,self.OnInput,InputButton)
        
        OutputButton = wx.Button(self,-1,u'导出',pos=(300,225))
        self.Bind(wx.EVT_BUTTON,self.OnOutput,OutputButton)
        
        CloseButton = wx.Button(self,wx.ID_CANCEL,u'关闭',pos=(300,285))

        #创建一个树
        self.tree = wx.TreeCtrl(self,size=(275,475))
        #增加一个根节点
        root = self.tree.AddRoot("ONE")
        #增加各种节点（通过文件）
        self.AddTreeNodes(root,data.tree)

    def OnNew(self,event):
        Subframe = formulas_write.TestFrame()
        Subframe.Show()

    def OnRevise(self,event):
        Subframe = formulas_write.TestFrame()
        Subframe.Show()

    def OnDelete(self,event):
        #dialog = wx.MessageDialog(None,u'确定要删除这个公式？',u'警告框',
        #                          wx.YES_NO|wx.ICON_QUESTION)
        #retCode = dialog.ShowModal()
        retCode = wx.MessageBox(u'确定要删除这个公式？此操作是无法恢复的',u'警告框',
                                wx.YES_NO | wx.ICON_INFORMATION)
        if (retCode == wx.ID_YES):
            print 'yes'
        else:
            print 'no'
        #dialog.Destroy()

    def OnFind(self,event):
        dialog = wx.TextEntryDialog(None,
                                    u'输入您想要查找的公式名：',                                
                                    u'查找框',u'默认值',wx.OK | wx.CANCEL )
        if dialog.ShowModal()==wx.ID_OK:
            print "You want to find %s"%dialog.GetValue()
        dialog.Destroy()

    def OnView(self,event):
        Subframe = draw_Dayline.DrawFrame()
        Subframe.Show()

    def OnInput(self,event):
        wildcard = u'5.0版公式文件（*.tne）|*.tne|'\
                   u'4.0版公式文件（*.tni）|*.tni|'\
                   u'旧版公式文件（*.tnc）|*.tnc'
        #导入的时候找文件，并提供格式
        dialog = wx.FileDialog(None,u'导入公式','','',wildcard,wx.OPEN)
        if dialog.ShowModal()==wx.ID_OK:
            print dialog.GetPath()
        dialog.Destroy()

    def OnOutput(self,event):
        #wildcard = u'公式导出文件（*|tne）|*.tne'
        #导出的时候找目录，默认格式*.tne即可
        dialog = wx.DirDialog(None,u'导出公式','',wx.SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            print dialog.GetPath()
        dialog.Destroy()

    def AddTreeNodes(self,parentItem,items):
        for item in items:
            if type(item) == str:
                self.tree.AppendItem(parentItem,item)
            else:
                newItem = self.tree.AppendItem(parentItem,item[0])
                self.AddTreeNodes(newItem,item[1])

            

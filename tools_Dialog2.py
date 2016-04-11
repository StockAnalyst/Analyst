#!/usr/bin/env python
#-*- coding:UTF-8 -*- 

import wx
import wx.grid
import data

#模板管理器界面（包含显示所有模板+修改）
class SubclassDialog2(wx.Dialog):#自定义的
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u'模板管理器',size=(500,200))

        #这里利用grid（其实用listCtrl就足够了，但是不会用--imageList的部分？？）
        colLabels = [u'模板名',u'基本信息']
        grid = wx.grid.Grid(self,-1,size=(500,115))
        grid.CreateGrid(len(data.column1),2)
        grid.EnableEditing(False)#设置为不可编辑的状态
        
        #设置表头
        grid.SetColLabelValue(0,colLabels[0])
        grid.SetColLabelValue(1,colLabels[1])

        #设置表内容
        '''
        i = 0
        while i < len(data.column1):
            grid.SetCellValue(i,0,data.column1[i])
            grid.SetCellValue(i,1,data.column2[i])
            ++i
        grid.AutoSizeColumns(setAsMin=True)
        '''   
        grid.SetCellValue(0, 0,data.column1[0])
        grid.SetCellValue(0, 1,data.column2[0])
        grid.SetCellValue(1, 0,data.column1[1])
        grid.SetCellValue(1, 1,data.column2[1])
        grid.AutoSizeColumns(setAsMin=True)
        grid.SetCellValue(2, 0,data.column1[2])
        grid.SetCellValue(2, 1,data.column2[2])
        grid.SetCellValue(3, 0,data.column1[3])
        grid.SetCellValue(3, 1,data.column2[3])
        
        #所有按钮
        #NameButton = wx.Button(self,wx.ID_OK,u'更名',pos=(100,125))
        NameButton = wx.Button(self,-1,u'更名',pos=(50,125))
        self.Bind(wx.EVT_BUTTON,self.OnName,NameButton)
        
        DeleteButton = wx.Button(self,-1,u'删除',pos=(150,125))
        self.Bind(wx.EVT_BUTTON,self.OnDelete,DeleteButton)

        AddButton = wx.Button(self,-1,u'新增',pos=(250,125))
        self.Bind(wx.EVT_BUTTON,self.OnAdd,AddButton)

        #这两个暂时没什么作用，也没绑定事件
        CancelButton = wx.Button(self,wx.ID_CANCEL,u'取消',pos=(350,125))
        

    def OnName(self,event):
        dialog = wx.TextEntryDialog(None,
                                    u'输入修改后的名字：',                                
                                    u'更名框',u'默认值',wx.OK | wx.CANCEL )
        if dialog.ShowModal()==wx.ID_OK:
            print "You want to change its name to %s"%dialog.GetValue()
        dialog.Destroy()

    def OnDelete(self,event):
        retCode = wx.MessageBox(u'确定要删除这个模板？此操作是无法恢复的',u'警告框',
                                wx.YES_NO | wx.ICON_INFORMATION)
        if (retCode == wx.ID_YES):
            print 'yes'
        else:
            print 'no'

    def OnAdd(self,event):
        dialog = wx.TextEntryDialog(None,
                                    u'新增模板基本信息：',                                
                                    u'新增框',u'模板名：基本信息：',wx.OK | wx.CANCEL|wx.TE_MULTILINE )
        if dialog.ShowModal()==wx.ID_OK:
            print "You want to add a new one -> %s"%dialog.GetValue()
        dialog.Destroy()

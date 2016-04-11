#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#FILE:公式编辑器

import wx
import wx.grid
import data
import draw_Dayline

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u'公式编辑器',size=(600,400))
        panel = wx.Panel(self)

    #1.设置所有的窗口
        #第一行左半部分
        fnameLabel = wx.StaticText(panel,-1,u'公式名称',pos=(15,15)) 
        fname = wx.TextCtrl(panel,-1,'',pos=(65,15))

        ftypeLabel = wx.StaticText(panel,-1,u'公式类型',pos=(185,15))
        ftype = wx.ComboBox(panel,-1,u'请选择',(235,15),wx.DefaultSize,data.typeList,wx.CB_DROPDOWN)

        fdesLabel = wx.StaticText(panel,-1,u'公式描述',pos=(15,45)) 
        fdes = wx.TextCtrl(panel,-1,'',pos=(65,45))
        
        fmethodLabel = wx.StaticText(panel,-1,u'画线方法',pos=(185,45))
        fmethod = wx.ComboBox(panel,-1,u'请选择',(235,45),wx.DefaultSize,data.methodList,wx.CB_DROPDOWN)
                
        fpassButton = wx.Button(panel,-1,u"密码保护",pos=(15,75))
        self.Bind(wx.EVT_BUTTON,self.OnFpass,fpassButton)

        #第一行右半部分
        colLabels = [u'参数',u'最小',u'最大',u'缺省']
        grid = wx.grid.Grid(panel,-1,(450,15),(435,100))
        grid.CreateGrid(16,4) 
        for col in range(4):
            grid.SetColLabelValue(col,colLabels[col])
            for row in range(16):
                grid.SetCellValue(row, col,'')

        #第二行所有按钮
        YesButton = wx.Button(panel, wx.ID_OK, u'确定')#确定和测试公式按钮一样的效果，在输出框中给出结果
        
        CancelButton = wx.Button(panel,-1,u'取消')
        self.Bind(wx.EVT_BUTTON,self.OnCancel,CancelButton)
        
        StoreButton = wx.Button(panel, -1,u'存为')
        self.Bind(wx.EVT_BUTTON,self.OnStore,StoreButton)
        
        InsertFuncButton = wx.Button(panel, -1,u'插入函数')#弹框出来一个新的界面
        self.Bind(wx.EVT_BUTTON,self.OnInsertFunc,InsertFuncButton)
        
        #InsertResButton = wx.Button(panel, -1,u'插入资源')
        TestForButton = wx.Button(panel, -1,u'测试公式')
        
        ViewButton = wx.Button(panel, -1,u'应用于图')
        self.Bind(wx.EVT_BUTTON,self.OnView,ViewButton)
        
        YesButton.SetDefault()
        
        #第三行
        fmultiIn = wx.TextCtrl(panel,-1,u'公式输入',style=wx.TE_MULTILINE,pos=(15,165),size=(870,200))#?这里是否有必要搞成丰富文本
        
        #第四行
        fmultiOutBox = wx.ComboBox(panel,-1,u'请选择',(15,385),(100,300),data.outputList,wx.CB_SIMPLE)
        fmultiOut = wx.TextCtrl(panel,-1,u'各类输出',style=wx.TE_MULTILINE,pos=(135,385),size=(735,150))#?这里是否有必要搞成丰富文本

    #2.利用sizer开始设置布局
        #mainSizer是最高级别的sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        #第一行firstSizer
        firstSizer = wx.BoxSizer(wx.HORIZONTAL)
        firstleftSizer = wx.FlexGridSizer(cols=4,hgap=5,vgap=5)
        firstleftSizer.Add(fnameLabel,0,0)
        firstleftSizer.Add(fname,0,0)
        firstleftSizer.Add(ftypeLabel,0,0)
        firstleftSizer.Add(ftype,0,0)
        firstleftSizer.Add(fdesLabel,0,0)
        firstleftSizer.Add(fdes,0,0)
        firstleftSizer.Add(fmethodLabel,0,0)
        firstleftSizer.Add(fmethod,0,0)
        firstleftSizer.Add(fpassButton,0,0)
        firstleftSizer.AddGrowableCol(0,0)
        firstleftSizer.AddGrowableCol(1,1)
        firstleftSizer.AddGrowableCol(2,0)
        firstleftSizer.AddGrowableCol(3,1)
        firstleftSizer.AddGrowableRow(0,0)
        firstleftSizer.AddGrowableRow(1,0)
        firstleftSizer.AddGrowableRow(2,0)
        firstSizer.Add(firstleftSizer,0,0,5)
        firstSizer.Add(grid,1,0,5)
        mainSizer.Add(firstSizer,0,0,5)

        #第二行secondSizer       
        secondSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(YesButton)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(CancelButton)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(StoreButton)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(InsertFuncButton)
        #secondSizer.Add((20,20), 1)
        #secondSizer.Add(InsertResButton)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(TestForButton)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(ViewButton)
        secondSizer.Add((20,20), 1)
        mainSizer.Add(secondSizer,0,wx.EXPAND,10)
        
        #第三行thirdSizer
        mainSizer.Add(fmultiIn,2,wx.EXPAND,10)

        #最后一行lastSizer
        lastSizer = wx.BoxSizer(wx.HORIZONTAL)
        lastSizer.Add(fmultiOutBox)
        lastSizer.Add(fmultiOut,1)
        mainSizer.Add(lastSizer,1,wx.EXPAND,10)
        
        panel.SetSizer(mainSizer)
        mainSizer.Fit(self)

    def OnFpass(self,event):
        dialog = wx.TextEntryDialog(None,
                                    u'输入您的密码保护：',                                
                                    u'密码保护框','',wx.OK | wx.CANCEL | wx.TE_PASSWORD)
        if dialog.ShowModal()==wx.ID_OK:
            print 'You have set a password!'
        dialog.Destroy()

    def OnYes(self,event):
        pass

    def OnCancel(self,event):
        retCode = wx.MessageBox(u'确定要放弃此前的编辑？此操作是无法恢复的',u'警告框',
                                wx.YES_NO | wx.ICON_INFORMATION)
        if (retCode == wx.ID_YES):
            print 'yes'
        else:
            print 'no'
        
    def OnStore(self,event):
        dialog = wx.DirDialog(None,u'另存为','',wx.SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            print dialog.GetPath()
        dialog.Destroy()

    def OnInsertFunc(self,event):
        pass

    def OnView(self,event):
        Subframe = draw_Dayline.DrawFrame()
        Subframe.Show()
        
'''if __name__ == '__main__':
    app = wx.PySimpleApp()
    TestFrame().Show()
    app.MainLoop()'''

#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#FILE:初始菜单


import wx
import tools_Dialog1
import tools_Dialog2
import f10_display
import f10_with_processbar_final

#主页面（左右分块+菜单项。。）        
class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Init',size=(900,600))
        p = wx.Panel(self)
        self.CreateStatusBar()
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menuBar.Append(menu, 'First')
        menu2 = wx.Menu()
        menuBar.Append(menu2, 'Second')
        
        menu3 = wx.Menu()
        child1 = menu3.Append(-1,u'公式管理器','there are lots of formulas')
        self.Bind(wx.EVT_MENU,self.OnChild1,child1)
        child2 = menu3.Append(-1,u'模板管理器','there are lots of templates')
        self.Bind(wx.EVT_MENU,self.OnChild2,child2)
        menuBar.Append(menu3,u'工具')
        #实现菜单栏menu的快捷键，方式为 alt+T
        #menuBar.Append(menu3, '&Tools')

        menu4 = wx.Menu()
        #child3 = menu4.Append(-1,u'个股资料','there are sorts of information')
        #self.Bind(wx.EVT_MENU,self.OnChild3,child3)
        
        #利用wx.MenuItem来创建菜单项，便于设置快捷键Ctrl+Q或者F1-10
        child3 = wx.MenuItem(menu4,1,u'&个股数据\tF10')
        menu4.AppendItem(child3)
        self.Bind(wx.EVT_MENU,self.OnChild3,id = 1)
        menu4.AppendSeparator()

        #二级菜单的设置，正常设置menu,但是不加入到menubar而是menu中即可
        child4 = wx.Menu()
        child4_1=child4.Append(-1,u'更新所有')
        self.Bind(wx.EVT_MENU,self.OnChild4_1,child4_1)
        child4_2=child4.Append(-1,u'更新SZ板块')
        child4_3=child4.Append(-1,u'更新SH板块')
        #注意区别的是，这里用appendmenu而不是appenditem
        menu4.AppendMenu(-1,u'更新个股资料',child4)
        
        menuBar.Append(menu4,u'微系统')
        
        self.SetMenuBar(menuBar)


    def OnChild1(self,event):
        dlg = tools_Dialog1.SubclassDialog1()
        if dlg.ShowModal() == wx.ID_CANCEL:
            print "cancel1"
        else:
            print "OK1"
        #dlg = wx.SingleChoiceDialog(None,'which formula do you select?',
         #                           'formulas manager',['3','2'])
        #if dlg.ShowModal() == wx.ID_OK:
          #  reponse = dlg.GetStringSelection()
        #这里必须要销毁，否接不能够正常结束
        dlg.Destroy()

    def OnChild2(self,event):
        dlg = tools_Dialog2.SubclassDialog2()
        if dlg.ShowModal() == wx.ID_CANCEL:
            print "cancel2"
        else:
            print "OK2"
        dlg.Destroy()

    def OnChild3(self,event):
        Subframe = f10_display.TestFrame1()
        Subframe.Show()

        #日志相关
        import loggerfun
        loggerfun.fun3()

    def OnChild4_1(self,event):
        f10_with_processbar_final.update_f10()
        
                                    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    
    #启动提示
    provider = wx.CreateFileTipProvider('tips.py',0)
    wx.ShowTip(None,provider,True)
    
    frame = MyFrame()
    frame.Show()

    #日志相关father层次
    import loggerfun
    loggerfun.fun0_s()
    app.MainLoop()
    loggerfun.fun0_f()
    

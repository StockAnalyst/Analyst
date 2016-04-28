#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#FILE:公式管理器

import wx
import os
import data
import formulas_write
import draw_Dayline

moshi_tool = 0 #取值为1（revice），2(delete)，3(find),4(output)
canshu_tool = ''
string_input = ''
string_temp = ''

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

        #创建一个树(style = wx.TR_HIDE_ROOT不显示根节点？)
        self.tree = wx.TreeCtrl(self,size=(275,475))
        #增加一个根节点
        root = self.tree.AddRoot(u"所有公式")
        #增加各种节点（通过文件）
        self.AddTreeNodes(root,data.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.OnTreeSelChanged)

    def AddTreeNodes(self,parentItem,items):
        for item in items:
            if type(item) == str:
                self.tree.AppendItem(parentItem,item)
            else:
                newItem = self.tree.AppendItem(parentItem,item[0])
                self.AddTreeNodes(newItem,item[1])

    mouse_in_treeCtrl = ''
    def OnTreeSelChanged(self,event):
        treeitem = event.GetItem()
        self.mouse_in_treeCtrl = self.tree.GetItemText(treeitem)
        #print self.mouse_in_treeCtrl

    def OnNew(self,event):
        if self.mouse_in_treeCtrl in data.typeList:
            Subframe = formulas_write.TestFrame(self.mouse_in_treeCtrl,1,0,[])
            Subframe.Show()
        elif self.mouse_in_treeCtrl in data.typeList1:
            Subframe = formulas_write.TestFrame(self.mouse_in_treeCtrl,2,0,[])
            Subframe.Show()
        elif self.mouse_in_treeCtrl == u'专家系统公式' or self.mouse_in_treeCtrl == u'五彩K线公式':
            Subframe = formulas_write.TestFrame('',3,0,[])
            Subframe.Show()
        else:
            wx.MessageBox(u'请在左边公式树中选择一种类型(父亲节点)，如：大势型',u'指示框')

    def OnRevise(self,event):
        self.OpenFormulasWrite(1,self.mouse_in_treeCtrl)
    
    def OnDelete(self,event):
        #dialog = wx.MessageDialog(None,u'确定要删除这个公式？',u'警告框',
        #                          wx.YES_NO|wx.ICON_QUESTION)
        #retCode = dialog.ShowModal()
        self.OpenFormulasWrite(2,self.mouse_in_treeCtrl)

    def OnFind(self,event):
        dialog = wx.TextEntryDialog(None,
                                    u'输入您想要查找的公式名,如：',                                
                                    u'查找框','ABI',wx.OK | wx.CANCEL )
        
        if dialog.ShowModal()==wx.ID_OK:
            print "You want to find %s"%dialog.GetValue()
        self.OpenFormulasWrite(3,dialog.GetValue())
        dialog.Destroy()

    #这里还存在问题，没有研究透彻，有些可以画图，有些不能画图。。。
    #包括画图方法有很多：副图，主图叠加。。。。
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
        self.OpenFormulasWrite(4,self.mouse_in_treeCtrl)
        #wildcard = u'公式导出文件（*|tne）|*.tne'
        #导出的时候找目录，默认output.txt即可

    
    def zhuanma(self, string_input):
        if isinstance(string_input,unicode):
            print string_input.encode('gb2312')
        else:
            #print string_input.decode('utf-8').encode('gb2312')
            print string_input
            
    def OpenFormulasWrite(self, moshi_tool, canshu_tool):
        leaveListFinal = data.leaveListFinal[0]+data.leaveListFinal[1]+data.leaveListFinal[2]+data.leaveListFinal[3]
        if moshi_tool == 1 or moshi_tool == 3:
            if canshu_tool in leaveListFinal:
                if canshu_tool in data.leaveListFinal[0]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[0] + """ WHERE name = %s""",canshu_tool )
                    item1 = data.cursor.fetchone()
                    Subframe = formulas_write.TestFrame(canshu_tool,1,1,item1)
                if canshu_tool in data.leaveListFinal[1]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[1] + """ WHERE name = %s""",canshu_tool )
                    item1 = data.cursor.fetchone()
                    Subframe = formulas_write.TestFrame(canshu_tool,2,1,item1)
                if canshu_tool in data.leaveListFinal[2]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[2] + """ WHERE name = %s""",canshu_tool )
                    item1 = data.cursor.fetchone()
                    Subframe = formulas_write.TestFrame(canshu_tool,3,1,item1)
                if canshu_tool in data.leaveListFinal[3]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[3] + """ WHERE name = %s""",canshu_tool )
                    item1 = data.cursor.fetchone()
                    Subframe = formulas_write.TestFrame(canshu_tool,3,1,item1)
                Subframe.Show()
            else:
                if moshi_tool == 3:
                    wx.MessageBox(u'没有此公式，请重新输入：',u'指示框')
                else:
                    wx.MessageBox(u'请在左边公式树中选择一个公式(叶子节点)，如：ABI',u'指示框')
        elif moshi_tool == 2:
            if canshu_tool in leaveListFinal:
                if canshu_tool in data.leaveListFinal[0]:
                    data.cursor.execute("""SELECT attr FROM """ + data.tb_name[0] + """ WHERE name = %s""",canshu_tool )
                if canshu_tool in data.leaveListFinal[1]:
                    data.cursor.execute("""SELECT attr FROM """ + data.tb_name[1] + """ WHERE name = %s""",canshu_tool)
                if canshu_tool in data.leaveListFinal[2]:
                    data.cursor.execute("""SELECT attr FROM """ + data.tb_name[2] + """ WHERE name = %s""",canshu_tool )
                if canshu_tool in data.leaveListFinal[3]:
                    data.cursor.execute("""SELECT attr FROM """ + data.tb_name[3] + """ WHERE name = %s""",canshu_tool )
                message = data.cursor.fetchone()
                #print message[0]
                if message[0] == 'system':
                   wx.MessageBox(u'这是系统公式，不允许删除',u'指示框')
                else:
                    retCode = wx.MessageBox(u'确定要删除这个公式？此操作是无法恢复的',u'警告框',
                                wx.YES_NO | wx.ICON_INFORMATION)
                    if (retCode == wx.ID_YES):
                        print 'yes'
                    else:
                        print 'no'
            else:
                wx.MessageBox(u'请在左边公式树中选择一个公式(叶子节点)，如：ABI',u'指示框')
        elif moshi_tool == 4:
            if canshu_tool in leaveListFinal + data.sidafenlei:
                if canshu_tool == data.sidafenlei[0]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[0] + """ WHERE 1""")
                    code_index = 4
                elif canshu_tool == data.sidafenlei[1]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[1] + """ WHERE 1""")
                    code_index = 3
                elif canshu_tool == data.sidafenlei[2]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[2] + """ WHERE 1""")
                    code_index = 2
                elif canshu_tool == data.sidafenlei[3]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[3] + """ WHERE 1""")
                    code_index = 2
                elif canshu_tool in data.leaveListFinal[0]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[0] + """ WHERE name = %s""",canshu_tool )
                    code_index = 4
                elif canshu_tool in data.leaveListFinal[1]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[1] + """ WHERE name = %s""",canshu_tool )
                    code_index = 3
                elif canshu_tool in data.leaveListFinal[2]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[2] + """ WHERE name = %s""",canshu_tool )
                    code_index = 2
                elif canshu_tool in data.leaveListFinal[3]:
                    data.cursor.execute("""SELECT * FROM """ + data.tb_name[3] + """ WHERE name = %s""",canshu_tool )
                    code_index = 2
                item = data.cursor.fetchall()
                #print item
                dialog = wx.DirDialog(None,u'请选择非系统盘的根路径，如D:\\','',wx.SAVE)
                if dialog.ShowModal()==wx.ID_OK:

                    des_path = dialog.GetPath() + 'output.txt'
                    f = open(des_path,'a') #以追加模式打开，实现写多条的功能

                    #获取目的路径下所有文件/文件夹名字（一级）
                    current_files = os.listdir(dialog.GetPath())
                    #保证不受上一次操作的影响,先清空
                    if 'output.txt' in current_files:
                        f.truncate()
                    
                    for one in item:
                        src_path = one[code_index]
                        f1 = open(src_path)
                        txt = f1.read()
                        f1.close()
                        f.write('\n\n-------------------------------------------------------------------\n\n')
                        f.write(txt)
                        for one_one in one:
                            #通过重定向写入文件(解决这个问题：报错 ascii code can't decode)
                            import sys
                            output = sys.stdout
                            outputfile = open(des_path,'a')
                            sys.stdout = outputfile
                            self.zhuanma(one_one)
                            #恢复正常
                            outputfile.close()
                            sys.stdout = output
                            
                    f.close()
                dialog.Destroy()
            else:
                wx.MessageBox(u'导出单个公式---请在左边公式树种选择一个公式（叶子节点），如：ABI\n' +
                              u'导出多个公式：请在左边公式树中选择一种大的类型(父亲节点)，如:技术指标公式', u'指示框')

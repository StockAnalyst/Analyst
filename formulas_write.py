#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#FILE:当前版本的公式编辑器(技术指标界面,区分不同界面，设置函数)

import wx
import wx.grid
import data
import draw_Dayline
import dtfy
import csjg
import sys
import function_insert

helpMessage=u'''测试不通过!
                请按照规定语法编写公式：
                1.单词之间以空格分隔
                2.每一句以；结尾
                3.语句的合法形式为 左值 :=/： 函数/表达式 ;
                4.函数的合法形式为 函数名 （ 参数1 ， 参数2 ）
                5.表达式的合法形式为 （ 表达式 ）
                '''
path = ''
fenlei = 0
canshu = ''
class TestFrame(wx.Frame):
    #模式取值范围0（新建），1（修改）对应不同控件中否，是有值
    #分类取值范围1，2，3对应三种不同界面
    def __init__(self,canshu_1,fenlei_1,moshi,item):
        global fenlei,canshu
        canshu = canshu_1
        fenlei = fenlei_1
        wx.Frame.__init__(self,None,-1,u'公式编辑器',size=(600,300))
        panel = wx.Panel(self)

    #1.设置所有的窗口
        #第一行左半部分
        global fname,fdes,fmethod,ftype
        fnameLabel = wx.StaticText(panel,-1,u'公式名称',pos=(15,15)) 
        fname = wx.TextCtrl(panel,-1,'',pos=(65,15))
        if moshi == 1:
            fname.SetValue(item[0])
        #公式类型 界面1和界面2有，界面3没有
        if fenlei == 1 or fenlei ==2:
            ftypeLabel = wx.StaticText(panel,-1,u'公式类型',pos=(185,15))
            ftype = wx.ComboBox(panel,-1,u'请选择',(235,15),wx.DefaultSize,data.typeList,wx.CB_DROPDOWN)
            if moshi == 0:
                ftype.SetValue(canshu)
            if moshi == 1:
                ftype.SetValue(item[2])
        
        fdesLabel = wx.StaticText(panel,-1,u'公式描述',pos=(15,45)) 
        fdes = wx.TextCtrl(panel,-1,'',pos=(65,45))
        if moshi == 1:
            fdes.SetValue(item[1])
        #画线方法 界面1有，界面2和界面3没有
        if fenlei == 1:
            fmethodLabel = wx.StaticText(panel,-1,u'画线方法',pos=(185,45))
            fmethod = wx.ComboBox(panel,-1,u'请选择',(235,45),wx.DefaultSize,data.methodList,wx.CB_DROPDOWN)
            if moshi == 1:
                fmethod.SetValue(item[3])
                
        fpassButton = wx.Button(panel,-1,u"密码保护",pos=(15,75))
        self.Bind(wx.EVT_BUTTON,self.OnFpass,fpassButton)

        #第一行右半部分
        colLabels = [u'参数',u'最小',u'最大',u'缺省']
        grid = wx.grid.Grid(panel,-1,(450,15),(435,100))
        grid.CreateGrid(16,4)
        #构建参数grid
        for col in range(4):
            grid.SetColLabelValue(col,colLabels[col])
            for row in range(16):
                grid.SetCellValue(row, col,'')
        #设置参数表中的值(最好的方法是像公式源码一样分别写文件，作为公式的一个属性存入数据库中，
        #目前为了简便采用一个替代方法，把参数信息存在data.py的一个【】中)
        if moshi == 1:
            for col in range(4):
                if item[0]=='ABI':
                    grid.SetCellValue(0,col,data.canshu_func[0][col])
                elif item[0] == 'ADL':
                    grid.SetCellValue(0,col,data.canshu_func[1][col])
                elif item[0] == 'ADR':
                    grid.SetCellValue(0,col,data.canshu_func[2][col])
                    grid.SetCellValue(1,col,data.canshu_func[3][col])
                elif item[0] == 'ASRX':
                    grid.SetCellValue(0,col,data.canshu_func[4][col])
                elif item[0] == 'ASRD':
                    grid.SetCellValue(0,col,data.canshu_func[5][col])
                elif item[0] == 'BIAS':
                    grid.SetCellValue(0,col,data.canshu_func[6][col])
                    grid.SetCellValue(1,col,data.canshu_func[7][col])
                    grid.SetCellValue(2,col,data.canshu_func[8][col])
                elif item[0] == 'CCIzj':
                    grid.SetCellValue(0,col,data.canshu_func[9][col])
            

        #第二行所有按钮
        YesButton = wx.Button(panel, wx.ID_OK, u'保存公式')#测试+（正确且没有）存入数据库/（错误）报错修改
        self.Bind(wx.EVT_BUTTON,self.OnYes,YesButton)
        
        #CancelButton = wx.Button(panel,wx.ID_CANCEL,u'取消')
        self.Bind(wx.EVT_CLOSE,self.OnCancel)#放弃当前所有修改，并关闭当前对话框
        
        StoreButton = wx.Button(panel, -1,u'另存为')#将公式源码和动态翻译结果存储
        self.Bind(wx.EVT_BUTTON,self.OnStore,StoreButton)
        
        InsertFuncButton = wx.Button(panel, -1,u'插入函数')#弹框出来一个新的界面
        self.Bind(wx.EVT_BUTTON,self.OnInsertFunc,InsertFuncButton)
        
        TestForButton = wx.Button(panel, -1,u'测试公式')#测试公式语法语义上是否有错，在输出框中给出结果
        self.Bind(wx.EVT_BUTTON,self.OnTestFor,TestForButton)
        
        if fenlei == 1:
            ViewButton = wx.Button(panel, -1,u'应用于图')
            self.Bind(wx.EVT_BUTTON,self.OnView,ViewButton)
        
        YesButton.SetDefault()
        
        #第三行
        global fmultiIn
        fmultiIn = wx.TextCtrl(panel,-1,u'公式输入',style=wx.TE_MULTILINE,pos=(15,165),size=(870,200))#?这里是否有必要搞成丰富文本
        if moshi == 1:
            global path
            f = open(item[5-fenlei])
            buffer = f.read()
            fmultiIn.SetValue(buffer)
            path = item[5-fenlei]
            
        #第四行
        global fmultiOutBox
        fmultiOutBox = wx.ComboBox(panel,-1,u'请选择',(15,385),(100,300),data.outputList,wx.CB_SIMPLE)
        self.Bind(wx.EVT_COMBOBOX,self.OnFmultioutbox,fmultiOutBox)
        global fmultiOut
        fmultiOut = wx.TextCtrl(panel,-1,'',style=wx.TE_MULTILINE,pos=(135,385),size=(735,150))#?这里是否有必要搞成丰富文本
        
    #2.利用sizer开始设置布局
        #mainSizer是最高级别的sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        #第一行firstSizer
        firstSizer = wx.BoxSizer(wx.HORIZONTAL)
        firstleftSizer = wx.FlexGridSizer(cols=4,hgap=5,vgap=5)
        firstleftSizer.Add(fnameLabel,0,0)
        firstleftSizer.Add(fname,0,0)

        if fenlei == 1 or fenlei == 2:
            firstleftSizer.Add(ftypeLabel,0,0)
            firstleftSizer.Add(ftype,0,0)
        firstleftSizer.Add(fdesLabel,0,0)
        firstleftSizer.Add(fdes,0,0)
        if fenlei == 1:
            firstleftSizer.Add(fmethodLabel,0,0)
            firstleftSizer.Add(fmethod,0,0)
        firstleftSizer.Add(fpassButton,0,0)

        #设置控件的 行列 可扩展属性
        firstleftSizer.AddGrowableCol(0,0)
        firstleftSizer.AddGrowableCol(1,1)
        firstleftSizer.AddGrowableCol(2,0)
        firstleftSizer.AddGrowableCol(3,1)
        firstleftSizer.AddGrowableRow(0,0)
        firstleftSizer.AddGrowableRow(1,0)
        #只有界面1有三行按钮控件
        if fenlei == 1:
            firstleftSizer.AddGrowableRow(2,0)
        firstSizer.Add(firstleftSizer,0,0,5)
        firstSizer.Add(grid,1,0,5)
        mainSizer.Add(firstSizer,0,0,5)

        #第二行secondSizer       
        secondSizer = wx.BoxSizer(wx.HORIZONTAL)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(YesButton)
        secondSizer.Add((20,20), 1)
        #secondSizer.Add(CancelButton)
        #secondSizer.Add((20,20), 1)
        secondSizer.Add(StoreButton)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(InsertFuncButton)
        secondSizer.Add((20,20), 1)
        secondSizer.Add(TestForButton)
        secondSizer.Add((20,20), 1)
        if fenlei == 1:
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

        import loggerfun
        loggerfun.fun1()

    def OnFpass(self,event):
        dialog = wx.TextEntryDialog(None,
                                    u'输入您的密码保护：',                                
                                    u'密码保护框','',wx.OK | wx.CANCEL | wx.TE_PASSWORD)
        if dialog.ShowModal()==wx.ID_OK:
            print 'You have set a password!'
        dialog.Destroy()

    def OnCancel(self,event):
        retCode = wx.MessageBox(u"确定放弃之前操作？此操作不可恢复",u'警告框',wx.OK|wx.CANCEL)
        if retCode == wx.OK:
            event.Skip() #继续执行默认的关闭操作
        
    def OnStore(self,event):
        dialog = wx.DirDialog(None,u'另存为','',wx.SAVE)
        if dialog.ShowModal()==wx.ID_OK:
            des_path = dialog.GetPath() + 'Store_formula.txt'
            f = open(des_path , 'w')
            import os
            current_files = os.listdir(dialog.GetPath())
            if 'Store_formula.txt' in current_files: #清空，去除影响
                f.truncate()
            global fmultiIn
            f.write(u'公式源码:\n'.encode('gbk'))
            f.write(fmultiIn.GetValue().encode('gbk'))
            f.write('\n')
            dtfy.readString(fmultiIn.GetValue())
            tempstring = dtfy.transResult()
            f.write(u'公式意义:\n'.encode('gbk'))
            f.write(tempstring.encode('gbk'))
            f.close()
        dialog.Destroy()

    def OnInsertFunc(self,event):
        dlg = function_insert.funcInsertDialog()
        if dlg.ShowModal() == wx.ID_CANCEL:
            if function_insert.status == True:
                value = fmultiIn.GetValue()
                temp = value + function_insert.retCode
                fmultiIn.SetValue(temp)
        else:
            pass            
        dlg.Destroy()

    def OnTestFor(self,event):
        fmultiOutBox.SetSelection(1)
        global helpMessage
        #csjg.readFile(path)
        csjg.readString(fmultiIn.GetValue())
        csjg.parseResult()
        results = csjg.execFormula(csjg.midResultlist)
        if results == 'error':
            fmultiOut.SetValue(helpMessage)
        else:
            fmultiOut.SetValue(u'测试通过!')

    def OnYes(self,event):
        #先测试，确保正确之后才能入库
        global helpMessage,fmultiIn,canshu
        csjg.readString(fmultiIn.GetValue())
        csjg.parseResult()
        results = csjg.execFormula(csjg.midResultlist)
        if results == 'error':
            fmultiOutBox.SetSelection(1)
            fmultiOut.SetValue(helpMessage)
        else:
            global fname,fdes,fmethod,ftype  #准备所有的数据
            item0 = fname.GetValue()
            item1 = fdes.GetValue()
            if fenlei == 1 or fenlei == 2:
                item2 = ftype.GetValue()
            if fenlei == 1:
                item3 = fmethod.GetValue()
            #这里仅仅是一个临时的方法，演示时仅用到这两个(暂时这么来测试)    
            if canshu == u'大势型' or canshu == 'ADR':
                item4 = 'C:\\Users\\fujia\\tdx_formula\\jszb\\ds\\'+ item0 + '.txt'
            if canshu == u'专家系统公式' or canshu == 'CCIzj':
                item4 = 'C:\\Users\\fujia\\tdx_formula\\zjxt\\'+ item0 + '.txt'
            code = fmultiIn.GetValue()
            import data        #存入数据库
            if fenlei == 1:
                self.chachong(data.tb_name[0],item0)
                data.cursor.execute("""INSERT INTO """ + data.tb_name[0] + """(name,describtion,type,dmethod,code,attr) VALUES(%s,%s,%s,%s,%s,%s)""",
                                            (item0,item1,item2,item3,item4,'user'))
            elif fenlei == 3:
                self.chachong(data.tb_name[2],item0)
                data.cursor.execute("""INSERT INTO """ + data.tb_name[2] + """(name,describtion,code,attr) VALUES(%s,%s,%s,%s)""",
                                            (item0,item1,item4,'user'))
            f = open(item4,'w')
            f.seek(0)
            f.write(code)
            f.close()
            data.db.commit()
            reload(data)
            wx.MessageBox(u'成功存入数据库，重新加载以查看',u'指示框')
        results = []

    def chachong(self,tbname,item0):
        data.cursor.execute("""SELECT name FROM """+ tbname + """ WHERE 1""")
        names = data.cursor.fetchall()
        if item0 in names:
            data.cursor.execute('''DELETE FROM '''+ tbname + """ WHERE name=%s""",item0)
        
    def OnView(self,event):
        global helpMessage,fmultiIn
        csjg.readString(fmultiIn.GetValue())
        csjg.parseResult()
        results = csjg.execFormula(csjg.midResultlist)
        if results == 'error':
            fmultiOutBox.SetSelection(1)
            fmultiOut.SetValue(helpMessage)
        else:
            fmultiOut.SetValue(u'测试通过!')
            lista = []
            for i in range(len(results[0])):
                lista.append(i)
            Subframe = draw_Dayline.DrawFrame(lista,results,'000001')
            Subframe.Show()
        results = []

    def OnFmultioutbox(self,event):
        if event.GetSelection()==0:
            global fmultiIn
            #dtfy.readFile(path)
            dtfy.readString(fmultiIn.GetValue())#读string的话涉及到转码的问题
            tempstring = dtfy.transResult()
            fmultiOut.SetValue(tempstring)
        elif event.GetSelection() == 1:
            global helpMessage
            #csjg.readFile(path)
            csjg.readString(fmultiIn.GetValue())
            csjg.parseResult()
            results = csjg.execFormula(csjg.midResultlist)
            if results == 'error':
                fmultiOut.SetValue(helpMessage)
            else:
                fmultiOut.SetValue(u'测试通过!')
'''
if __name__ == '__main__':
    app = wx.PySimpleApp()
    TestFrame().Show()
    app.MainLoop()

'''


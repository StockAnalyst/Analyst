#!/usr/bin/env python
#-*- coding=utf-8 -*-
#FILE:实现网格的顺序排列，左键单击从小到大哦，右键单击从大到小（final版本）

import wx
import wx.grid

data =[["1","2","10.1","Dernier"],["2","1","20.2","Sandberg"],["3","7","30.3","Matthews"],["4","5","40.4","Durham"]
        ,["5","8","50.5","Moreland"],["6","4","60.6","Cey"],["7","3","70.7","Davis"],["8","6","80.8","Bowa"]
        ,["9","9","90.9","Sutcliffe"]]
colLabels = ("Last","Second","First")

#对于大量数据的，操作较多，变化较多的网格最好使用自定义网格类
class LineupTable(wx.grid.PyGridTableBase): 
    
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)

    def GetNumberRows(self):
        return len(data)
    
    def GetNumberCols(self):
        return len(data[0])-1

    def GetColLabelValue(self,col):
        return colLabels[col]

    def GetRowLabelValue(self,row):
        return data[row][0]

    def IsEmptyCell(self,row,col):
        return False

    def GetValue(self,row,col):
        return data[row][col+1]

    def SetValue(self,row,col,value):
        pass

#按照从小到大排序(1表示第一列，2表示第二列，3表示第三列)
'''dataSortBigger1 = []
dataSortBigger2 = []
dataSortBigger3 = []'''
dataSortBigger = [[]for i in range(3)]
def sortMin(data,col):
    data_temp = []
    for data1 in data:
        data_temp.append(data1)
    while len(data_temp):
        min1 = data_temp[0]
        for data1 in data_temp:
            if data1[col] < min1[col]:
                min1 = data1
        dataSortBigger[col-1].append(min1)
        '''if col == 1:
            dataSortBigger1.append(min1)
        if col == 2:
            dataSortBigger2.append(min1)
        if col == 3:
            dataSortBigger3.append(min1)'''
        data_temp.remove(min1)

#按照从小到大排序
class LineupTableBigger(wx.grid.PyGridTableBase): 
    
    def __init__(self,dataSortBigger):
        wx.grid.PyGridTableBase.__init__(self)
        self.dataSortBigger = dataSortBigger

    def GetNumberRows(self):
        return len(self.dataSortBigger)
    
    def GetNumberCols(self):
        return len(self.dataSortBigger[0])-1

    def GetColLabelValue(self,col):
        return colLabels[col]

    def GetRowLabelValue(self,row):
        return self.dataSortBigger[row][0]

    def IsEmptyCell(self,row,col):
        return False

    def GetValue(self,row,col):
        return self.dataSortBigger[row][col+1]

    def SetValue(self,row,col,value):
        pass

#按照从大到小排序(1表示第一列，2表示第二列，3表示第三列)
'''dataSortSmaller1 = []
dataSortSmaller2 = []
dataSortSmaller3 = []'''
dataSortSmaller = [[]for i in range(3)]
def sortMax(data,col):
    data_temp = []
    for data1 in data:
        data_temp.append(data1)
    while len(data_temp):
        max1 = data_temp[0]
        for data1 in data_temp:
            if data1[col] > max1[col]:
                max1 = data1
        dataSortSmaller[col-1].append(max1)
        '''if col == 1:
            dataSortSmaller1.append(max1)
        if col == 2:
            dataSortSmaller2.append(max1)
        if col == 3:
            dataSortSmaller3.append(max1)'''
        data_temp.remove(max1)

#按照从大到小排序
class LineupTableSmaller(wx.grid.PyGridTableBase): 
    
    def __init__(self,dataSortSmaller):
        wx.grid.PyGridTableBase.__init__(self)
        self.dataSortSmaller = dataSortSmaller

    def GetNumberRows(self):
        return len(self.dataSortSmaller)
    
    def GetNumberCols(self):
        return len(self.dataSortSmaller[0])-1

    def GetColLabelValue(self,col):
        return colLabels[col]

    def GetRowLabelValue(self,row):
        return self.dataSortSmaller[row][0]

    def IsEmptyCell(self,row,col):
        return False

    def GetValue(self,row,col):
        return self.dataSortSmaller[row][col+1]

    def SetValue(self,row,col,value):
        pass
      
#主程序
class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent):
        for i in range(0,3):
            sortMin(data,i+1)
            sortMax(data,i+1)
        '''sortMin(data,1)
        sortMin(data,2)
        sortMin(data,3)
        sortMax(data,1)
        sortMax(data,2)
        sortMax(data,3)'''
        #初始化
        wx.grid.Grid.__init__(self,parent,-1)
        self.SetTable(LineupTable())

        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK,self.OnLeftClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK,self.OnRightClick)

    def OnLeftClick(self,event):
        for i in range(0,3):
            if event.GetCol()==i:
                self.SetTable(LineupTableBigger(dataSortBigger[i]))
                self.Refresh()
        '''if event.GetCol()==0:
            self.SetTable(LineupTableBigger1())
            self.Refresh()
        if event.GetCol()==1:
            self.SetTable(LineupTableBigger2())
            self.Refresh()
        if event.GetCol()==2:
            self.SetTable(LineupTableBigger3())
            self.Refresh()'''

    def OnRightClick(self,event):
        for i in range(0,3):
            if event.GetCol()==i:
                self.SetTable(LineupTableSmaller(dataSortSmaller[i]))
                self.Refresh()
        '''if event.GetCol()==0:
            self.SetTable(LineupTableSmaller1())
            self.Refresh()
        if event.GetCol()==1:
            self.SetTable(LineupTableSmaller2())
            self.Refresh()
        if event.GetCol()==2:
            self.SetTable(LineupTableSmaller3())
            self.Refresh()'''
    
class TestFrame(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self,parent,-1,"A Grid")
        grid = SimpleGrid(self)
        

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = TestFrame(None)
    frame.Show(True)
    app.MainLoop()


#!/usr/bin/env python
# -*- coding:utf-8 -*-
#单独的进度条（函数形式，实际将这个穿插到需要的.py中，真是没用到）

import wx

#cmd下的进度条
'''
from __future__ import division
  
import sys,time
j = '#'
if __name__ == '__main__':
  for i in range(1,61):
    j += '#'
    sys.stdout.write(str(int((i/60)*100))+'% ||'+j+'->'+"\r")
    sys.stdout.flush()
    time.sleep(0.5)
print
'''

#wxpython下的进度条

def process_bar(progressMax):
    dialog = wx.ProgressDialog(u"进度条", u"当前进度", progressMax,  
            style=wx.PD_CAN_ABORT )
    keepGoing = True
    
    count = 0
    while keepGoing and count < progressMax:  
        count = count + 1
        
        if count%(progressMax/5) == 0:
            wx.Sleep(progressMax/10000)
            keepGoing = dialog.Update(count)

        '''
        if count == progressMax/5:
            #这里的休眠时间用实际操作的时间替代
            wx.Sleep(progressMax/10000)
            keepGoing = dialog.Update(count)
        if count == progressMax/5*2 :
            wx.Sleep(progressMax/10000)
            keepGoing = dialog.Update(count)
        if count == progressMax/5*3:
            wx.Sleep(progressMax/10000)
            keepGoing = dialog.Update(count)
        if count == progressMax/5*4:
            wx.Sleep(progressMax/10000)
            keepGoing = dialog.Update(count)
        if count == progressMax/5*5 :
            wx.Sleep(progressMax/10000)
            keepGoing = dialog.Update(count)
        '''
    print (count)
    dialog.Destroy()  
  
if __name__ == "__main__":  
    app = wx.PySimpleApp()
    process_bar(162882)


        


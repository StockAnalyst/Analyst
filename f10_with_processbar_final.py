#!/usr/bin/env python
# -*- coding:utf-8 -*-
#FILE:获取dzh F10数据并入库

import os
import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_mkt",charset='utf8')
cursor = db.cursor()

import wx

#获取目录下所有文件列表名，形如['000001.001','000001.002']
def get_recursive_file_list(path):
    current_files = os.listdir(path)
    all_files = []
    for file_name in current_files:
        full_file_name = file_name#全路径名
        all_files.append(full_file_name)

        if os.path.isdir(full_file_name):
            next_level_files = get_recursive_file_list(full_file_name)
            all_files.extend(next_level_files)

    return all_files

all_file_names1 = get_recursive_file_list('D:/dzh/dzh_gtja/data/SZnse/Base/')
nums1 = len(all_file_names1)
all_file_names2 = get_recursive_file_list('D:/dzh/dzh_gtja/data/SHase/Base/')
nums2 = len(all_file_names2)

def update_f10():
        
    progressMax = nums1 + nums2
    dialog = wx.ProgressDialog(u"进度条", u"当前进度", progressMax,  
            style=wx.PD_CAN_ABORT )
    keepGoing = True
    i = 0
    #并没有做更精细的判断，实际上需要的
    while keepGoing and i < (progressMax/10000+1)*10000:

        if i<nums1:
            name = all_file_names1[i].split('.')
            if name[1] == 'f10':
                i = i + 1
                continue
            #避免转义字符\或者可以利用r'D:\dzh\data\SZnse\Base\000001.001'
            src = 'D:\\dzh\\data\\SZnse\\Base\\' + all_file_names1[i]
            des = 'D:\\F10\\SZ\\base\\' + name[1] + '\\' + name[0] + '.txt'
            command='copy ' + src + ' ' + des
            os.system(command)
            listF10 = []
            listF10.append(' ')
            listF10.append(name[0])
            listF10.append(des)
            listF10.append('SZ')
            cursor.execute("""INSERT INTO tb_"""+name[1]+""" VALUES (%s,%s,%s,%s)""",listF10)
            db.commit()
            i = i + 1
            if i%(progressMax/10000) == 0:
                keepGoing = dialog.Update(i)
            continue

        if i>=nums1 and i < progressMax:
            name = all_file_names2[i-nums1].split('.')
            if name[1] == 'f10':
                i = i + 1
                continue
            #避免转义字符\或者可以利用r'D:\dzh\data\SZnse\Base\000001.001'
            src = 'D:\\dzh\\data\\SHase\\Base\\' + all_file_names2[i-nums1]
            des = 'D:\\F10\\SH\\base\\' + name[1] + '\\' + name[0] + '.txt'
            command='copy ' + src + ' ' + des
            os.system(command)
            listF10 = []
            listF10.append(' ')
            listF10.append(name[0])
            listF10.append(des)
            listF10.append('SH')
            cursor.execute("""INSERT INTO tb_"""+name[1]+""" VALUES (%s,%s,%s,%s)""",listF10)
            db.commit()
            i = i + 1
            if i%(progressMax/10000) == 0:
                keepGoing = dialog.Update(i)
            continue

        else:
            i = i + 1
            if i%(progressMax/10000) == 0:
                keepGoing = dialog.Update(i)
            continue
            
    dialog.Destroy()
    cursor.close()
    db.close()

'''
if __name__ == '__main__':
    app = wx.PySimpleApp()
    update_f10()

'''




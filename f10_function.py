#!/usr/bin/env python
# -*- coding:utf-8 -*-
#FILE:获取dzh F10数据并入库（函数版本的，实际由于加上了进度条没用这个）

import os
import MySQLdb
db = MySQLdb.connect("127.0.0.1","root","root","db_f10",charset='utf8')
cursor = db.cursor()

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


#SZ数据F10
def getF10SZ():
    all_file_names = get_recursive_file_list('D:/dzh/data/SZnse/Base/')
    nums = len(all_file_names)
    for i in xrange(0,nums):
        name = all_file_names[i].split('.')
        if name[1] == 'f10':
            continue
        #避免转义字符\或者可以利用r'D:\dzh\data\SZnse\Base\000001.001'
        src = 'D:\\dzh\\data\\SZnse\\Base\\' + all_file_names[i]
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
    print ("All Done!")


#连续执行多条指令
#command='''mkdir hello & \
#ver & \
#'''

#SH数据F10
def getF10SH():
    all_file_names = get_recursive_file_list('D:/dzh/data/SHase/Base/')
    nums = len(all_file_names)
    for i in xrange(0,nums):
        name = all_file_names[i].split('.')
        if name[1] == 'f10':
            continue
        #避免转义字符\或者可以利用r'D:\dzh\data\SZnse\Base\000001.001'
        src = 'D:\\dzh\\data\\SHase\\Base\\' + all_file_names[i]
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
    print ("All Done!")
        
if __name__ == '__main__':
    getF10SH()
    getF10SZ()
    cursor.close()
    db.close()






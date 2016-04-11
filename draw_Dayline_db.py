#-*- coding:UTF-8 -*-
#!/usr/bin/env python
#FILE:画图的连接数据库取数据


import wx
import MySQLdb

#之前在建立数据库的时候，将date字段的类型设置成 DATE
conn = MySQLdb.connect(host ='localhost',port=3306,user='root',passwd='root',db='db_mkt')
#建立游标
cur = conn.cursor()
#我的数据库结构是data数据库下面有一个his_data的表，存着一只股票的所有历史数据
cur.execute('select * from mkt_his ')
#这里的数据是逆序取得,时间顺序从后向前（方便了很多）
allDaylineData = cur.fetchall()

x = []
y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []

for daylineData in allDaylineData:
    
    #第一列是时间，作为x轴
    x.append(daylineData[0])
    
    #下面分别是ma5,ma10,ma20
    y1.append(daylineData[10])
    y2.append(daylineData[11])
    y3.append(daylineData[12])

    #下面分别是volume,v_ma5,v_ma10,v_ma20
    y4.append(daylineData[7])
    y5.append(daylineData[13])
    y6.append(daylineData[14])
    y7.append(daylineData[15])
    
    #只取一年的数据（还是取所有的数据？由于现在图是可以调整的）
    if (len(x) >= 365):
        break
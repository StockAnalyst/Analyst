#-*- coding:UTF-8 -*-
#!/usr/bin/env python
#Filename:SimpleStockDayline_1.0.py


import numpy as np
from matplotlib import pylab as pl
import matplotlib as mpl
import MySQLdb



#设置中文字体
mpl.rcParams['font.sans-serif'] = ['SimHei']


#之前在建立数据库的时候，将date字段的类型设置成 DATE
conn = MySQLdb.connect("127.0.0.1","root","root","db_mkt" )
#建立游标
cur = conn.cursor()


def drawhist(code):
        
    
    #我的数据库结构是data数据库下面有一个his_data的表，存着一只股票的所有历史数据
    
    cur.execute("""select date,ma5,ma10,ma20,volume,v_ma5,v_ma10,v_ma20
            from tb_his where code=%s
            """,(code))


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
        y1.append(daylineData[1])
        y2.append(daylineData[2])
        y3.append(daylineData[3])

        #下面分别是volume,v_ma5,v_ma10,v_ma20
        y4.append(daylineData[4])
        y5.append(daylineData[5])
        y6.append(daylineData[6])
        y7.append(daylineData[7])
        
        #只取一年的数据
        if (len(x) >= 365):
            break

    #extent = (0,1,0,1)
    #x = np.linspace(0,1,12)

    #从这里正式开始画图，这里作为（面向对象的思想）
    f1 = pl.figure(num = 1,figsize=(16,12))

    #这个是用来设置facecolor的
    #rect = f1.patch
    #rect.set_facecolor("black")

    pl.subplot(311,axisbg='w')
    pl.plot(x,y1,'r',label='ma5')
    pl.plot(x,y2,'g',label='ma10')
    pl.plot(x,y3,'b',label='ma20')

    pl.title(u"单股票日线图")
    pl.ylabel(u"MA值")
    pl.legend(loc = 'upper left')

    pl.subplot(312,axisbg='w')


    pl.bar(x,y4,color = 'k')
    pl.plot(x,y5,label='v_ma5')
    pl.plot(x,y6,label='v_ma10')
    pl.plot(x,y7,label='v_ma20')

    pl.title(u"单股票日Volume图")
    pl.ylabel(u"Volume值")
    pl.legend(loc = 'upper left')



    pl.subplot(313,axisbg='w')
    ''''这些是统计参数？等数据处理后，再画图'''

    pl.show()

    
#drawhist('000001')
#!/usr/bin/env python
#-*- coding:gbk -*-
#FILE:当前版本实际用的各种示例数据(连接db,公式管理器界面all,公式编辑器界面all,插入函数界面all)

import wx
import MySQLdb

#插入函数界面函数信息
db1 = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="db_mkt",charset="utf8")
cursor1 = db1.cursor()
attrList = ['HQHS','YYHS','LLHS','XTHS','SXHS']
functionList = [[] for i in range(5) ]
cursor1.execute("""SELECT * FROM tb_function WHERE 1""")
functionAll = cursor1.fetchall()
for i in range(5):
    cursor1.execute("""SELECT * FROM tb_function WHERE attr=%s""",attrList[i])
    functionList[i] = cursor1.fetchall()
#断开连接
cursor1.close()
db1.close()

db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="db_mkt",charset="utf8")
cursor = db.cursor()

#some example datas for grid in 模式管理器
column1 = [u'MACD基本',u'DDE决策',u'SUP决策',u'资金决策']
column2 = [u'周期：未绑定 主：MA 副：VOL-TDX,MACD...',
           u'周期：未绑定 主：MA 副：VOL-TDX,DDX,DDY,DDZ...',
           u'周期：未绑定 主：MA 副：VOL-TDX,SUPL,SUPV...',
           u'周期：未绑定 主：MA 副：VOL-TDX,ZJLX,ZJQDL...']

#some example datas in 公式编辑器
typeList=[u'大势型',u'超买超卖型',u'趋势型',u'能量型',u'成交量型',u'均线型',u'图表型',u'路径型',
          u'停损型',u'策略型',u'神系',u'龙系',u'鬼系',u'其他系',u'特色型',u'其他类型']#技术指标的type类型

typeList1=[u'指标条件选股',u'基本面选股',u'即时盘中选股',u'走势特征选股',u'形态特征选股',u'其他类型']#条件选股的type类型

methodList=[u'副图',u'主图叠加',u'副图（叠加K线）',u'副图（叠加美国线）',u'副图（叠加收盘站线）',u'主图替换']#技术指标的画图方法

outputList=[u'动态翻译',u'测试结果']#输出选项(,u'参数精灵',u'用法注释')

sidafenlei = [u"技术指标公式",u"条件选股公式",u"专家系统公式",u"五彩K线公式"]#所有公式的四大分类

tb_name = ['tb_jszb','tb_tjxg','tb_zjxt','tb_wckx']#所有公式在db中的四个表名

leaveListFinal = [[] for i in range(4)]#[[],[],[],[]]分类存储所有的叶子节点（所有公式）
for i in range(4):
    cursor.execute("""SELECT name FROM """ + tb_name[i] + """ WHERE 1""")
    leaveList = cursor.fetchall()
    for leaveone in leaveList:
        leaveListFinal[i].append(leaveone[0])

#some example datas for treectrl
list1 = [[] for i in range(0,16)]#[[],[],[],[],[]...]分类存储 技术指标的所有节点
for name in typeList:
    index = 0
    for i in range(0,16):
        if name == typeList[i]:
            index = i
            break
    cursor.execute("""SELECT name FROM tb_jszb WHERE type=%s""",name)
    item = cursor.fetchall()
    for item1 in item:
        #通过转码来解决编码的错误问题
        list1[index].append(item1[0].encode('gbk'))
        
list2 = [[] for i in range(0,6)]#[[],[],[],[],[],[]]分类存储 条件选股的所有节点
for name in typeList1:
    index = 0
    for i in range(0,6):
        if name == typeList1[i]:
            index = i
            break
    cursor.execute("""SELECT name FROM tb_tjxg WHERE type=%s""",name)
    item = cursor.fetchall()
    for item1 in item:
        list2[index].append(item1[0].encode('gbk'))

list3 = []#[]无分类存储 专家系统的所有节点
cursor.execute("""SELECT name FROM tb_zjxt WHERE 1 """)
item = cursor.fetchall()
for item1 in item:
    list3.append(item1[0].encode('gbk'))

list4 = []#[]无分类存储 五彩K线的所有节点
cursor.execute("""SELECT name FROM tb_wckx WHERE 1 """)
item = cursor.fetchall()
for item1 in item:
    list4.append(item1[0].encode('gbk'))

#treectrl控件的数据源
tree = [["技术指标公式",
            [['大势型',
                            list1[0]],
            ['超买超卖型',
                            list1[1]],
            ['趋势型',
                            list1[2]],
            ['能量型',
                            list1[3]],
            ['成交量型',
                            list1[4]],
            ['均线型',
                            list1[5]],
            ['图表型',
                            list1[6]],
            ['路径型',
                            list1[7]],
            '停损型',
            ['策略型',
                            list1[9]],
            ['神系',
                            list1[10]],
            ['龙系',
                            list1[11]],
            ['鬼系',
                            list1[12]],
            ['其他系',
                            list1[13]],
            ['特色型',
                            list1[14]],
            '其他类型']],
        ["条件选股公式",
            [['指标条件选股',
                            list2[0]],
             ['基本面选股',
                            list2[1]],
             ['即时盘中选股',
                            list2[2]],
             ['走势特征选股',
                            list2[3]],
             ['形态特征选股',
                            list2[4]],
             '其他类型']],
         ["专家系统公式",
             list3],
         ["五彩K线公式",
             list4]
     ]

#公式编辑器界面的参数信息（all）
canshu_func = [['M' , '2.00' , '100.00' , '5.00'],['M' , '2.00' , '60.00'  , '7.00'],['N' , '2.00' , '100.00' , '10.00'],['M' , '2.00' , '60.00', '6.00'],
                 ['P1' ,'0.00' , '100.00' , '20.00'],['P1' ,'0.00' , '100.00' , '90.00'],['N' , '2.00' , '250.00' , '12.00'],['LL' ,'0.00' , '40.00'  , '6.00' ],
                 ['LH' , '0.00' , '40.00'  , '6.00' ],['N' , '1.00' , '100.00' , '10.00']]

#断开连接
#cursor.close()
#db.close()

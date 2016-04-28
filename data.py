#!/usr/bin/env python
#-*- coding:gbk -*-
#FILE:当前版本实际用的各种示例数据

import wx
import MySQLdb

db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="db_mkt",charset="utf8")
cursor = db.cursor()

#some example datas for treectrl
cursor.execute("""SELECT name FROM tb_jszb WHERE type=%s""",u"大势型")
item = cursor.fetchall()
list1 = []
for item1 in item:
    #通过转码来解决编码的错误问题
    list1.append(item1[0].encode('gbk'))

tree = [["技术指标公式",
              [['大势型',
                             list1],
               ['超买超买型',
                             ['CCI']],
               ['趋势型',
                             ['CHO']],
               ['能量型',
                             ['BRAR']],
               ['成交量型',
                             ['AMO']],
               ['均线型',
                             ['MA']],
               ['图表型',
                             ['ZX']],
               ['路径型',
                             ['BOLL']],
               '停损型',
               ['策略型',
                             ['MAcl']],
               ['神系',
                             ['SG-XDT']],
               ['龙系',
                             ['RAD']],
               ['鬼系',
                             ['CYC']],
               ['其他系',
                             ['XT']],
               ['特色型',
                             ['CPBS']],
               '其他类型']],
	 ["条件选股公式",
               [['指标条件选股',
                             ['ASRD']],
                ['基本面选股',
                             ['A001']],
                ['即时盘中选股',
                             ['B003']],
                ['走势形式选股',
                             ['UPN']],
                ['形态特征选股',
                            ['MSTAR']],
                '其他类型']],
         ["专家系统公式",
                ['BIAS']],
         ["五彩K线公式",
                ['KSTAR1','KSTAR2']]
      ]
'''

tree = [
	 [u"条件选股公式",
               [[u'指标条件选股',
                             ['ASRD']],
                [u'基本面选股',
                             ['A001']],
                [u'即时盘中选股',
                             ['B003']],
                [u'走势形式选股',
                             ['UPN']],
                [u'形态特征选股',
                            ['MSTAR']],
                u'其他类型']],
         [u"专家系统公式",
                ['BIAS']],
         [u"五彩K线公式",
                ['KSTAR1','KSTAR2']]
      ]
'''
#some example datas for grid in 模式管理器
column1 = [u'MACD基本',u'DDE决策',u'SUP决策',u'资金决策']
column2 = [u'周期：未绑定 主：MA 副：VOL-TDX,MACD...',
           u'周期：未绑定 主：MA 副：VOL-TDX,DDX,DDY,DDZ...',
           u'周期：未绑定 主：MA 副：VOL-TDX,SUPL,SUPV...',
           u'周期：未绑定 主：MA 副：VOL-TDX,ZJLX,ZJQDL...']

#some example datas in 公式编辑器
typeList=[u'大势型',u'超买超买型',u'趋势型',u'能量型',u'成交量型',u'均线型',u'图表型',u'路径型',
          u'停损型',u'策略型',u'神系',u'龙系',u'鬼系',u'其他系',u'特色型',u'其他类型']

methodList=[u'副图',u'主图叠加',u'副图（叠加K线）',u'副图（叠加美国线）',u'副图（叠加收盘站线）',u'主图替换']

typeList1=[u'指标条件选股',u'基本面选股',u'即时盘中选股',u'走势形式选股',u'形态特征选股',u'其他类型']

outputList=[u'动态翻译',u'测试结果',u'参数精灵',u'用法注释']

leaveListFinal = [[] for i in range(4)]
tb_name = ['tb_jszb','tb_tjxg','tb_zjxt','tb_wckx']
for i in range(4):
    cursor.execute("""SELECT name FROM """ + tb_name[i] + """ WHERE 1""")
    leaveList = cursor.fetchall()
    for leaveone in leaveList:
        leaveListFinal[i].append(leaveone[0])
    #print leaveListFinal[i]

sidafenlei = [u"技术指标公式",u"条件选股公式",u"专家系统公式",u"五彩K线公式"]

#断开连接
#cursor.close()
#db.close()

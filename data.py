#!/usr/bin/env python
#-*- coding:gbk -*-
#FILE:��ǰ�汾ʵ���õĸ���ʾ������

import wx
import MySQLdb

db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="db_mkt",charset="utf8")
cursor = db.cursor()

#some example datas for treectrl
cursor.execute("""SELECT name FROM tb_jszb WHERE type=%s""",u"������")
item = cursor.fetchall()
list1 = []
for item1 in item:
    #ͨ��ת�����������Ĵ�������
    list1.append(item1[0].encode('gbk'))

tree = [["����ָ�깫ʽ",
              [['������',
                             list1],
               ['��������',
                             ['CCI']],
               ['������',
                             ['CHO']],
               ['������',
                             ['BRAR']],
               ['�ɽ�����',
                             ['AMO']],
               ['������',
                             ['MA']],
               ['ͼ����',
                             ['ZX']],
               ['·����',
                             ['BOLL']],
               'ͣ����',
               ['������',
                             ['MAcl']],
               ['��ϵ',
                             ['SG-XDT']],
               ['��ϵ',
                             ['RAD']],
               ['��ϵ',
                             ['CYC']],
               ['����ϵ',
                             ['XT']],
               ['��ɫ��',
                             ['CPBS']],
               '��������']],
	 ["����ѡ�ɹ�ʽ",
               [['ָ������ѡ��',
                             ['ASRD']],
                ['������ѡ��',
                             ['A001']],
                ['��ʱ����ѡ��',
                             ['B003']],
                ['������ʽѡ��',
                             ['UPN']],
                ['��̬����ѡ��',
                            ['MSTAR']],
                '��������']],
         ["ר��ϵͳ��ʽ",
                ['BIAS']],
         ["���K�߹�ʽ",
                ['KSTAR1','KSTAR2']]
      ]
'''

tree = [
	 [u"����ѡ�ɹ�ʽ",
               [[u'ָ������ѡ��',
                             ['ASRD']],
                [u'������ѡ��',
                             ['A001']],
                [u'��ʱ����ѡ��',
                             ['B003']],
                [u'������ʽѡ��',
                             ['UPN']],
                [u'��̬����ѡ��',
                            ['MSTAR']],
                u'��������']],
         [u"ר��ϵͳ��ʽ",
                ['BIAS']],
         [u"���K�߹�ʽ",
                ['KSTAR1','KSTAR2']]
      ]
'''
#some example datas for grid in ģʽ������
column1 = [u'MACD����',u'DDE����',u'SUP����',u'�ʽ����']
column2 = [u'���ڣ�δ�� ����MA ����VOL-TDX,MACD...',
           u'���ڣ�δ�� ����MA ����VOL-TDX,DDX,DDY,DDZ...',
           u'���ڣ�δ�� ����MA ����VOL-TDX,SUPL,SUPV...',
           u'���ڣ�δ�� ����MA ����VOL-TDX,ZJLX,ZJQDL...']

#some example datas in ��ʽ�༭��
typeList=[u'������',u'��������',u'������',u'������',u'�ɽ�����',u'������',u'ͼ����',u'·����',
          u'ͣ����',u'������',u'��ϵ',u'��ϵ',u'��ϵ',u'����ϵ',u'��ɫ��',u'��������']

methodList=[u'��ͼ',u'��ͼ����',u'��ͼ������K�ߣ�',u'��ͼ�����������ߣ�',u'��ͼ����������վ�ߣ�',u'��ͼ�滻']

typeList1=[u'ָ������ѡ��',u'������ѡ��',u'��ʱ����ѡ��',u'������ʽѡ��',u'��̬����ѡ��',u'��������']

outputList=[u'��̬����',u'���Խ��',u'��������',u'�÷�ע��']

leaveListFinal = [[] for i in range(4)]
tb_name = ['tb_jszb','tb_tjxg','tb_zjxt','tb_wckx']
for i in range(4):
    cursor.execute("""SELECT name FROM """ + tb_name[i] + """ WHERE 1""")
    leaveList = cursor.fetchall()
    for leaveone in leaveList:
        leaveListFinal[i].append(leaveone[0])
    #print leaveListFinal[i]

sidafenlei = [u"����ָ�깫ʽ",u"����ѡ�ɹ�ʽ",u"ר��ϵͳ��ʽ",u"���K�߹�ʽ"]

#�Ͽ�����
#cursor.close()
#db.close()

#!/usr/bin/env python
#-*- coding:gbk -*-
#FILE:��ǰ�汾ʵ���õĸ���ʾ������(����db,��ʽ����������all,��ʽ�༭������all,���뺯������all)

import wx
import MySQLdb

#���뺯�����溯����Ϣ
db1 = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="db_mkt",charset="utf8")
cursor1 = db1.cursor()
attrList = ['HQHS','YYHS','LLHS','XTHS','SXHS']
functionList = [[] for i in range(5) ]
cursor1.execute("""SELECT * FROM tb_function WHERE 1""")
functionAll = cursor1.fetchall()
for i in range(5):
    cursor1.execute("""SELECT * FROM tb_function WHERE attr=%s""",attrList[i])
    functionList[i] = cursor1.fetchall()
#�Ͽ�����
cursor1.close()
db1.close()

db = MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="db_mkt",charset="utf8")
cursor = db.cursor()

#some example datas for grid in ģʽ������
column1 = [u'MACD����',u'DDE����',u'SUP����',u'�ʽ����']
column2 = [u'���ڣ�δ�� ����MA ����VOL-TDX,MACD...',
           u'���ڣ�δ�� ����MA ����VOL-TDX,DDX,DDY,DDZ...',
           u'���ڣ�δ�� ����MA ����VOL-TDX,SUPL,SUPV...',
           u'���ڣ�δ�� ����MA ����VOL-TDX,ZJLX,ZJQDL...']

#some example datas in ��ʽ�༭��
typeList=[u'������',u'��������',u'������',u'������',u'�ɽ�����',u'������',u'ͼ����',u'·����',
          u'ͣ����',u'������',u'��ϵ',u'��ϵ',u'��ϵ',u'����ϵ',u'��ɫ��',u'��������']#����ָ���type����

typeList1=[u'ָ������ѡ��',u'������ѡ��',u'��ʱ����ѡ��',u'��������ѡ��',u'��̬����ѡ��',u'��������']#����ѡ�ɵ�type����

methodList=[u'��ͼ',u'��ͼ����',u'��ͼ������K�ߣ�',u'��ͼ�����������ߣ�',u'��ͼ����������վ�ߣ�',u'��ͼ�滻']#����ָ��Ļ�ͼ����

outputList=[u'��̬����',u'���Խ��']#���ѡ��(,u'��������',u'�÷�ע��')

sidafenlei = [u"����ָ�깫ʽ",u"����ѡ�ɹ�ʽ",u"ר��ϵͳ��ʽ",u"���K�߹�ʽ"]#���й�ʽ���Ĵ����

tb_name = ['tb_jszb','tb_tjxg','tb_zjxt','tb_wckx']#���й�ʽ��db�е��ĸ�����

leaveListFinal = [[] for i in range(4)]#[[],[],[],[]]����洢���е�Ҷ�ӽڵ㣨���й�ʽ��
for i in range(4):
    cursor.execute("""SELECT name FROM """ + tb_name[i] + """ WHERE 1""")
    leaveList = cursor.fetchall()
    for leaveone in leaveList:
        leaveListFinal[i].append(leaveone[0])

#some example datas for treectrl
list1 = [[] for i in range(0,16)]#[[],[],[],[],[]...]����洢 ����ָ������нڵ�
for name in typeList:
    index = 0
    for i in range(0,16):
        if name == typeList[i]:
            index = i
            break
    cursor.execute("""SELECT name FROM tb_jszb WHERE type=%s""",name)
    item = cursor.fetchall()
    for item1 in item:
        #ͨ��ת�����������Ĵ�������
        list1[index].append(item1[0].encode('gbk'))
        
list2 = [[] for i in range(0,6)]#[[],[],[],[],[],[]]����洢 ����ѡ�ɵ����нڵ�
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

list3 = []#[]�޷���洢 ר��ϵͳ�����нڵ�
cursor.execute("""SELECT name FROM tb_zjxt WHERE 1 """)
item = cursor.fetchall()
for item1 in item:
    list3.append(item1[0].encode('gbk'))

list4 = []#[]�޷���洢 ���K�ߵ����нڵ�
cursor.execute("""SELECT name FROM tb_wckx WHERE 1 """)
item = cursor.fetchall()
for item1 in item:
    list4.append(item1[0].encode('gbk'))

#treectrl�ؼ�������Դ
tree = [["����ָ�깫ʽ",
            [['������',
                            list1[0]],
            ['��������',
                            list1[1]],
            ['������',
                            list1[2]],
            ['������',
                            list1[3]],
            ['�ɽ�����',
                            list1[4]],
            ['������',
                            list1[5]],
            ['ͼ����',
                            list1[6]],
            ['·����',
                            list1[7]],
            'ͣ����',
            ['������',
                            list1[9]],
            ['��ϵ',
                            list1[10]],
            ['��ϵ',
                            list1[11]],
            ['��ϵ',
                            list1[12]],
            ['����ϵ',
                            list1[13]],
            ['��ɫ��',
                            list1[14]],
            '��������']],
        ["����ѡ�ɹ�ʽ",
            [['ָ������ѡ��',
                            list2[0]],
             ['������ѡ��',
                            list2[1]],
             ['��ʱ����ѡ��',
                            list2[2]],
             ['��������ѡ��',
                            list2[3]],
             ['��̬����ѡ��',
                            list2[4]],
             '��������']],
         ["ר��ϵͳ��ʽ",
             list3],
         ["���K�߹�ʽ",
             list4]
     ]

#��ʽ�༭������Ĳ�����Ϣ��all��
canshu_func = [['M' , '2.00' , '100.00' , '5.00'],['M' , '2.00' , '60.00'  , '7.00'],['N' , '2.00' , '100.00' , '10.00'],['M' , '2.00' , '60.00', '6.00'],
                 ['P1' ,'0.00' , '100.00' , '20.00'],['P1' ,'0.00' , '100.00' , '90.00'],['N' , '2.00' , '250.00' , '12.00'],['LL' ,'0.00' , '40.00'  , '6.00' ],
                 ['LH' , '0.00' , '40.00'  , '6.00' ],['N' , '1.00' , '100.00' , '10.00']]

#�Ͽ�����
#cursor.close()
#db.close()

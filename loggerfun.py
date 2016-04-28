#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#FILE:日志中logger（当前版本，结合logging.config只利用了root）

import logging
import logging.config

#日志相关father层次
logging.config.fileConfig("logging.conf")
logger = logging.getLogger('root')

'''
这是最基本的logger，不涉及多个logger相互调用：
但是如果需要嵌套且不出现double/层次关系，满足下列两条件：
1）不要将子logger写在logging.conf中
2）直接新建一个logger（和root写在同一个文件中）
'''

def fun0_s():
    logger.info(u'开启')

def fun0_f():
    logger.info(u'关闭\n')

def fun1():
    logger.info(u'新增了自定义技术指标')

def fun2():
    logger.info(u'新增了自定义模板')

def fun3():
    logger.info(u'更新了F10数据')

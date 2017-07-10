#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/7    17:45
#__author__='Administrator'
import os ,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量

BAES='test_student_mag'#库名
HOSTS="mysql+pymysql://root:root@127.0.0.1:3306/"+BAES+"?charset=utf8"#连接
USER='admin'
PWD='admin'

ADMIN_OPEN=[
    ('创建讲师','add_teach'),
    ('查看讲师','teach_l'),
    ('创建班级','add_class'),
    ('查看班级','class_l'),
    ('讲师关联班级','assoc'),
    ('创建学员','add_stu'),
    ('查看学员','stu_l'),
    ('班级关联学员','class_student'),
    ('退出','tech_exit'),
]

TEACH_OPEN=[
    ('查看班级','show_class'),
    ( '创建新班级','add_class'),
    ('班级增加学员','add_student'),
     ('增加新课节','add_lesson'),
      ('开始上课','add_cla_day'),
       ('批改成绩','set_results'),
    ('退出','tech_exit')
]
STUED_OPEN=[
    ('提交作业','up_work'),
    ( '查看成绩','set_resu'),
    ('查看班级排行','cla_top'),
    ('退出','tech_exit')
]
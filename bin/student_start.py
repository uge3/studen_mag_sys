#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/9    22:46
#__author__='Administrator'
import os ,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from core.student_class import Stu_Mag
from cfg import config
if __name__ == '__main__':
    while True:
        stu=Stu_Mag()
        stu.user_log()
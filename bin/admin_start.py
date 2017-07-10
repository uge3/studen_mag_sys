#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/7    17:45
#__author__='Administrator'

import os ,sys
from sqlalchemy import create_engine
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from core import admin_class
from core import admin_log
from cfg import config
if __name__ == '__main__':
    #                      用户 密码  主机             库
    #engine = create_engine(config.HOSTS,)#连接
    #admin_class.Base.metadata.create_all(admin_class.engine)#创建表结构
    while True:
        admin=admin_log.Admin_Mag()
        admin.user_log()


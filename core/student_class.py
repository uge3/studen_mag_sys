#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/8    12:29
#__author__='Administrator'
import os ,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy import func #统计
from  core import admin_class
from  cfg import config
#学员类
class Stu_Mag(object):

    def __init__(self):
        self.Session_class=sessionmaker(bind=admin_class.engine)#创建与数据库的会话 类
        self.Session=self.Session_class()#生成实例
        self.stu_name=''#学员姓名

    #开始相关操作
    def openatin(self):#开始相关操作
        while True:
            print('\033[32;1m学员界面\033[0m'.center(60,'='))
            print(('\033[36;1m[%s]\033[0m'%self.stu_name).center(60,'='))

            for index,i in enumerate(config.STUED_OPEN):
                print(index,':',i[0])
            id=input('请选择>>:')
            if id.isdigit():
                if int(id)>=len(config.STUED_OPEN):continue
                s=config.STUED_OPEN[int(id)][1]
            else:
                continue
            if hasattr(self,s):#是反射否存在
                func=getattr(self,s)#调用
                func()#执行

    #提交作业
    def up_work(self):
        class_id=self.class_l()
        if not class_id:
            return None#班级ID
        les_id=self.lessn_obj(class_id)#课节表ID\
        if not les_id:return None
        cl_dayid=self.class_less(class_id,les_id)#课程表ID
        if cl_dayid:
            stu_id=self.stu_obj.id#学员ID
            stu_work=self.Session.query(admin_class.Student_work).filter_by(students_id=stu_id,class_id=cl_dayid.id).first()
            if stu_work:
                if stu_work.status=='yes':
                    print('\033[31;1m作业已经提交,不能重复提交!\033[0m')
                    return None
                #对应的课程表
                les_n=self.Session.query(admin_class.Class_Day).filter_by(class_id=class_id,lesson_id=les_id).first()
                print('姓名:',self.stu_name,'班级:',les_n.class_n,'课节:',les_n.lesson_n,'作业提交状态:',stu_work.status,'成绩:',stu_work.results)
                chend=input('提交作业>>>: Y/y 确认!').upper().strip()
                if chend=='Y':
                    self.Session.query(admin_class.Student_work).filter_by(students_id=stu_id,class_id=cl_dayid.id).update({"status":"yes"})
                    print('提交完成!')
                    self.Session.commit()
                    return
                else:
                    return None
            else:
                print('\033[31;1m您可能没有上本节课!无法提交\033[0m')
                return None
        else:
            print('\033[31;1m本节课可能没有开始!\033[0m')
            return None


    #获取课程ID
    def class_less(self,cla_id,les_id):
        cl_dayid=self.Session.query(admin_class.Class_Day).filter(admin_class.Class_Day.class_id==cla_id).\
            filter(admin_class.Class_Day.lesson_id==les_id).first()#获取班级课程表id
        if cl_dayid:
            return cl_dayid
        else:
            return None

    #获取课程表 选课节
    def lessn_obj(self,cla):
        les_l=self.Session.query(admin_class.Class_Day).filter_by(class_id=cla).all()
        for i in les_l:
            print('编号:',i.lesson_id,'课节:',i.lesson_n)
        les_id=input('请按编号选择课节 >>:').strip()
        if les_id.isdigit():
            for i in les_l:
                if int(les_id)==i.lesson_id:
                    return int(les_id)#返回课节ID
            else:
                print('选择课节有误!')
                return None
        else:
            print('选择课节有误!')
            return None

    #查看班级选择
    def class_l(self):#查看班级
        for i in self.stu_obj.class_name:
            print('编号',i.id,'>>:',i.name)
        class_id=input('请按编号选择班级>>:').strip()
        if  class_id.isdigit() :#判断是否是整数
            for i in self.stu_obj.class_name:#是否在学员的班级中
                if int(class_id)==i.id:
                    return int(class_id)#返回班级ID
            else:
                print('选择班级有误!')
                return None
        else:
            print('选择班级有误!')
            return None

    #查看课节
    def lesson_l(self):
        for i in self.les:
            print('编号',i.id,'>>:',i)
        les_id=input('请按编号选择课节 >>:').strip()
        if les_id.isdigit():
            for i in self.les:
                if int(les_id)==i.id:
                    return int(les_id)#返回课节ID
            else:
                pass
        else:
            print('选择课节有误!')
            return None

    #查看成绩
    def set_resu(self):
        class_id=self.class_l()#班级ID
        les_l=self.Session.query(admin_class.Class_Day).filter_by(class_id=class_id).all()#本班所有课节
        stu_id=self.stu_obj.id#学员ID
        for i in les_l:
            stu_work=self.Session.query(admin_class.Student_work).filter_by(students_id=stu_id,class_id=i.id).first()#取对应的课节
            if stu_work:
                cla_day=self.Session.query(admin_class.Class_Day).filter_by(id=stu_work.class_id).first()#课程表对象
                if cla_day:
                    print('姓名:',self.stu_name,'班级：',cla_day.class_n,'课节:',cla_day.lesson_n,' 作业提交状态:',stu_work.status,'成绩:',stu_work.results)
                else:
                    pass
            else:
                pass

    #查看排名
    def cla_top(self):
        class_id=self.class_l()#班级ID
        les_l=self.Session.query(admin_class.Class_Day).filter_by(class_id=class_id).all()#取当前班级的所有课节
        stu_id_l=self.Session.query(admin_class.Student).all()#取学生id
        top_list=[]#分数
        for i in stu_id_l:
            resut=0
            for j in les_l:
                stu_work=self.Session.query(admin_class.Student_work).filter_by(students_id=i.id,class_id=j.id).first()
                if not stu_work:continue
                if stu_work.results:
                    resut+=int(stu_work.results)
            else:
                top_list.append((resut,i.name))
        print(top_list)
        self.sort(top_list)
        for index,i in enumerate(top_list):
            print('名次',index+1,'总分数--姓名:',i)

    #排序
    def sort(self,ls):
        for i in range(len(ls)-1):
            for j in range(len(ls)-i-1):
                if ls[j]<ls[j+1]:
                    ls[j],ls[j+1] =ls[j+1],ls[j]
        return ls



    #退出
    def tech_exit(self):
        return  exit()

    #登陆
    def user_log(self):#登陆
            user_n=input('请输入用户名(qq)>>:').strip()
            if not user_n.isdigit():return None
            aut_obj=self.Session.query(admin_class.Student).filter(admin_class.Student.qq==int(user_n)).first()
            if aut_obj:
                #print(self.aut_obj_1.pwd)#用户对应密码
                pwds=input('请输入密码>>:').strip()
                if pwds == aut_obj.pwd:
                    self.stu_name=aut_obj.name
                    self.qq=aut_obj.qq
                    self.stu_obj = self.Session.query(admin_class.Student).filter(admin_class.Student.qq==self.qq).first()#取当前学员对象实例
                    self.openatin()
                else:
                    print('密码有误')
                    return
            else:
                print('输入的用户名不存')
                return



    #stu.up_work()
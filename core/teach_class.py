#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/7    17:48
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

#讲师类
class Teach_Mag(object):

    def __init__(self):
        self.Session_class=sessionmaker(bind=admin_class.engine)#创建与数据库的会话 类
        self.Session=self.Session_class()#生成实例
        self.teach_name=''

    #开始相关操作
    def openatin(self):#开始相关操作
        while True:
            print('\033[35;1m讲师界面\033[0m'.center(60,'='))
            for index,i in enumerate(config.TEACH_OPEN):
                print(index,':',i[0])
            id=input('请选择>>:')
            if id.isdigit():
                if int(id)>=len(config.TEACH_OPEN):continue
                s=config.TEACH_OPEN[int(id)][1]
            else:
                continue
            if hasattr(self,s):#是反射否存在
                func=getattr(self,s)#调用
                func()#执行

    #查看班级
    def show_class(self):#查看班级
        print('\033[32;1m查看班级(可管理)\033[0m'.center(60,'='))
        #show_class=self.Session.query(admin_class.Class_name).filter(admin_class.Class_name.teach_name==self.teach_name)
        print('\033[31;1m全部班级\033[0m'.center(45,'-'))#所有班级
        for i in self.class_list:
            print(i)
        print('\033[35;1m可管理班级\033[0m'.center(45,'-'))
        cla_id=self.class_l()#调用查看班级
        class_obj=self.Session.query(admin_class.Class_name).filter(admin_class.Class_name.id==cla_id).first()
        if class_obj:#获取班级对象成功 有内容
            print(class_obj,class_obj.name,class_obj.id)
            self.student_l(class_obj.name)#调用查看学员 得到班级对象
            # print('[%s] 班 学员列表'.center(60,'=')%c)
            # for i in c.students:
            #     print(i.id,'姓名:',i.name,'QQ:',i.qq)
            # print('end'.center(60,'='))
            return
        else:
            print('选择有误!')
            return

    #查看班级选择
    def class_l(self):#查看班级
        for i in self.teach_obj.class_n:
            print('编号',i.id,'班级:',i.name)
        class_id=input('请按编号选择班级>>:').strip()
        if  class_id.isdigit() :#判断是否是整数
            for i in self.teach_obj.class_n:#是否在讲师的班级中
                if int(class_id)==i.id:
                    return int(class_id)#返回班级ID
            else:
                print('选择班级有误!')
                return None
        else:
            print('选择班级有误!')
            return None

    #查看班级学员
    def student_l(self,class_name):#查看班级学员
        stu_l=self.Session.query(admin_class.Class_name).filter(admin_class.Class_name.name==str(class_name)).first()#所选班级对象
        print('[%s] 班 学员列表'.center(60,'=')%stu_l)
        for i in stu_l.students:
            print(i.id,'姓名:',i.name,'QQ:',i.qq)
        print('end'.center(60,'='))
        return stu_l#返回所选班级对象

    #查看课节
    def less_cher(self):
        les=self.Session.query(admin_class.Lesson).all()#取课节名列表
        for i in les:
            print('编号',i.id,'课节名>>:',i)
        return les
    #查看课节 选择
    def lesson_l(self):
        les=self.less_cher()#取课节名列表
        # for i in les:
        #     print('编号',i.id,'课节名>>:',i)
        les_id=input('请按编号选择课节 >>:').strip()
        if les_id.isdigit():
            for i in les:
                if int(les_id)==i.id:
                    return int(les_id)#返回课节ID
            else:
                print('选择课节有误!')
                return None
        else:
            print('选择课节有误!')
            return None

    #创建班级
    def add_class(self):#创建班级
        print('\033[35;1m创建班级界面\033[0m'.center(60,'='))
        attr=input("输入班级名>>:").strip()
        if attr in self.class_list:#如果存在
            return print('班级名重复!')
        c=admin_class.Class_name(name=attr)#创建新班级
        self.teach_obj.class_n.append(c)#关联讲师与班级
        if self.add_all(c):#进行调用添加
            self.Session.add_all([c])
            self.Session.commit()
        return

    #班级增加学员
    def add_student(self):#班级增加学员
        print('\033[35;1m增加学员界面\033[0m'.center(60,'='))
        cla_id=self.class_l()#调用查看班级
        if not cla_id:return None
        #获取班级对象
        c=self.Session.query(admin_class.Class_name).filter(admin_class.Class_name.id==cla_id).first()
        if not c:return None
        stu_l=self.student_l(c.name)#查看班级学员
        student_qq=input('请输入学生QQ号码>>:').strip()
        s_qq=self.Session.query(admin_class.Student).filter(admin_class.Student.qq==int(student_qq)).first()#学员qq对象
        if s_qq:#如果有这个qq
            c.students.append(s_qq)#加入班级
            self.Session.commit()
            print('加入班级成功！')
        else:
            return print('QQ对应的学员不存在')

    #添加课节
    def add_lesson(self):#添加课节
        print('现有课节'.center(40,'='))
        les=self.less_cher()#取课节名列表
        day_name=input('输入课节名>>:').strip()
        d1=admin_class.Lesson(name=day_name)
        self.add_all(d1)

    #获取课程ID
    def class_less(self,cla_id,les_id):

        cl_dayid=self.Session.query(admin_class.Class_Day).filter(admin_class.Class_Day.class_id==cla_id).\
            filter(admin_class.Class_Day.lesson_id==les_id).first()#获取班级课程表id
        if cl_dayid:
            return cl_dayid
        else:
            return None

    #获取班级对象
    def class_obj(self,cla_id):
        clas_obj=self.Session.query(admin_class.Class_name).filter(admin_class.Class_name.id==cla_id).first()#获取班级对象
        return clas_obj

    #开始上课
    def add_cla_day(self):#开始上课
        print('\033[32;1m班级上课\033[0m'.center(60,'='))
        cla_id=self.class_l()##获取班级id
        if not cla_id:return None
        les_id=self.lesson_l()#获取课节id
        if not les_id:return None
        clas_obj=self.class_obj(cla_id)#获取班级对象
        print(clas_obj,clas_obj.id)#班级名,ID
        cl_dayid=self.class_less(cla_id,les_id)#获取课程表对象
        if cl_dayid:#如果课程表存在
            print('当前班级该节课已经上过!')
            return
        clas_day=admin_class.Class_Day(class_id=cla_id,lesson_id=les_id)#创建上课课程记录
        self.Session.add(clas_day)#添加记录
        cl_day_id=self.class_less(cla_id,les_id)#获取当前班级课程对象
        c_obj=self.student_l(cl_day_id.class_n)#获取班级   学员对象
        for i in c_obj.students:
            stu_work=admin_class.Student_work(students_id=i.id,class_id=cl_day_id.id,status='not')#创建上课记录
            self.Session.add(stu_work)#添加记录
        self.Session.commit()
        return print('上课记录添加完成')

    #批改作业
    def set_results(self):#批改作业
        print('\033[32;1m批改作业\033[0m'.center(60,'='))
        cla_id=self.class_l()##获取班级id
        if not cla_id:return None
        les_id=self.lesson_l()#获取课节id
        if not les_id:return None
        cl_day_id=self.class_less(cla_id,les_id)#获取课程表对象
        if not cl_day_id:print('本节课未上!');return None
        #获取当前班级中，
        stude_day=self.Session.query(admin_class.Student_work).filter(admin_class.Student_work.class_id==cl_day_id.id).all()
        print('\033[36;1m开始批改作业\033[0m'.center(60,'='))
        print('\033[31;1m作业未提交则不显示\033[0m')
        for i in stude_day:
            if i.status=='yes' and not i.results:
                print(i.id,'姓名:',i.students_w.name,'成绩:',i.results)
                resu=input('请输入成绩>>:').strip()
                if resu.isdigit():
                    self.Session.query(admin_class.Student_work).filter(admin_class.Student_work.id==i.id).update({"results":resu})
            elif i.status=='yes' and i.results:
                print(i.id,'姓名:',i.students_w.name,'成绩:',i.results)
                resu=input('是否修改成绩? N/n 跳过,输入新成绩').upper().strip()
                if resu=='N':
                    continue
                if resu.isdigit():
                    self.Session.query(admin_class.Student_work).filter(admin_class.Student_work.id==i.id).update({"results":resu})

        else:
            self.Session.commit()
            print("已提交的作业全部批改完毕!")

    #增加函数
    def add_all(self,lists):#增加函数
        self.Session.add_all([lists])
        confirm=input('请进行确认: 按\033[31;1mN\033[0m回滚操作,其他键确认!' ).upper().strip()
        if confirm=="N":
            self.Session.rollback()#
            return False
        try:
            self.Session.commit()
            print('操作成功')
            return lists
        except Exception as e:
            self.Session.rollback()#
            print('操作失败!,可能该信息已经存在!')
            return

    #退出
    def tech_exit(self):
        return  exit()
    #登陆
    def user_log(self):#登陆
            user_n=input('请输入用户名>>:').strip()
            aut_obj=self.Session.query(admin_class.Teacher).filter(admin_class.Teacher.user==user_n).first()
            if aut_obj:
                #print(self.aut_obj_1.pwd)#用户对应密码
                pwds=input('请输入密码>>:').strip()
                if pwds == aut_obj.pwd:
                    self.teach_name=aut_obj.name
                    #print(self.teach_name)#当前讲师姓名
                    self.teach_obj = self.Session.query(admin_class.Teacher).filter(admin_class.Teacher.name==self.teach_name).first()#取当前讲课对象实例
                    self.class_list=self.Session.query(admin_class.Class_name).all()#获取班级名列表
                    #self.les=self.Session.query(admin_class.Lesson).all()#取课节名列表
                    #print(self.s_name_list[2])
                    self.openatin()
                else:
                    print('密码有误')
                    return
            else:
                print('输入的用户名不存')
                return

#Session.query()
while True:
    teach=Teach_Mag()
    #teach.add_teach()
    #teach.add_stu()

    teach.user_log()
#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/9    23:12
#__author__='Administrator'
import os ,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from sqlalchemy.orm import sessionmaker, relationship
from core import admin_class
from cfg import config
#管理登陆
class Admin_Mag(object):
    def __init__(self):
        self.Session_class=sessionmaker(bind=admin_class.engine)#创建与数据库的会话 类
        self.Session=self.Session_class()#生成实例
    #开始相关操作
    def openatin(self):#开始相关操作
        while True:
            print('\033[35;1m管理员界面\033[0m'.center(60,'='))
            for index,i in enumerate(config.ADMIN_OPEN):
                print(index,':',i[0])
            id=input('请选择>>:')
            if id.isdigit():
                if int(id)>=len(config.ADMIN_OPEN):continue
                s=config.ADMIN_OPEN[int(id)][1]
            else:
                continue
            if hasattr(self,s):#是反射否存在
                func=getattr(self,s)#调用
                func()#执行

    #关联讲师班级
    def assoc(self):
        t_id=self.tech_cher()
        cla_id=self.class_cher()
        #讲师表对象
        t=self.Session.query(admin_class.Teacher).filter(admin_class.Teacher.id==t_id).first()
        #获取班级对象
        c=self.Session.query(admin_class.Class_name).filter(admin_class.Class_name.id==cla_id).first()
        t.class_n.append(c)
        self.Session.commit()
        print('讲师:',t.name,'班级:',c.name)
        print('关联完成!')

    #讲师表对象
    def tech_cher(self):
        #t=self.Session.query(admin_class.Teacher).all()#讲师表对象
        t=self.teach_l()
        #for i in t :
            #print('编号',i.id,'>>:',i.name)
        t_id=input('请按编号选择讲师>>:').strip()
        if  t_id.isdigit() :#判断是否是整数
            for i in t:#
                if int(t_id)==i.id:
                    return int(t_id)#返回班级ID
            else:
                pass
        else:
            print('选择讲师有误!')
            return None
    #创建班级
    def add_class(self):
        print('\033[35;1m创建班级界面\033[0m'.center(60,'='))
        self.class_l()
        attr=input("输入班级名>>:").strip()
        self.class_list=self.Session.query(admin_class.Class_name).all()#获取班级名列表
        if attr in self.class_list:#如果存在
            return print('班级名重复!')
        c=admin_class.Class_name(name=attr)#创建新班级
        self.add_all(c)

    #查看讲师
    def teach_l(self):
        t=self.Session.query(admin_class.Teacher).all()
        for i in t:
            print('编号:',i.id,'讲师姓名:',i.name,'用户名:',i.user,'密码',i.pwd,' 管理班级:',i.class_n)
        return t


    #查看班级
    def class_l(self):
        c=self.Session.query(admin_class.Class_name).all()#班级对象
        print("全部班级信息".center(50,'-'))
        for i in c:
            print('编号',i.id,'>>:',i.name)
        return c

    #查看班级选择
    def class_cher(self):#查看班级
        c=self.class_l()
        class_id=input('请按编号选择班级>>:').strip()
        if  class_id.isdigit() :#判断是否是整数
            for i in c:#
                if int(class_id)==i.id:
                    return int(class_id)#返回班级ID
            else:
                pass
        else:
            print('选择班级有误!')
            return None
    #创建讲师
    def add_teach(self):#创建讲师
        while True:
            name =input('输入讲师姓名>>:').strip()
            user =input('输入讲师用户名>>:').strip()
            pwd =input('输入讲师密码>>:').strip()
            t1 = admin_class.Teacher(name=name,user=user,pwd=pwd)
            self.add_all(t1)
            e=input('是否继续 Y/y 继续! 其他返回').upper().strip()
            if e=='Y':continue
            break
    #学员添加
    def add_stu(self):#学员添加
        while True:
            name =input('输入学员姓名>>:').strip()
            pwd =input('输入学员密码>>:').strip()
            qq =input('输入学员QQ>>:').strip()
            if not qq.isdigit():
                print('QQ必需是数字')
                continue
            s=admin_class.Student(name=name,pwd=pwd,qq=int(qq))
            self.add_all(s)
            e=input('是否继续 Y/y 继续! 其他返回').upper().strip()
            if e=='Y':continue
            break

    #查看学员
    def stu_l(self):
        student_l=self.Session.query(admin_class.Student).all()
        for i in student_l:
            print('ID:',i.id,'学员姓名:',i.name,'QQ:',i.qq,'培训班级:',i.class_name)
        return student_l

    #学员选择
    def stu_cher(self):
        student_l=self.stu_l()
        stu_id=input('请按ID选择学员>>:').strip()
        if  stu_id.isdigit() :#判断是否是整数
            for i in student_l:#
                if int(stu_id)==i.id:
                    return int(stu_id)#返回班级ID
            else:
                pass
        else:
            print('选择学员有误!')
            return None

    #班级关联学员
    def class_student(self):#班级增加学员
        print('\033[35;1m班级关联学员界面\033[0m'.center(60,'='))
        cla_id=self.class_cher()#调用查看班级
        if not cla_id:return None
        #获取班级对象
        c=self.Session.query(admin_class.Class_name).filter(admin_class.Class_name.id==cla_id).first()
        if not c:return None
        stu_id=self.stu_cher()
        #student_qq=input('请输入学生QQ号码>>:').strip()
        s_qq=self.Session.query(admin_class.Student).filter(admin_class.Student.id==stu_id).first()#学员qq对象
        if s_qq:#如果有这个qq
            c.students.append(s_qq)#加入班级
            self.Session.commit()
            print('加入班级成功！')
        else:
            return print('对应的学员不存在')

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
            return
        except Exception as e:
            self.Session.rollback()#
            print('操作失败!,可能该信息已经存在!')
            print(e)
            return
    #退出
    def tech_exit(self):
        return  exit()

     #登陆
    #登陆
    def user_log(self):#登陆
        user_n=input('请输入管理员用户名>>:').strip()
        aut_obj=self.Session.query(admin_class.Admin_user).filter(admin_class.Admin_user.name==user_n).first()
        if aut_obj:
            #print(self.aut_obj_1.pwd)#用户对应密码
            pwds=input('请输入密码>>:').strip()
            if pwds == aut_obj.pwd:

                self.openatin()
            else:
                print('密码有误')
                return
        else:
            print('输入的用户名不存')
            return
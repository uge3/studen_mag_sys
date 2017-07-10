#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#python 
#2017/7/7    17:46
#__author__='Administrator'
# 创建表
import os ,sys
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#获取相对路径转为绝对路径赋于变量
sys.path.append(BASE_DIR)#增加环境变量
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index,Table,DATE
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy import func #统计
from  cfg import config
Base = declarative_base()#生成orm 基类

#创建班级关联学员表,自动维护
class_name_m2m_student = Table('class_name_m2m_student', Base.metadata,
                        Column('class_name_id',Integer,ForeignKey('class_name.id')),#关联外键,班级id
                        Column('student_id',Integer,ForeignKey('student.id')),#关联外键,学员id
                        )
#创建班级关联老师表,自动维护
teacher_name_m2m_class = Table('teacher_name_m2m_class', Base.metadata,
                        Column('teacher_id',Integer,ForeignKey('teacher.id')),#关联外键,老师id
                        Column('class_name_id',Integer,ForeignKey('class_name.id')),#关联外键,班级id
                        )
#班级表
class Class_name(Base):#班级表
    __tablename__ = 'class_name'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),unique=True)
    students = relationship('Student',secondary=class_name_m2m_student,backref='class_name')#关联学员,班级
    #teachers = relationship('Teacher',secondary=class_name_m2m_teacher,backref='class_name')#关联老师,班级
    def __repr__(self):
        return self.name

#老师表
class Teacher(Base):#老师表
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    user = Column(String(32),unique=True)
    pwd = Column(String(32))
    class_n = relationship('Class_name',secondary=teacher_name_m2m_class,backref='teach_name')#关联老师,班级
    def __repr__(self):
        return self.name

#学员表
class Student(Base):#学员表
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    pwd = Column(String(64))
    qq = Column(Integer,nullable=False,unique=True)
    def __repr__(self):
        return self.id

#进度  课节表
class Lesson(Base):
    __tablename__='lesson'
    id = Column(Integer, primary_key=True)
    name=Column(String(32),unique=True)#唯一课节名
    def __repr__(self):
        return self.name

#课程表
class Class_Day(Base):#课程表
    __tablename__='class_day'
    id=Column(Integer,primary_key=True)
    class_id=Column(Integer,ForeignKey("class_name.id"),nullable=False)#外键 班级
    lesson_id= Column(Integer,ForeignKey("lesson.id"),nullable=False)#课程进度
    class_n=relationship("Class_name",foreign_keys=[class_id],backref="m_class_day")#自定义关联反查 班级Class_name通过m_class_day 查Class_day
    lesson_n=relationship("Lesson",foreign_keys=[lesson_id],backref="m_lesson_day")#自定义关联反查 课节Lesson通过m_lesson_day 查Class_day
    def __repr__(self):
        return self.id#课程名ID

class Student_work(Base):#  作业 上 课记录
    __tablename__='student_work'
    id=Column(Integer,primary_key=True)
    students_id=Column(Integer,ForeignKey("student.id"))#外键 学员ID
    class_id= Column(Integer,ForeignKey('class_day.id'))#班级课程 日期 ID
    status= Column(String(32),nullable=False)#作业提交 状态
    results= Column(String(64))#成绩
    students_w=relationship("Student",foreign_keys=[students_id],backref="m_study_class")#自定义关联反查 学员类Student通过m_study_class 查student_work
    stu_class=relationship("Class_Day",foreign_keys=[class_id],backref="class_stu_work")#自定义关联反查 班级Class_name通过m_class_study 查Student_work

class Admin_user(Base):
    __tablename__='admin_user'
    id=Column(Integer,primary_key=True)
    name=Column(String(32),nullable=False,unique=True)
    pwd=Column(String(64),nullable=False)

#                      用户 密码  主机             库
engine = create_engine(config.HOSTS,)#连接
Base.metadata.create_all(engine)#创建表结构

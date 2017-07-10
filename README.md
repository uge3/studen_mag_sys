学员管理系统

实现功能:
1、系统初始化
2、管理员视图
    功能：创建讲师、查看讲师、创建班级、查看班级、关联讲师与班级、创建学员、查看学员、班级关联学员
3、讲师视图
    功能：管理班级、创建班级（自动与自己关联）、班级增加学员、增加新课节、
          指定班级上课，选择上课课节（自动创建课程记录，同时为这个班的每位学员创建一条上课纪录）
          批改成绩（先选择一个班级、再选择学员）
4、学员视图
    功能：提交作业
          查看作业成绩
          查看班级中的总成绩排名


stude_mag_sys/#程序目录
|- - -__init__.py
|- - -bin/#启动目录
|      |- - -__init__.py
|      |- - -admin_start.py#管理员视图启动
|      |- - -mag_init.py#系统初始化
|      |- - -student.py#学员视图启动
|      |- - -teach_start.py#讲师视图启动
|
|- - -cfg/#配置目录
|      |- - -__init__.py
|      |- - -config.py#配置文件
|
|- - -core/#主逻辑目录
|      |- - -__init__.py
|      |- - -admain_class.py#主要逻辑 类
|      |- - -admin_log.py#管理员逻辑 类
|      |- - -student_class.py#学员逻辑 类
|      |- - -teach_class.py#讲师逻辑 类
|
|- - -REDMAE
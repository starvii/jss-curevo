from sqlalchemy import Table, Column, INTEGER, VARCHAR, CHAR, TEXT, DATETIME, Index
from model import engine, metadata

# 课程、章节表
course = \
    Table('course', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True, doc=('list', 'detail')),
          Column('code', VARCHAR(100), doc=('list', 'detail', 'edit')),  # 课程、章节编号
          Column('name', VARCHAR(255), doc=('list', 'detail', 'edit')),  # 课程、章节名称
          Column('parent_id', CHAR(20), doc=('list', 'detail', 'edit')),  # 上级章节、课程ID
          Column('display_order', INTEGER, doc=('list', 'detail', 'edit')),
          Column('comment', TEXT, doc=('detail', 'edit')),  # 备注
          Column('delete_at', DATETIME),
          Index('idx_course_id', 'id', unique=True),
          Index('idx_course_delete_at', 'delete_at'),
          )

# 章节依赖关系表
course_dependency = \
    Table('course_dependency', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True, doc=('list', 'detail')),
          Column('being_dependent_id', VARCHAR(20), doc=('list', 'detail', 'edit')),
          Column('dependent_id', VARCHAR(20), doc=('list', 'detail', 'edit')),
          Column('delete_at', DATETIME),
          Index('idx_course_dependency_id', 'id', unique=True),
          Index('idx_course_dependency_delete_at', 'delete_at'),
          )

# 教师信息表
teacher = \
    Table('teacher', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True, doc=('list', 'detail')),
          Column('code', VARCHAR(50), doc=('list', 'detail', 'edit')),  # 教师编号
          Column('name', VARCHAR(50), doc=('list', 'detail', 'edit')),  # 教师姓名
          Column('unit', VARCHAR(100), doc=('list', 'detail', 'edit')),  # 工作单位，医学院、附一、附二等
          Column('dept', VARCHAR(100), doc=('list', 'detail', 'edit')),  # 部门、科室等
          Column('phone', VARCHAR(50), doc=('list', 'detail', 'edit')),  # 联系电话
          Column('email', VARCHAR(100), doc=('detail', 'edit')),  # 邮箱
          Column('comment', TEXT, doc=('detail', 'edit')),  # 备注
          Column('delete_at', DATETIME),
          Index('idx_teacher_id', 'id', unique=True),
          Index('idx_teacher_delete_at', 'delete_at'),
          )

# 教师、课程信息对应关系表
teacher_course = \
    Table('teacher_course', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True, doc=('list', 'detail')),
          Column('teacher_id', CHAR(20), doc=('list', 'detail', 'edit')),
          Column('course_id', CHAR(20), doc=('list', 'detail', 'edit')),
          Column('level', INTEGER, doc=('list', 'detail', 'edit')),
          Column('delete_at', DATETIME),
          Index('idx_teacher_course_id', 'id', unique=True),
          Index('idx_teacher_course_delete_at', 'delete_at'),
          )

# 行政班
natural_class = \
    Table('natural_class', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True, doc=('list', 'detail')),
          Column('grade', VARCHAR(10), doc=('list', 'detail', 'edit')),  # 2015级
          Column('belong_to_college', VARCHAR(20), doc=('list', 'detail', 'edit')),  # 仁济学院
          Column('dept', VARCHAR(50), doc=('list', 'detail', 'edit')),  # 护理学专业
          Column('name', VARCHAR(100), doc=('list', 'detail', 'edit')),  # 1班
          Column('student_count', INTEGER, doc=('list', 'detail', 'edit')),
          Column('comment', TEXT, doc=('detail', 'edit')),
          Column('delete_at', DATETIME),
          Index('idx_natural_class_id', 'id', unique=True),
          Index('idx_natural_class_delete_at', 'delete_at'),
          )

# 教学班
teaching_class = \
    Table('teaching_class', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True, doc=('list', 'detail')),
          Column('name', VARCHAR(100), doc=('list', 'detail', 'edit')),
          Column('include_natural_class_ids', TEXT, doc=('list', 'detail', 'edit')),
          Column('comment', TEXT, doc=('detail', 'edit')),
          Column('delete_at', DATETIME),
          Index('idx_teaching_class_id', 'id', unique=True),
          Index('idx_teaching_class_delete_at', 'delete_at'),
          )

# 课程安排总表
schedule = \
    Table('schedule', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True, doc=('list', 'detail')),
          Column('subject_id', CHAR(20), doc=('list', 'detail', 'edit')),
          Column('weekday', INTEGER, doc=('list', 'detail', 'edit')),
          Column('time_range', VARCHAR(50), doc=('list', 'detail', 'edit')),
          Column('course_id', CHAR(20), doc=('list', 'detail', 'edit')),
          Column('delete_at', DATETIME),
          Index('idx_schedule_id', 'id', unique=True),
          Index('idx_schedule_delete_at', 'delete_at'),
          )

# 排课主题表 TODO: 待细化
schedule_subject = \
    Table('schedule_subject', metadata,
          Column('db_id', INTEGER, primary_key=True, autoincrement=True),
          Column('id', CHAR(20), unique=True),
          Column('name', VARCHAR(200)),
          Column('date_range', TEXT),
          Column('date_exchange', TEXT),
          Column('course_ids', TEXT),
          Column('teacher_ids', TEXT),
          Column('delete_at', DATETIME),
          Index('idx_schedule_subject_id', 'id', unique=True),
          Index('idx_schedule_subject_delete_at', 'delete_at'),
          )


def create():
    metadata.create_all(bind=engine)


def drop():
    metadata.drop_all(bind=engine)


if '__main__' == __name__:
    create()

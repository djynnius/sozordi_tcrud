from sqlalchemy import (
    create_engine, 
    Table,
    Column, 
    String, 
    Integer, 
    Float,
    Text, 
    DateTime, 
    Boolean, 
    ForeignKey
)
from sqlalchemy.orm import (
    sessionmaker, 
    declarative_base, 
    relationship
)

from datetime import datetime


Base = declarative_base()



#many to many tables
students_subjects = Table(
    'students_subjects', 
    Base.metadata, 
    Column('id', Integer, primary_key=True), 
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
)    

teachers_subjects = Table(
    'teachers_subjects', 
    Base.metadata, 
    Column('id', Integer, primary_key=True), 
    Column('teacher_id', Integer, ForeignKey('teachers.id')),
    Column('subject_id', Integer, ForeignKey('subjects.id'))
) 

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    sex = Column(String(10))
    age = Column(Integer)
    reg_num = Column(String(10), unique=True)
    created_at = Column(DateTime, default=datetime.now)
    subjects = relationship('Subject', secondary=students_subjects, back_populates='courses')

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(30))
    lastname = Column(String(30))
    sex = Column(String(10))
    staff_num = Column(String(10), unique=True)
    created_at = Column(DateTime, default=datetime.now)
    subjects = relationship('Subject', secondary=teachers_subjects, back_populates='courses')    

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject = Column(String(30))
    code = Column(String(30))
    credits = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

if __name__ == '__main__':
    from pathlib import Path

    root = Path().absolute()
    root = str(root)
    root = root.split("/")[:-1]
    root = "/".join(root)
    
    engine = create_engine(f"sqlite:///{root}/school.db")

    Base.metadata.create_all(bind=engine)
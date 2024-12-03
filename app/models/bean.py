from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)  # Tên lớp học
    description = Column(String, nullable=True)  # Mô tả lớp học

    # Quan hệ một-nhiều: Một lớp có nhiều sinh viên
    students = relationship("Student", back_populates="classroom")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Tên sinh viên
    age = Column(Integer, nullable=False)  # Tuổi
    email = Column(String, unique=True, index=True, nullable=False)  # Email
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))  # Liên kết tới lớp học

    # Quan hệ ngược: Sinh viên thuộc một lớp học
    classroom = relationship("Classroom", back_populates="students")

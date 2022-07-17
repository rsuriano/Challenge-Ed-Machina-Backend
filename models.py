from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from db_conn import Base

# Association tables

students_degrees = Table(
    "students_degrees",
    Base.metadata,
    Column("student_id", ForeignKey("student.id"), primary_key=True),
    Column("degree_id", ForeignKey("degree.id"), primary_key=True)
)

subjects_degrees = Table(
    "subjects_degrees",
    Base.metadata, 
    Column("subject_id", ForeignKey("subject.id"), primary_key=True),
    Column("degree_id", ForeignKey("degree.id"), primary_key = True)
)

class StudentsSubjects(Base):
    __tablename__ = "students_subjects"

    student_id      =   Column(ForeignKey("student.id"), primary_key=True)
    subject_id      =   Column(ForeignKey("subject.id"), primary_key=True)
    attempt_number  =   Column(Integer)
    student         =   relationship("Student", back_populates="subjects")
    subject         =   relationship("Subject", back_populates="students")


# Main classes

class Student(Base):
    __tablename__ = "student"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, index=True)
    email           =   Column(String, unique=True, index=True)
    phone           =   Column(Integer)
    enrollment_year =   Column(Integer)

    degrees         =   relationship("Degree", secondary="students_degrees", back_populates="students") 
    subjects        =   relationship("StudentsSubjects", back_populates="student")


class Subject(Base):
    __tablename__ = "subject"

    id          =   Column(Integer, primary_key=True, index=True)
    name        =   Column(String, index=True)
    total_hours =   Column(Integer)

    degrees     =   relationship("Degree", secondary="subjects_degrees", back_populates="subjects")
    students    =   relationship("StudentsSubjects", back_populates="subject")


class Degree(Base):
    __tablename__ = "degree"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, index=True)
    length_years    =   Column(Integer)

    students        =   relationship("Student", secondary="students_degrees", back_populates="degrees")
    subjects        =   relationship("Subject", secondary="subjects_degrees", back_populates="degrees")

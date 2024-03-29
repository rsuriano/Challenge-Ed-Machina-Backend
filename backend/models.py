'''Database models and associations'''
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db_conn import Base

# Main entities

class Degree(Base):
    '''Degree: represents a major or course that has many Subjects and enrolled Students.'''
    __tablename__ = "degree"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, unique=True, index=True)
    length_years    =   Column(Integer)

    subjects        =   relationship("Subject", back_populates="degree")
    students        =   relationship("StudentDegree", back_populates="degree")

class Subject(Base):
    '''Subject: represents a Subject that is part of a Degree.'''
    __tablename__ = "subject"

    id          =   Column(Integer, primary_key=True, index=True)
    name        =   Column(String, unique=True, index=True)
    total_hours =   Column(Integer)
    degree_id   =   Column(Integer, ForeignKey("degree.id"))

    degree      =   relationship("Degree", back_populates="subjects")
    students    =   relationship("StudentSubject", back_populates="subject")

class Student(Base):
    '''Student: represents a Student that is enrolled to one or several Degrees.'''
    __tablename__ = "student"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, index=True)
    email           =   Column(String, unique=True, index=True)
    address         =   Column(String)
    phone           =   Column(Integer)
    
    degrees         =   relationship("StudentDegree", back_populates="student")
    subjects        =   relationship("StudentSubject", back_populates="student")


# Association tables

class StudentDegree(Base):
    '''StudentDegree: association object between a Student and a Degree.'''
    __tablename__ = "student_degree"

    student_id      =   Column(Integer, ForeignKey("student.id"), primary_key=True, index=True)
    degree_id       =   Column(Integer, ForeignKey("degree.id"), primary_key=True, index=True)
    enrollment_year =   Column(Integer)

    student         =   relationship("Student", back_populates="degrees")
    degree          =   relationship("Degree", back_populates="students")

class StudentSubject(Base):
    ''' StudentSubject: association object between a Student and a Subject.'''
    __tablename__ = "student_subject"

    student_id      =   Column(ForeignKey("student.id"), primary_key=True, index=True)
    subject_id      =   Column(ForeignKey("subject.id"), primary_key=True, index=True)
    attempt_number  =   Column(Integer)

    student         =   relationship("Student", back_populates="subjects")
    subject         =   relationship("Subject", back_populates="students")

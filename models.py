'''Database models and associations'''
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db_conn import Base

# Main entities

class Student(Base):
    '''Student: represents a Student that is enrolled to one or several Degrees.'''
    __tablename__ = "student"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, index=True)
    email           =   Column(String, unique=True, index=True)
    address         =   Column(String)
    phone           =   Column(Integer)
    
    degrees         =   relationship("Enrollment", back_populates="student")
    subjects        =   relationship("Lead", back_populates="student")


class Subject(Base):
    '''Subject: represents a Subject that is part of a Degree.'''
    __tablename__ = "subject"

    id          =   Column(Integer, primary_key=True, index=True)
    name        =   Column(String, unique=True, index=True)
    total_hours =   Column(Integer)
    degree_id   =   Column(Integer, ForeignKey("degree.id"))

    degree      =   relationship("Degree", back_populates="subjects")
    students    =   relationship("Lead", back_populates="subject")


class Degree(Base):
    '''Degree: represents a major or course that has many Subjects and enrolled Students.'''
    __tablename__ = "degree"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, unique=True, index=True)
    length_years    =   Column(Integer)

    subjects        =   relationship("Subject", back_populates="degree")
    students        =   relationship("Enrollment", back_populates="degree")


# Association tables

class Enrollment(Base):
    '''Enrollment: association object between a Student and a Degree.'''
    __tablename__ = "student_degree"

    student_id      =   Column(Integer, ForeignKey("student.id"), primary_key=True, index=True)
    degree_id       =   Column(Integer, ForeignKey("degree.id"), primary_key=True, index=True)
    enrollment_year =   Column(Integer)

    student         =   relationship("Student", back_populates="degrees")
    degree          =   relationship("Degree", back_populates="students")

class Lead(Base):
    ''' Lead: association object between a Student and a Subject.'''
    __tablename__ = "student_subject"
    __table_args__ = (UniqueConstraint('student_id', 'subject_id'), )

    id              =   Column(Integer, primary_key=True, index=True)
    student_id      =   Column(ForeignKey("student.id"), index=True)
    subject_id      =   Column(ForeignKey("subject.id"), index=True)
    attempt_number  =   Column(Integer)

    student         =   relationship("Student", back_populates="subjects")
    subject         =   relationship("Subject", back_populates="students")

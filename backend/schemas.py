'''Schemas for API validation'''
from pydantic import BaseModel


'''Base schemas'''

class DegreeBase(BaseModel):
    name: str
    length_years: int

    class Config:
        orm_mode = True

class SubjectBase(BaseModel):
    name: str
    total_hours: int

    class Config:
        orm_mode = True

class StudentBase(BaseModel):
    name: str
    email: str
    address: str
    phone: int

    class Config:
        orm_mode = True

class EnrollmentBase(BaseModel):
    enrollment_year: int

    class Config:
        orm_mode = True

class LeadBase(BaseModel):
    attempt_number: int

    class Config:
        orm_mode = True


'''Create schemas'''

class DegreeCreate(DegreeBase):
    pass

class SubjectCreate(SubjectBase):
    degree_id: int

class StudentCreate(StudentBase):
    pass

class EnrollmentCreate(EnrollmentBase):
    student_id: int
    degree_id: int

class LeadCreate(LeadBase):
    student_id: int
    subject_id: int


'''Base schemas'''

class Degree(DegreeBase):
    id: int

class Subject(SubjectBase):
    id: int
    degree: Degree

class Student(StudentBase):
    id: int

class Enrollment(EnrollmentBase):
    student: Student
    degree: Degree

class Lead(LeadBase):
    id: int
    student: Student
    subject: Subject

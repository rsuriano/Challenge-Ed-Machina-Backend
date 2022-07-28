'''Schemas for API validation'''
from typing import Any
from pydantic import BaseModel
from pydantic.utils import GetterDict


'''Custom Getters for Association Objects'''
class StudentSubjectGetter(GetterDict):
    def get(self, key:str, default: Any = None) -> Any:
        if key in {'id', 'name', 'length_years'}:
            return getattr(self._obj.subject, key)
        else:
            return super(StudentSubjectGetter, self).get(key, default)

class StudentSubjectGetter(GetterDict):
    def get(self, key:str, default: Any = None) -> Any:
        if key in {'id', 'name', 'total_hours'}:
            return getattr(self._obj.subject, key)
        else:
            return super(StudentSubjectGetter, self).get(key, default)

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

class StudentDegreeBase(BaseModel):
    enrollment_year: int

    class Config:
        orm_mode = True

class StudentSubjectBase(BaseModel):
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

class StudentDegreeCreate(StudentDegreeBase):
    degree_id: int

class StudentSubjectCreate(StudentSubjectBase):
    subject_id: int

class LeadCreate(StudentCreate):
    degrees: list[StudentDegreeCreate]
    subjects: list[StudentSubjectCreate]


'''Base schemas'''

class Degree(DegreeBase):
    id: int

class Subject(SubjectBase):
    id: int
    degree: Degree

class Student(StudentBase):
    id: int

class StudentDegree(StudentDegreeBase):
    degree: Degree

class StudentSubject(StudentSubjectBase):
    subject: Subject

class Lead(Student):
    degrees: list[StudentDegree]
    subjects: list[StudentSubject]
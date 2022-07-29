'''Data creation and retrieval'''
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
import models, schemas


''' Save data to database '''

def create_degree(db: Session, degree: schemas.DegreeCreate):
    try:
        db_degree = models.Degree(name=degree.name, length_years=degree.length_years)
        db.add(db_degree)
        db.commit()
        db.refresh(db_degree)
        return db_degree
    
    # Catch duplicated Degree (name)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Degree already exists.')
    

def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_degree = get_degree_by_id(db=db, degree_id=subject.degree_id)

    # Raise exception if degree doesn't exist in DB
    if db_degree is None:
        raise HTTPException(status_code=400, detail='Degree not found.')

    else:
        # Try to save new subject
        try:
            db_subject = models.Subject(name=subject.name, total_hours=subject.total_hours, degree=db_degree)
            db.add(db_subject)
            db.commit()
            db.refresh(db_subject)
            return db_subject

        # Catch duplicated Subject (name)
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Subject name already exists.')
        

def create_lead(db: Session, lead: schemas.LeadCreate):
    # Save basic Student data
    try:
        db_student = models.Student(\
            name=lead.name, email=lead.email, address=lead.address, phone=lead.phone)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)

    # Catch duplicated Student
    except IntegrityError:
        raise HTTPException(status_code=400, \
            detail=f'Student with email {lead.email} is already registered.')
    
    # Save StudentDegree associations
    for student_degree in lead.degrees:
        db_degree = get_degree_by_id(db, degree_id=student_degree.degree_id)

        # Raise exception if degree doesn't exist in DB
        if (db_degree is None):
            raise HTTPException(status_code=400, \
                detail=f'Degree id {student_degree.degree_id} not found.')

        # Add the Student's Degree to DB Session
        try:
            db_student_degree = models.StudentDegree(enrollment_year=student_degree.enrollment_year)
            db_student_degree.degree = db_degree
            db_student.degrees.append(db_student_degree)
            db.add(db_student)

        # Raise exception if the Student is already enrolled to that Degree
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, \
                detail=f'Student is already enrolled to {db_degree.name}.')
    
    # Save Degrees to database
    db.commit()
    db.refresh(db_student)

    # Save StudentSubject associations
    for student_subject in lead.subjects:
        db_subject = get_subject_by_id(db, subject_id=student_subject.subject_id)

        # Raise exception if subject doesn't exist in DB
        if db_subject is None:
            raise HTTPException(status_code=400, \
                detail=f'Subject id {db_subject.id} not found.')

        # Check if Subject doesn't belong to any of the Student's enrolled Degrees
        if db_subject.degree_id not in [degrees_list.degree.id for degrees_list in db_student.degrees]:
            raise HTTPException(\
                status_code=400,\
                detail=f"Subject id {db_subject.id} doesn't belong to any of the student's degrees.")

        # Add the Student's Subject to DB Session
        try:
            db_student_subject = models.StudentSubject(attempt_number=student_subject.attempt_number)
            db_student_subject.subject = db_subject
            db_student.subjects.append(db_student_subject)
            db.add(db_student)

        # Raise exception if the Student is already enrolled to that Subject
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, \
                detail=f'Student is already enrolled to {db_subject.name}.')
    
    # Save Degrees to database
    db.commit()
    db.refresh(db_student)

    return db_student


''' Get data from database '''

def get_degree_by_id(db: Session, degree_id: int):
    return db.query(models.Degree).where(models.Degree.id == degree_id).one_or_none()

def get_degrees(db: Session):
    return db.query(models.Degree).all()


def get_subject_by_id(db: Session, subject_id: int):
    return db.query(models.Subject).where(models.Subject.id == subject_id).one_or_none()

def get_subjects(db: Session):
    return db.query(models.Subject).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student)\
        .options(joinedload(models.Student.degrees))\
        .options(joinedload(models.Student.subjects))\
        .where(models.Student.id == student_id).one_or_none()

def get_students(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Student)\
        .options(joinedload(models.Student.degrees))\
        .options(joinedload(models.Student.subjects))\
        .offset(skip).limit(limit)\
        .all()

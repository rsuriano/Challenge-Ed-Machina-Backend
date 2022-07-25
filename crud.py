'''Data creation and retrieval'''
from psycopg2 import IntegrityError
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
        

def create_student(db: Session, student: schemas.StudentCreate):
    try:
        db_student = models.Student(\
            name=student.name, email=student.email, address=student.address, phone=student.phone)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

    # Catch duplicated Student (email)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Email is already registered.')


def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    db_student = get_student_by_id(db, student_id=enrollment.student_id)
    db_degree = get_subject_by_id(db, subject_id=enrollment.degree_id)

    # Raise exception if student or subject doesn't exist in DB.
    if (db_student is None):
        raise HTTPException(status_code=400, detail='Student not found.')
    if (db_degree is None):
        raise HTTPException(status_code=400, detail='Degree not found.')

    try:
        db_enrollment = models.Enrollment(\
            student_id=enrollment.student_id, degree_id=enrollment.degree_id,\
            enrollment_year=enrollment.enrollment_year)
        db.add(db_enrollment)
        db.commit()
        db.refresh(db_enrollment)
        return db_enrollment
    
    # Catch duplicated entry
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Enrollment already exists.')


def create_lead(db: Session, lead: schemas.LeadCreate):
    db_student = get_student_by_id(db, student_id=lead.student_id)
    db_subject = get_subject_by_id(db, subject_id=lead.subject_id)
    db_enrollments = get_enrollments_by_student_id(db, student_id=lead.student_id)

    # Check if student and subject exist, if not raise exception
    if (db_student is None):
        raise HTTPException(status_code=400, detail='Student not found.')
    if (db_subject is None):
        raise HTTPException(status_code=400, detail='Subject not found.')

    # Check if subject doesn't belong to any of the student's enrolled degrees
    if db_subject.degree_id not in [enrollment.degree.id for enrollment in db_enrollments]:
        raise HTTPException(\
            status_code=400,\
            detail="Subject doesn't belong to any of the student's degrees.")
    
    else:
        # Try to save new Lead
        try:
            db_lead = models.Lead(\
                    student_id=lead.student_id, subject_id=lead.subject_id, attempt_number=lead.attempt_number)
            db.add(db_lead)
            db.commit()
            db.refresh(db_lead)
            return db_lead
            
        # Catch duplicated entry
        except IntegrityError:
            raise HTTPException(status_code=400, detail='Lead already exists.')


''' Get data from database '''

def get_degree_by_id(db: Session, degree_id: int):
    return db.query(models.Degree).where(models.Degree.id == degree_id).one_or_none()

def get_degree_by_name(db: Session, degree_name: str):
    return db.query(models.Degree).where(models.Degree.name == degree_name).one()

def get_degrees(db: Session):
    return db.query(models.Degree).all()


def get_subject_by_id(db: Session, subject_id: int):
    return db.query(models.Subject).where(models.Subject.id == subject_id).one_or_none()

def get_subject_by_name(db: Session, subject_name: str):
    return db.query(models.Subject).where(models.Subject.name == subject_name).one()

def get_subjects(db: Session):
    return db.query(models.Subject).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(models.Student).where(models.Student.id == student_id).one_or_none()

def get_student_by_email(db: Session, student_email: str):
    return db.query(models.Student).where(models.Student.email == student_email).one()

def get_students(db: Session):
    return db.query(models.Student).all()


def get_enrollments_by_student_id(db: Session, student_id: int):
    return db.query(models.Enrollment).where(models.Enrollment.student_id == student_id).all()

def get_enrollments(db: Session):
    return db.query(models.Enrollment)\
        .options(joinedload(models.Enrollment.student))\
        .options(joinedload(models.Enrollment.degree))\
        .all()


def get_lead_by_id(db: Session, lead_id: int):
    return db.query(models.Lead)\
        .options(joinedload(models.Lead.student))\
        .options(joinedload(models.Lead.subject))\
        .where(models.Lead.id == lead_id).one_or_none()

def get_leads(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Lead)\
        .options(joinedload(models.Lead.student))\
        .options(joinedload(models.Lead.subject))\
        .order_by(models.Lead.id)\
        .offset(skip).limit(limit)\
        .all()

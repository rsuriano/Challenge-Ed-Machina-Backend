'''API endpoints'''
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud
from db_conn import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Ed I\\\\achina - Backend Challenge')

# DB for dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/degrees/", response_model=schemas.Degree, tags=["degrees"])
def create_degree(degree: schemas.DegreeCreate, db: Session = Depends(get_db)):
    return crud.create_degree(db, degree=degree)

@app.get("/degrees/", response_model=list[schemas.Degree], tags=["degrees"])
def get_degrees(db: Session = Depends(get_db)):
    return crud.get_degrees(db)


@app.post("/subjects/", response_model=schemas.Subject, tags=["subjects"])
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject=subject)

@app.get("/subjects/", response_model=list[schemas.Subject], tags=["subjects"])
def get_subjects(db: Session = Depends(get_db)):
    return crud.get_subjects(db)


@app.post("/students/", response_model=schemas.Student, tags=["students"])
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student=student)

@app.get("/students/", response_model=list[schemas.Student], tags=["students"])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.post("/enrollment/", response_model=schemas.Enrollment, tags=["enrollment"])
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.create_enrollment(db, enrollment=enrollment)

@app.get("/enrollment/", response_model=list[schemas.Enrollment], tags=["enrollment"])
def get_enrollments(db: Session = Depends(get_db)):
    return crud.get_enrollments(db)

# @app.get("/enrollment/{student_id}", response_model=list[schemas.Enrollment])
# def get_enrollment_by_student_id(student_id: int, db: Session = Depends(get_db)):
#     db_enrollment = crud.get_enrollments_by_student_id(db, student_id=student_id)
#     if db_enrollment is None:
#         raise HTTPException(status_code=404, detail="Lead not found")
#     return db_enrollment


@app.post("/leads/", response_model=schemas.Lead, tags=["leads"])
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = crud.create_lead(db, lead=lead)
    if db_lead is None:
        raise HTTPException(\
            status_code=400, \
            detail="Subject doesn't belong to any of the student's degrees.")
    else:
        return db_lead

@app.get("/leads/", response_model=list[schemas.Lead], tags=["leads"])
def get_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_leads = crud.get_leads(db, skip=skip, limit=limit)
    return db_leads

@app.get("/leads/{lead_id}", response_model=schemas.Lead, tags=["leads"])
def get_lead_by_id(lead_id: int, db: Session = Depends(get_db)):
    db_lead = crud.get_lead_by_id(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

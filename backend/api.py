'''API endpoints'''
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud
from db_conn import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(\
    title='Ed I\\\\achina - Backend Challenge',
    version='0.2.0',
    contact={
        'name': 'Ramiro Suriano',
        'url': 'https://github.com/rsuriano'
        },
    )

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


@app.post("/leads/", response_model=schemas.Lead, tags=["leads"])
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    return crud.create_lead(db, lead=lead)

@app.get("/leads/", response_model=list[schemas.Lead], tags=["leads"])
def get_leads(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if skip < 0:
        raise HTTPException(status_code=400, detail="'skip' parameter must be positive")
    if limit < 0:
        raise HTTPException(status_code=400, detail="'limit' parameter must be positive")
    return crud.get_students(db, skip=skip, limit=limit)

@app.get("/leads/{lead_id}", response_model=schemas.Lead, tags=["leads"])
def get_lead_by_id(lead_id: int, db: Session = Depends(get_db)):
    db_lead = crud.get_student_by_id(db, student_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

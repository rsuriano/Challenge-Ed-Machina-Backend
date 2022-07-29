'''Data Loader'''
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

# Connect to DB and check if it's empty
DB_URL = "postgresql://postgres:password@host.docker.internal/edmachina"
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
class Degree(Base):
    '''Degree: represents a major or course that has many Subjects and enrolled Students.'''
    __tablename__ = "degree"

    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String, unique=True, index=True)
    length_years    =   Column(Integer)

base_url = 'http://host.docker.internal:8000'
url_degrees = '/degrees/'
url_subjects = '/subjects/'
url_leads = '/leads/'

if SessionLocal().query(Degree).all() == []:
    print('Populating DB...')

    session = requests.session()

    def add_degree(name: str, length_years: int):
        data = {'name': name, 'length_years': length_years}
        r = session.post(base_url+url_degrees, json=data)
        return r.json()['id']

    def add_subject(name: str, total_hours: int, degree_id: int):
        data = {'name': name, 'total_hours': total_hours, 'degree_id': degree_id}
        r = session.post(base_url+url_subjects, json=data)
        return r.json()['id']

    def add_lead(name: str, email: str, address: str, phone: int, **kwargs):
        data = {'name': name, 'email': email, 'address': address, 'phone': phone,\
                'degrees': kwargs['degrees'], 'subjects': kwargs['subjects']}
        r = session.post(base_url+url_leads, json=data)
        return r.json()['id']

    # Try to save data to DB
    try:
        # Add degrees
        d1 = add_degree('Ingenieria Electronica', 5)
        d2 = add_degree('Ingeniería en Sistemas', 5)
        d3 = add_degree('Contador Público', 5)

        # Add subjects
        s1 = add_subject('Introducción a las Ingenierías', 64, d1)
        s2 = add_subject('Algebra y Geometría', 128, d1)
        s3 = add_subject('Analisis Matematico I', 128, d1)
        s4 = add_subject('Quimica General para Ingeniería', 96, d1)

        s5 = add_subject('Elementos de Algebra y Geometría', 128, d2)
        s6 = add_subject('Resolución de Problemas y Algoritmos', 128, d2)
        s7 = add_subject('Introducción a la Ingeniería de Software', 128, d2)
        s8 = add_subject('Lenguajes Formales y Autómatas', 128, d2)

        s9 = add_subject('Introducción a la Administración', 96, d3)
        s10 = add_subject('Introducción al Estudio de las Ciencias Sociales', 96, d3)
        s11 = add_subject('Matemática I C', 96, d3)
        s12 = add_subject('Contabilidad Básica', 96, d3)

        # Add Leads
        add_lead('Ramiro', 'r@s.com', 'Alem 1400', 12345,\
                    degrees=[
                        {'enrollment_year': 2014, 'degree_id': d1}
                    ],
                    subjects=[
                        {'attempt_number': 1, 'subject_id': s1},
                        {'attempt_number': 2, 'subject_id': s2},
                        {'attempt_number': 2, 'subject_id': s3},
                        {'attempt_number': 4, 'subject_id': s4},
                    ])

        add_lead('Juan', 'j@edu.com', 'Viamonte 430', 12345,\
                    degrees=[
                        {'enrollment_year': 2012, 'degree_id': d1},
                        {'enrollment_year': 2015, 'degree_id': d2}
                    ],
                    subjects=[
                        {'attempt_number': 2, 'subject_id': s1},
                        {'attempt_number': 1, 'subject_id': s2},
                        {'attempt_number': 1, 'subject_id': s5},
                        {'attempt_number': 1, 'subject_id': s6},
                    ])

        add_lead('María', 'm@edu.com', 'Viamonte 430', 12345,\
                    degrees=[
                        {'enrollment_year': 2018, 'degree_id': d3}
                    ],
                    subjects=[
                        {'attempt_number': 2, 'subject_id': s9},
                        {'attempt_number': 1, 'subject_id': s10},
                        {'attempt_number': 1, 'subject_id': s11},
                        {'attempt_number': 1, 'subject_id': s12},
                    ])

        add_lead('Lucas', 'l@edu.com', 'Alvear 2500', 12345,\
                    degrees=[
                        {'enrollment_year': 2020, 'degree_id': d2}
                    ],
                    subjects=[
                        {'attempt_number': 5, 'subject_id': s5},
                        {'attempt_number': 1, 'subject_id': s6}
                    ])

        add_lead('Gabriel', 'g@edu.com', 'Cordoba 4700', 12345,\
                    degrees=[
                        {'enrollment_year': 2016, 'degree_id': d3},
                        {'enrollment_year': 2010, 'degree_id': d1},
                    ],
                    subjects=[
                        {'attempt_number': 2, 'subject_id': s11},
                        {'attempt_number': 3, 'subject_id': s9}
                    ])

        add_lead('Laura', 'lau@edu.com', 'Tucuman 2200', 12345,\
                    degrees=[
                        {'enrollment_year': 2001, 'degree_id': d1},
                        {'enrollment_year': 2002, 'degree_id': d2},
                        {'enrollment_year': 2003, 'degree_id': d3},
                    ],
                    subjects=[
                        {'attempt_number': 5, 'subject_id': s3},
                        {'attempt_number': 2, 'subject_id': s8},
                        {'attempt_number': 1, 'subject_id': s10}
                    ])
    except:
        # Data is already on the DB
        pass
else:
    print('Database is not empty.')
    #print(SessionLocal().query(Degree).all())
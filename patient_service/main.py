import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models #
import database #
import requests
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

# Ganti baris ini
APPOINTMENT_SERVICE_URL = "http://appointment-service:8003/appointments"


@strawberry.type
class PatientType:
    id: int
    name: str
    age: int
    gender: str

@strawberry.type
class AppointmentType:
    id: int
    patient_id: int
    doctor_id: int
    schedule: str

@strawberry.type
class Query:
    @strawberry.field
    def patients(self, info) -> List[PatientType]:
        with get_db() as db:
            return [PatientType(id=p.id, name=p.name, age=p.age, gender=p.gender) for p in db.query(models.Patient).all()]

    @strawberry.field
    def patient(self, info, patient_id: int) -> Optional[PatientType]:
        with get_db() as db:
            p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
            if p:
                return PatientType(id=p.id, name=p.name, age=p.age, gender=p.gender)
            return None

    @strawberry.field
    def patient_appointments(self, info, patient_id: int) -> List[AppointmentType]:
        resp = requests.get(f"{APPOINTMENT_SERVICE_URL}?patient_id={patient_id}")
        if resp.status_code == 200:
            return [AppointmentType(**a) for a in resp.json()]
        return []

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_patient(self, name: str, age: int, gender: str) -> PatientType:
        with get_db() as db:
            db_patient = models.Patient(name=name, age=age, gender=gender)
            db.add(db_patient)
            db.commit()
            db.refresh(db_patient)
            return PatientType(id=db_patient.id, name=db_patient.name, age=db_patient.age, gender=db_patient.gender)

from contextlib import contextmanager
@contextmanager
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

schema = strawberry.Schema(query=Query, mutation=Mutation)
from strawberry.fastapi import GraphQLRouter
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

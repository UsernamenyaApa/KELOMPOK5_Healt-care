import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import database
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



APPOINTMENT_SERVICE_URL = "http://appointment-service:8003/appointments"

@strawberry.type
class DoctorType:
    id: int
    name: str
    specialization: str

@strawberry.type
class AppointmentType:
    id: int
    patient_id: int
    doctor_id: int
    schedule: str

@strawberry.type
class Query:
    @strawberry.field
    def doctors(self, info) -> List[DoctorType]:
        with get_db() as db:
            return [DoctorType(id=d.id, name=d.name, specialization=d.specialization) for d in db.query(models.Doctor).all()]

    @strawberry.field
    def doctor(self, info, doctor_id: int) -> Optional[DoctorType]:
        with get_db() as db:
            d = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
            if d:
                return DoctorType(id=d.id, name=d.name, specialization=d.specialization)
            return None

    @strawberry.field
    def doctor_appointments(self, info, doctor_id: int) -> List[AppointmentType]:
        resp = requests.get(f"{APPOINTMENT_SERVICE_URL}?doctor_id={doctor_id}")
        if resp.status_code == 200:
            return [AppointmentType(**a) for a in resp.json()]
        return []

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_doctor(self, name: str, specialization: str) -> DoctorType:
        with get_db() as db:
            db_doctor = models.Doctor(name=name, specialization=specialization)
            db.add(db_doctor)
            db.commit()
            db.refresh(db_doctor)
            return DoctorType(id=db_doctor.id, name=db_doctor.name, specialization=db_doctor.specialization)

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

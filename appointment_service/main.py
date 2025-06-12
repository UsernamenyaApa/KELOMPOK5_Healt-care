import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database
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

PATIENT_SERVICE_URL = "http://patient-service:8001/patients/"
DOCTOR_SERVICE_URL = "http://doctor-service:8002/doctors/"

# Strawberry GraphQL Types
@strawberry.type
class AppointmentType:
    id: int
    patient_id: int
    doctor_id: int
    schedule: str

# Query
@strawberry.type
class Query:
    @strawberry.field
    def appointments(self, info, patient_id: Optional[int] = None, doctor_id: Optional[int] = None) -> List[AppointmentType]:
        with get_db() as db:
            query = db.query(models.Appointment)
            if patient_id:
                query = query.filter(models.Appointment.patient_id == patient_id)
            if doctor_id:
                query = query.filter(models.Appointment.doctor_id == doctor_id)
            return [AppointmentType(id=a.id, patient_id=a.patient_id, doctor_id=a.doctor_id, schedule=a.schedule) for a in query.all()]

    @strawberry.field
    def appointment(self, info, appointment_id: int) -> Optional[AppointmentType]:
        with get_db() as db:
            a = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
            if a:
                return AppointmentType(id=a.id, patient_id=a.patient_id, doctor_id=a.doctor_id, schedule=a.schedule)
            return None

# Mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_appointment(self, patient_id: int, doctor_id: int, schedule: str) -> AppointmentType:
        with get_db() as db:
            patient_resp = requests.get(f"{PATIENT_SERVICE_URL}{patient_id}")
            if patient_resp.status_code != 200:
                raise Exception("Patient not found")
        doctor_resp = requests.get(f"{DOCTOR_SERVICE_URL}{doctor_id}")
        if doctor_resp.status_code != 200:
            raise Exception("Doctor not found")
        db_appointment = models.Appointment(patient_id=patient_id, doctor_id=doctor_id, schedule=schedule)
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return AppointmentType(id=db_appointment.id, patient_id=db_appointment.patient_id, doctor_id=db_appointment.doctor_id, schedule=db_appointment.schedule)

    @strawberry.mutation
    def update_appointment(self, appointment_id: int, schedule: str) -> Optional[AppointmentType]:
        db: Session = next(get_db())
        appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
        if not appointment:
            return None
        appointment.schedule = schedule
        db.commit()
        db.refresh(appointment)
        return AppointmentType(id=appointment.id, patient_id=appointment.patient_id, doctor_id=appointment.doctor_id, schedule=appointment.schedule)

    @strawberry.mutation
    def delete_appointment(self, appointment_id: int) -> bool:
        db: Session = next(get_db())
        appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
        if not appointment:
            return False
        db.delete(appointment)
        db.commit()
        return True

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

schema = strawberry.Schema(query=Query, mutation=Mutation)

from strawberry.fastapi import GraphQLRouter
from fastapi import Depends, HTTPException
from pydantic import BaseModel

class AppointmentUpdate(BaseModel):
    schedule: str

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# REST endpoint for patient_service integration
from fastapi import Query

@app.get("/appointments")
def get_appointments(patient_id: int = Query(None), db: Session = Depends(get_db)):
    query = db.query(models.Appointment)
    if patient_id is not None:
        appointments = query.filter(models.Appointment.patient_id == patient_id).all()
    else:
        appointments = query.all()
    return [
        {
            "id": a.id,
            "patient_id": a.patient_id,
            "doctor_id": a.doctor_id,
            "schedule": a.schedule
        } for a in appointments
    ]

# Pastikan kode di bawah ini ada di dalam fungsi/class yang sesuai

@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return {"detail": "Appointment deleted"}

@app.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, update: AppointmentUpdate, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.schedule = update.schedule
    db.commit()
    db.refresh(appt)
    return appt

import strawberry
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import database
import requests
from typing import List, Optional
from pydantic import BaseModel
# --- PERUBAHAN DI SINI: Impor GraphQLRouter secara langsung ---
from strawberry.fastapi import GraphQLRouter
from fastapi import HTTPException

app = FastAPI()

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Initialization ---
models.Base.metadata.create_all(bind=database.engine)

# --- Dependency ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Strawberry GraphQL Types ---
@strawberry.type
class AppointmentType:
    # Mengembalikan ke snake_case agar sesuai dengan ekspektasi frontend
    id: int
    patient_id: int
    doctor_id: int
    schedule: str

# --- GraphQL Query ---
@strawberry.type
class Query:
    @strawberry.field
    def appointments(self, info, patient_id: Optional[int] = None, doctor_id: Optional[int] = None) -> List[AppointmentType]:
        db = next(get_db())
        try:
            query = db.query(models.Appointment)
            if patient_id:
                query = query.filter(models.Appointment.patient_id == patient_id)
            if doctor_id:
                query = query.filter(models.Appointment.doctor_id == doctor_id)
            return [AppointmentType(id=a.id, patient_id=a.patient_id, doctor_id=a.doctor_id, schedule=a.schedule) for a in query.all()]
        finally:
            db.close()

    @strawberry.field
    def appointment(self, info, appointment_id: int) -> Optional[AppointmentType]:
        db = next(get_db())
        try:
            a = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
            if a:
                return AppointmentType(id=a.id, patient_id=a.patient_id, doctor_id=a.doctor_id, schedule=a.schedule)
            return None
        finally:
            db.close()

# --- GraphQL Mutation ---
@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_appointment(self, patientId: int, doctorId: int, schedule: str) -> AppointmentType:
        db = next(get_db())
        try:
            # --- PERBAIKAN PADA PATIENT SERVICE QUERY ---
            patient_query = """
            query($patientId: Int!) {
                patient(patientId: $patientId) {
                    id
                    name
                }
            }
            """
            patient_resp = requests.post(
                "http://patient-service:8001/graphql",
                json={"query": patient_query, "variables": {"patientId": patientId}}
            )

            # --- KODE DEBUGGING UNTUK MELIHAT RESPONS MENTAH ---
            print("--- DEBUGGING PATIENT RESPONSE ---")
            print(f"Status Code: {patient_resp.status_code}")
            print(f"Content-Type Header: {patient_resp.headers.get('content-type')}")
            print(f"Raw Response Body: {patient_resp.text}")
            print("--- END DEBUGGING ---")
            
            patient_data = None
            try:
                patient_data = patient_resp.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: Gagal mengurai JSON dari patient-service")
                raise Exception("Respons dari Patient Service tidak valid (bukan JSON)")

            if patient_resp.status_code != 200 or not (patient_data and patient_data.get("data", {}).get("patient")):
                raise Exception("Patient not found")

            # --- PERBAIKAN PADA DOCTOR SERVICE QUERY ---
            doctor_query = """
            query($doctorId: Int!) {
                doctor(doctorId: $doctorId) {
                    id
                    name
                }
            }
            """
            doctor_resp = requests.post(
                "http://doctor-service:8002/graphql",
                json={"query": doctor_query, "variables": {"doctorId": doctorId}}
            )
            
            doctor_data = None
            try:
                doctor_data = doctor_resp.json()
            except requests.exceptions.JSONDecodeError:
                print("Error: Gagal mengurai JSON dari doctor-service")
                raise Exception("Respons dari Doctor Service tidak valid (bukan JSON)")

            if doctor_resp.status_code != 200 or not (doctor_data and doctor_data.get("data", {}).get("doctor")):
                raise Exception("Doctor not found")

            # Simpan appointment ke database lokal
            db_appointment = models.Appointment(patient_id=patientId, doctor_id=doctorId, schedule=schedule)
            db.add(db_appointment)
            db.commit()
            db.refresh(db_appointment)
            
            return AppointmentType(
                id=db_appointment.id,
                patient_id=db_appointment.patient_id,
                doctor_id=db_appointment.doctor_id,
                schedule=db_appointment.schedule
            )
        finally:
            db.close()

    @strawberry.mutation
    def update_appointment(self, appointment_id: int, schedule: str) -> Optional[AppointmentType]:
        db = next(get_db())
        try:
            appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
            if not appointment:
                return None
            appointment.schedule = schedule
            db.commit()
            db.refresh(appointment)
            return AppointmentType(id=appointment.id, patient_id=appointment.patient_id, doctor_id=appointment.doctor_id, schedule=appointment.schedule)
        finally:
            db.close()

    @strawberry.mutation
    def delete_appointment(self, appointment_id: int) -> bool:
        db = next(get_db())
        try:
            appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
            if not appointment:
                return False
            db.delete(appointment)
            db.commit()
            return True
        finally:
            db.close()

# --- Schema dan GraphQL Router ---
schema = strawberry.Schema(query=Query, mutation=Mutation)
# --- PERUBAHAN DI SINI: Menggunakan GraphQLRouter yang sudah diimpor ---
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


# --- REST Endpoints (jika masih diperlukan) ---
class AppointmentUpdate(BaseModel):
    schedule: str

@app.get("/appointments")
def get_rest_appointments(patient_id: Optional[int] = None, db: Session = Depends(get_db)):
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

@app.get("/appointments/{appointment_id}")
def get_rest_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.delete("/appointments/{appointment_id}")
def delete_rest_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return {"detail": "Appointment deleted"}

@app.put("/appointments/{appointment_id}")
def update_rest_appointment(appointment_id: int, update: AppointmentUpdate, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appt.schedule = update.schedule
    db.commit()
    db.refresh(appt)
    return appt

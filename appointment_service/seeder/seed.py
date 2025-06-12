import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import random

# Import dari parent directory
from .. import models
from ..database import engine, Base

def run_seed():
    # Hapus semua data dan buat tabel baru
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Buat session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Buat beberapa janji temu dengan jadwal acak
    appointments = []
    start_date = datetime.now()

    # Asumsikan ada 10 pasien dan 7 dokter (sesuai seed data lainnya)
    for i in range(15):  # Buat 15 janji temu
        patient_id = random.randint(1, 10)  # ID pasien 1-10
        doctor_id = random.randint(1, 7)    # ID dokter 1-7
        
        # Jadwal acak dalam 30 hari ke depan
        days_ahead = random.randint(1, 30)
        hours = random.randint(8, 16)  # Jam 8 pagi - 4 sore
        minutes = random.choice([0, 15, 30, 45])  # Interval 15 menit
        
        appointment_date = start_date + timedelta(days=days_ahead)
        schedule_time = appointment_date.replace(hour=hours, minute=minutes, second=0)
        
        # Format jadwal: 'YYYY-MM-DD HH:MM'
        schedule = schedule_time.strftime('%Y-%m-%d %H:%M')
        
        appointment = models.Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            schedule=schedule
        )
        appointments.append(appointment)

    # Tambahkan data ke database
    for appointment in appointments:
        db.add(appointment)

    db.commit()
    print(f"Berhasil menambahkan {len(appointments)} data janji temu")
    db.close()

# Untuk menjalankan seeder secara langsung
if __name__ == "__main__":
    run_seed()
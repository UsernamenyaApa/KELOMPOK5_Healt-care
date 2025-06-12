import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    # Data dokter
    doctors = [
        models.Doctor(name="dr. Anita Wijaya, Sp.JP", specialization="Cardiology"),
        models.Doctor(name="dr. Bambang Sutrisno, Sp.KK", specialization="Dermatology"),
        models.Doctor(name="dr. Citra Dewi, Sp.PD", specialization="General Practice"),
        models.Doctor(name="dr. Dimas Prayogo, Sp.S", specialization="Neurology"),
        models.Doctor(name="dr. Eka Putri, Sp.P", specialization="Pulmonology"),
        models.Doctor(name="dr. Fajar Ramadhan, Sp.M", specialization="Ophthalmology"),
        models.Doctor(name="dr. Gita Nirmala, Sp.THT", specialization="ENT Specialist"),
    ]

    # Tambahkan data ke database
    for doctor in doctors:
        db.add(doctor)

    db.commit()
    print(f"Berhasil menambahkan {len(doctors)} data dokter")
    db.close()

# Untuk menjalankan seeder secara langsung
if __name__ == "__main__":
    run_seed()
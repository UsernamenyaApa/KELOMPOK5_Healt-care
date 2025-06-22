import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import dari parent directory
import models #
from database import engine, Base

def run_seed():
    # Hapus semua data dan buat tabel baru
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Buat session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Data pasien
    patients = [
        models.Patient(name="Ahmad Rizky", age=35, gender="Laki-laki"),
        models.Patient(name="Siti Nurhaliza", age=28, gender="Perempuan"),
        models.Patient(name="Budi Santoso", age=45, gender="Laki-laki"),
        models.Patient(name="Dewi Kartika", age=32, gender="Perempuan"),
        models.Patient(name="Eko Prasetyo", age=50, gender="Laki-laki"),
        models.Patient(name="Fitriani", age=25, gender="Perempuan"),
        models.Patient(name="Gunawan", age=42, gender="Laki-laki"),
        models.Patient(name="Hani Wijaya", age=30, gender="Perempuan"),
        models.Patient(name="Irfan Hakim", age=38, gender="Laki-laki"),
        models.Patient(name="Juwita Sari", age=27, gender="Perempuan"),
    ]

    # Tambahkan data ke database
    for patient in patients:
        db.add(patient)

    db.commit()
    print(f"Berhasil menambahkan {len(patients)} data pasien")
    db.close()

# Untuk menjalankan seeder secara langsung
if __name__ == "__main__":
    run_seed()
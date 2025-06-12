from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Tambahkan path ke PYTHONPATH agar bisa mengimport modul dari service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from patient_service.models import Patient, Base
from patient_service.database import engine

# Hapus semua data dan buat tabel baru
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Buat session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Data pasien
patients = [
    Patient(name="Ahmad Rizky", age=35, gender="Laki-laki"),
    Patient(name="Siti Nurhaliza", age=28, gender="Perempuan"),
    Patient(name="Budi Santoso", age=45, gender="Laki-laki"),
    Patient(name="Dewi Kartika", age=32, gender="Perempuan"),
    Patient(name="Eko Prasetyo", age=50, gender="Laki-laki"),
    Patient(name="Fitriani", age=25, gender="Perempuan"),
    Patient(name="Gunawan", age=42, gender="Laki-laki"),
    Patient(name="Hani Wijaya", age=30, gender="Perempuan"),
    Patient(name="Irfan Hakim", age=38, gender="Laki-laki"),
    Patient(name="Juwita Sari", age=27, gender="Perempuan"),
]

# Tambahkan data ke database
for patient in patients:
    db.add(patient)

db.commit()
print(f"Berhasil menambahkan {len(patients)} data pasien")
db.close()

database_url = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@db-patient:3306/patient_db"
)

# Gunakan database_url untuk membuat engine
engine = create_engine(database_url)
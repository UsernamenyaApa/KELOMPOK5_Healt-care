from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
# Tambahkan import os
import os

# Tambahkan path ke PYTHONPATH agar bisa mengimport modul dari service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from doctor_service.models import Doctor, Base
from doctor_service.database import engine

# Hapus semua data dan buat tabel baru
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Buat session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Data dokter
doctors = [
    Doctor(name="dr. Anita Wijaya, Sp.JP", specialization="Cardiology"),
    Doctor(name="dr. Bambang Sutrisno, Sp.KK", specialization="Dermatology"),
    Doctor(name="dr. Citra Dewi, Sp.PD", specialization="General Practice"),
    Doctor(name="dr. Dimas Prayogo, Sp.S", specialization="Neurology"),
    Doctor(name="dr. Eka Putri, Sp.P", specialization="Pulmonology"),
    Doctor(name="dr. Fajar Ramadhan, Sp.M", specialization="Ophthalmology"),
    Doctor(name="dr. Gita Nirmala, Sp.THT", specialization="ENT Specialist"),
]

# Tambahkan data ke database
for doctor in doctors:
    db.add(doctor)

db.commit()
print(f"Berhasil menambahkan {len(doctors)} data dokter")
db.close()

# Gunakan environment variable untuk koneksi database
database_url = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@db-doctor:3306/doctor_db"
)

# Gunakan database_url untuk membuat engine
engine = create_engine(database_url)
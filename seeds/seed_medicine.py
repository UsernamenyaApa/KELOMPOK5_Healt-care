from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Tambahkan path ke PYTHONPATH agar bisa mengimport modul dari service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from medicine_service.models import Medicine, Base
from medicine_service.database import engine

# Hapus semua data dan buat tabel baru
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Buat session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Data obat
medicines = [
    Medicine(name="Paracetamol", price=10000, description="Obat pereda nyeri dan penurun demam"),
    Medicine(name="Amoxicillin", price=25000, description="Antibiotik untuk infeksi bakteri"),
    Medicine(name="Omeprazole", price=20000, description="Obat untuk mengurangi asam lambung"),
    Medicine(name="Simvastatin", price=30000, description="Obat penurun kolesterol"),
    Medicine(name="Metformin", price=15000, description="Obat untuk diabetes tipe 2"),
    Medicine(name="Amlodipine", price=18000, description="Obat tekanan darah tinggi"),
    Medicine(name="Cetirizine", price=12000, description="Antihistamin untuk alergi"),
    Medicine(name="Salbutamol", price=35000, description="Obat untuk asma"),
    Medicine(name="Ibuprofen", price=8000, description="Anti-inflamasi non-steroid"),
    Medicine(name="Loratadine", price=15000, description="Antihistamin tanpa efek mengantuk"),
]

# Tambahkan data ke database
for medicine in medicines:
    db.add(medicine)

db.commit()
print(f"Berhasil menambahkan {len(medicines)} data obat")
db.close()

database_url = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@db-medicine:3306/medicine_db"
)

# Gunakan database_url untuk membuat engine
engine = create_engine(database_url)
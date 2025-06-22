import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import dari parent directory
import models
from database import engine, Base

def run_seed():
    # Hapus semua data dan buat tabel baru
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Buat session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Data obat
    medicines = [
        models.Medicine(name="Paracetamol", price=10000, description="Obat pereda nyeri dan penurun demam"),
        models.Medicine(name="Amoxicillin", price=25000, description="Antibiotik untuk infeksi bakteri"),
        models.Medicine(name="Omeprazole", price=20000, description="Obat untuk mengurangi asam lambung"),
        models.Medicine(name="Simvastatin", price=30000, description="Obat penurun kolesterol"),
        models.Medicine(name="Metformin", price=15000, description="Obat untuk diabetes tipe 2"),
        models.Medicine(name="Amlodipine", price=18000, description="Obat tekanan darah tinggi"),
        models.Medicine(name="Cetirizine", price=12000, description="Antihistamin untuk alergi"),
        models.Medicine(name="Salbutamol", price=35000, description="Obat untuk asma"),
        models.Medicine(name="Ibuprofen", price=8000, description="Anti-inflamasi non-steroid"),
        models.Medicine(name="Loratadine", price=15000, description="Antihistamin tanpa efek mengantuk"),
    ]

    # Tambahkan data ke database
    for medicine in medicines:
        db.add(medicine)

    db.commit()
    print(f"Berhasil menambahkan {len(medicines)} data obat")
    db.close()

# Untuk menjalankan seeder secara langsung
if __name__ == "__main__":
    run_seed()
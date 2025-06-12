from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Gunakan environment variable atau default ke konfigurasi Docker
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@db-patient:3306/patient_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

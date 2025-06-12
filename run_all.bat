@echo off
REM Jalankan file ini dari root project!
REM Aktifkan virtual environment
IF EXIST venv\Scripts\activate.bat call venv\Scripts\activate.bat

REM Jalankan backend FastAPI services dengan python dari venv
start cmd /k "call venv\Scripts\activate && uvicorn patient_service.main:app --reload --port 8001"
start cmd /k "call venv\Scripts\activate && uvicorn doctor_service.main:app --reload --port 8002"
start cmd /k "call venv\Scripts\activate && uvicorn appointment_service.main:app --reload --port 8003"
start cmd /k "call venv\Scripts\activate && uvicorn medicine_service.main:app --reload --port 8004"

REM Jalankan frontend
cd frontend
start cmd /k "npm start"
cd ..

echo Semua service dan frontend telah dijalankan di terminal terpisah.
pause

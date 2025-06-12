@echo off
REM Aktifkan venv (hanya untuk cmd, bukan bash)
call ..\venv\Scripts\activate

echo Menjalankan seed data untuk Healthcare Hub...

echo.
echo 1. Seed data pasien...
python seed_patient.py

echo.
echo 2. Seed data dokter...
python seed_doctor.py

echo.
echo 3. Seed data obat...
python seed_medicine.py

echo.
echo 4. Seed data janji temu...
python seed_appointment.py

REM Nonaktifkan venv setelah selesai
call ..\venv\Scripts\deactivate

echo.
echo Selesai! Semua data seed telah ditambahkan.
pause
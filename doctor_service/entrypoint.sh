#!/bin/bash

# Jalankan seeder jika RUN_SEEDER=true
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Menjalankan seeder untuk doctor service..."
    python -m doctor_service.seeder.seed
    echo "Seeder selesai!"
fi

# Jalankan aplikasi
exec uvicorn doctor_service.main:app --host 0.0.0.0 --port 8002
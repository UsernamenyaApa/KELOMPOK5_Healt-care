#!/bin/bash

# Jalankan seeder jika RUN_SEEDER=true
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Menjalankan seeder untuk patient service..."
    python -m patient_service.seeder.seed
    echo "Seeder selesai!"
fi

# Jalankan aplikasi
exec uvicorn patient_service.main:app --host 0.0.0.0 --port 8001
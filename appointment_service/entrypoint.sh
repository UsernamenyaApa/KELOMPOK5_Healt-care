#!/bin/bash

# Jalankan seeder jika RUN_SEEDER=true
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Menjalankan seeder untuk appointment service..."
    python -m appointment_service.seeder.seed
    echo "Seeder selesai!"
fi

# Jalankan aplikasi
exec uvicorn appointment_service.main:app --host 0.0.0.0 --port 8003
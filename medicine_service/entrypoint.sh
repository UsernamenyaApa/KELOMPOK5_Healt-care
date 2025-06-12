#!/bin/bash

# Jalankan seeder jika RUN_SEEDER=true
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Menjalankan seeder untuk medicine service..."
    python -m medicine_service.seeder.seed
    echo "Seeder selesai!"
fi

# Jalankan aplikasi
exec uvicorn medicine_service.main:app --host 0.0.0.0 --port 8004
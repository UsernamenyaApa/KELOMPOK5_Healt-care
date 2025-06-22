#!/bin/bash

# Jalankan seeder jika RUN_SEEDER=true
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Menjalankan seeder untuk patient service..."
    # Path seeder sekarang langsung relatif dari /app
    python -m seeder.seed # Mengubah patient_service.seeder.seed menjadi seeder.seed
    echo "Seeder selesai!"
fi

# Jalankan aplikasi
# Path main.py sekarang langsung relatif dari /app
exec uvicorn main:app --host 0.0.0.0 --port 8001 # Mengubah patient_service.main:app menjadi main:app
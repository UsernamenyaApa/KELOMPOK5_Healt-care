#!/bin/bash

# Jalankan seeder jika RUN_SEEDER=true
if [ "$RUN_SEEDER" = "true" ]; then
    echo "Menjalankan seeder untuk appointment service..."
    # Path modul Python ini sekarang langsung dari root /app
    python -m seeder.seed # Perhatikan: appointment_service.seeder.seed menjadi seeder.seed
    echo "Seeder selesai!"
fi

# Jalankan aplikasi
exec uvicorn main:app --host 0.0.0.0 --port 8003 # Perhatikan: appointment_service.main:app menjadi main:app
@echo off
echo Menjalankan semua seeder...

docker-compose run --rm patient-service bash -c "python -m patient_service.seeder.seed"
docker-compose run --rm doctor-service bash -c "python -m doctor_service.seeder.seed"
docker-compose run --rm appointment-service bash -c "python -m appointment_service.seeder.seed"
docker-compose run --rm medicine-service bash -c "python -m medicine_service.seeder.seed"
docker-compose run --rm chat-service bash -c "python -m chat_service.seeder.seed"

echo Semua seeder berhasil dijalankan!
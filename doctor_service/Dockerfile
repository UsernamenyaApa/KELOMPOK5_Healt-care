FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Script untuk menjalankan aplikasi dengan opsi seeding
COPY ./doctor_service/entrypoint.sh /app/
RUN chmod +x /app/doctor_service/entrypoint.sh

CMD ["/app/doctor_service/entrypoint.sh"]
CMD ["uvicorn", "doctor_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
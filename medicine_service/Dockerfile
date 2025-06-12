FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Script untuk menjalankan aplikasi dengan opsi seeding
COPY ./medicine_service/entrypoint.sh /app/
RUN chmod +x /app/medicine_service/entrypoint.sh

CMD ["/app/medicine_service/entrypoint.sh"]
CMD ["uvicorn", "medicine_service.main:app", "--host", "0.0.0.0", "--port", "8004"]
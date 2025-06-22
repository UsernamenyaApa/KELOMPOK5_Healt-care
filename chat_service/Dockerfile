FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Perubahan di sini: "chat_service.main:app" menjadi "main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
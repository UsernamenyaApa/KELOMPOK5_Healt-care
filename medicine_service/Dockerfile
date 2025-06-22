FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt dari folder service ini ke /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file dari folder service ini (medicine_service) ke /app
# Ini akan menyalin main.py, models.py, seeder/, entrypoint.sh dll.
COPY . /app/

# Sesuaikan path entrypoint.sh, karena sekarang ada di root /app
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Hanya gunakan satu CMD, yaitu menjalankan entrypoint script
CMD ["/app/entrypoint.sh"]
# Baris ini dihapus/dikomentari karena sudah ditangani oleh entrypoint.sh
# CMD ["uvicorn", "medicine_service.main:app", "--host", "0.0.0.0", "--port", "800X"] # Port akan 8004
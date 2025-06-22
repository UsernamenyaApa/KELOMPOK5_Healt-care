# patient_service/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Salin hanya requirements.txt untuk service ini
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari folder patient_service ke /app di dalam container
# Sekarang, konteks build hanya akan menjadi folder patient_service
COPY . /app/

# Script untuk menjalankan aplikasi dengan opsi seeding
# Karena sekarang kita di dalam /app dan isinya adalah konten patient_service,
# path-nya menjadi langsung "./entrypoint.sh" atau "entrypoint.sh"
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Path untuk seeder dan main sekarang langsung dari /app
CMD ["/app/entrypoint.sh"]
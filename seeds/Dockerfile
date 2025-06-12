FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["python", "-m", "seeds.seed_doctor", "&&", "python", "-m", "seeds.seed_patient", "&&", "python", "-m", "seeds.seed_appointment", "&&", "python", "-m", "seeds.seed_medicine"]
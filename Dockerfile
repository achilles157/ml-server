# Dockerfile di dalam folder functions/

# Gunakan image Python resmi sebagai base
FROM python:3.9-slim-buster

# Atur direktori kerja di dalam container
WORKDIR /app

# Copy file requirements.txt dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua kode aplikasi Anda (termasuk model .tflite)
COPY . .

# Variabel lingkungan untuk port. Cloud Run akan mengeset PORT secara otomatis
ENV PORT=8080

# Perintah untuk menjalankan aplikasi Anda
# Uvicorn adalah ASGI server untuk FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
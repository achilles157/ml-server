# Gunakan image Python resmi sebagai base
FROM python:3.9-slim-buster

# Atur direktori kerja di dalam container
WORKDIR /app

# Copy file requirements.txt dan install dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua kode aplikasi Anda (termasuk model .tflite dan service account key)
# Pastikan struktur direktori di container sesuai
COPY app ./app
COPY ml_models ./ml_models

# Expose port yang akan digunakan Railway
EXPOSE $PORT

# Perintah untuk menjalankan aplikasi Anda menggunakan Uvicorn
# Sesuaikan path ke main:app sesuai struktur folder Anda
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
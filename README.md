# PaddyPadi - Model Ahli Backend (FastAPI)

Repositori ini berisi implementasi backend untuk Model Ahli yang digunakan oleh aplikasi _frontend_ [PaddyPadi 🌱](https://github.com/nama-pengguna-anda/paddypadi) (link ke repo frontend Anda). Backend ini bertanggung jawab untuk menerima gambar daun padi dan mengembalikan prediksi penyakit menggunakan model _machine learning_ yang lebih kompleks dan akurat.

## ✨ Fitur Utama

* **Endpoint Prediksi Gambar:** Menerima _request_ POST dengan gambar dan mengembalikan hasil prediksi (kelas penyakit dan _confidence_).
* **Model _Machine Learning_ Tingkat Lanjut:** Menggunakan model (misalnya, Keras/TensorFlow, PyTorch) yang dilatih untuk deteksi penyakit padi dengan akurasi tinggi.
* **Pengolahan Gambar:** Melakukan pra-pemrosesan gambar yang masuk agar sesuai dengan input model.
* **API Cepat dan Skalabel:** Dibangun dengan [FastAPI](https://fastapi.tiangolo.com/) (atau [Nama Framework Anda, misal: Flask](https://flask.palletsprojects.com/)) untuk kinerja tinggi dan kemudahan _deployment_.
* **Lintas Platform:** Dapat di-_deploy_ di berbagai _cloud provider_ seperti Railway, Google Cloud Run, AWS EC2/Lambda, dll.

## 🚀 Teknologi yang Digunakan

* **Bahasa Pemrograman:** Python ([Versi Python yang Anda gunakan, misal: 3.9+](https://www.python.org/))
* **Web Framework:** [FastAPI](https://fastapi.tiangolo.com/) (atau Flask/lainnya)
* **_Machine Learning Library_:** [TensorFlow](https://www.tensorflow.org/) / [Keras](https://keras.io/) (atau PyTorch/lainnya)
* **_Image Processing_:** [Pillow (PIL)](https://python-pillow.org/) / [OpenCV](https://opencv.org/)
* **(Opsional) Containerization:** [Docker](https://www.docker.com/)

## 🛠️ Instalasi & Setup Lokal

Ikuti langkah-langkah di bawah untuk menjalankan backend ini di lingkungan lokal Anda.

### Prasyarat

* Python ([Versi Python yang Anda gunakan])
* `pip` (Python package installer)
* `venv` (Direkomendasikan untuk _virtual environment_)

### Langkah-langkah

1.  **Clone Repositori:**
    ```bash
    git clone [https://github.com/nama-pengguna-anda/paddy-padi-expert-model-backend.git](https://github.com/nama-pengguna-anda/paddy-padi-expert-model-backend.git)
    cd paddy-padi-expert-model-backend
    ```

2.  **Buat dan Aktifkan _Virtual Environment_:**
    ```bash
    python -m venv venv
    # Di Windows
    .\venv\Scripts\activate
    # Di macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Pastikan Anda memiliki file `requirements.txt` yang berisi semua dependensi Python, contoh: `fastapi`, `uvicorn`, `tensorflow`, `Pillow`, dll.)*

4.  **Tempatkan Model Anda:**
    * Letakkan file model _machine learning_ Anda (misalnya, `model.h5`, `saved_model/`) di lokasi yang diharapkan oleh aplikasi backend. Biasanya ini di dalam folder proyek, seperti `models/` atau di _root_ folder.
    * Jika model Anda diunduh dari GCS atau S3, pastikan kredensial dan logika pengunduhan sudah dikonfigurasi.

5.  **Jalankan Aplikasi Backend:**

    * **Untuk FastAPI:**
        ```bash
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ```
        (Asumsi file utama Anda adalah `main.py` dan objek aplikasi Anda bernama `app`)

    * **Untuk Flask:**
        ```bash
        flask run --host 0.0.0.0 --port 8000
        ```
        (Pastikan `FLASK_APP` diatur dengan benar, misal: `export FLASK_APP=app.py`)

    Aplikasi akan berjalan di `http://localhost:8000`. Anda dapat mengakses dokumentasi API interaktif (Swagger UI) di `http://localhost:8000/docs` jika menggunakan FastAPI.

## 💻 Penggunaan API

### Endpoint: `/predict`

* **Metode:** `POST`
* **Deskripsi:** Menerima gambar dan mengembalikan prediksi penyakit.
* **Header:** `Content-Type: multipart/form-data`
* **Body:**
    * `file` (File): Gambar daun padi yang akan diprediksi.

### Contoh _Request_ (menggunakan `curl`):

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/image.jpg;type=image/jpeg"
```

### Contoh _Response_:

```json
{
  "class_name": "bacterial_leaf_blight",
  "confidence": 0.9578,
  "model": "expert-server (keras)"
}
```

## ☁️ Deployment

Backend ini dapat di-_deploy_ di berbagai layanan _cloud_ seperti:

* **Railway:** Cukup tautkan repositori GitHub Anda dan konfigurasikan proses build.
* **Google Cloud Run:** Ideal untuk _containerized applications_ yang _serverless_ dan diskalakan secara otomatis.
* **AWS Lambda & API Gateway:** Untuk arsitektur _serverless_ dengan _pay-per-use_.
* **Heroku:** Platform-as-a-Service (PaaS) yang mudah digunakan.

**Catatan Penting untuk _Deployment_:**

* Pastikan Anda mengkonfigurasi variabel lingkungan yang diperlukan (misalnya, `PORT`, `MODEL_PATH`, dll.) di lingkungan _deployment_ Anda.
* Jika model Anda besar, pertimbangkan untuk menyimpannya di _cloud storage_ (misalnya, Google Cloud Storage, AWS S3) dan mengunduhnya saat aplikasi di-_deploy_ atau dimulai untuk mengurangi ukuran _image_ Docker dan waktu _cold start_.
* Konfigurasi CORS (Cross-Origin Resource Sharing) dengan benar di backend Anda untuk mengizinkan _request_ dari _domain_ frontend aplikasi Anda.

## 🤝 Kontribusi

Kontribusi selalu diterima\! Jika Anda memiliki saran atau ingin meningkatkan model/API, silakan _fork_ repositori ini dan buat _pull request_.

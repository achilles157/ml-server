# server/app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .services import prediction_service
from .models import schemas
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("./paddypadi-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)

# Konteks manager untuk memuat model saat startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kode ini berjalan saat server dimulai
    prediction_service.load_model()
    yield
    # Kode ini berjalan saat server dimatikan (jika ada cleanup)

app = FastAPI(
    title="PaddyPadi Backend API",
    lifespan=lifespan # Menjalankan fungsi load_model saat startup
)

# Mengizinkan frontend React untuk mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ganti dengan URL frontend Anda untuk produksi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Cek Status Server")
def read_root():
    return {"status": "PaddyPadi API is running"}

@app.post("/predict", 
          response_model=schemas.PredictionResponse, 
          summary="Prediksi Penyakit Padi")
async def handle_prediction(image: UploadFile = File(..., description="File gambar daun padi.")):
    """
    Endpoint ini menerima gambar dan mengembalikan diagnosis dari model ahli.
    """
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Tipe file tidak valid. Harap unggah gambar.")

    image_bytes = await image.read()
    
    try:
        result = await prediction_service.predict(image_bytes)
        return result
    except Exception as e:
        # Menangani error yang mungkin terjadi selama prediksi
        raise HTTPException(status_code=500, detail=f"Terjadi error saat prediksi: {str(e)}")
    
@app.post("/set-admin/{email}")
def set_admin_role(email: str):
    """Endpoint aman untuk menjadikan user sebagai admin."""
    # Tambahkan logika untuk memastikan hanya admin lain yang bisa memanggil ini
    try:
        user = auth.get_user_by_email(email)
        # Set custom claim 'admin' menjadi true
        auth.set_custom_user_claims(user.uid, {'admin': True})
        return {"message": f"User {email} telah dijadikan admin."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User tidak ditemukan: {str(e)}")
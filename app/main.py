from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .services import prediction_service
import os
import json
import firebase_admin
from firebase_admin import credentials, auth

firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
if firebase_creds_json:
    firebase_creds_dict = json.loads(firebase_creds_json)
    cred = credentials.Certificate(firebase_creds_dict)
    firebase_admin.initialize_app(cred)
else:
    print("WARNING: FIREBASE_CREDENTIALS_JSON environment variable not set.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    prediction_service.load_model()
    yield

app = FastAPI(
    title="PaddyPadi Backend API",
    lifespan=lifespan 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Cek Status Server")
def read_root():
    return {"status": "PaddyPadi API is running"}

@app.post("/predict", 
          summary="Prediksi Penyakit Padi")
async def handle_prediction(image: UploadFile = File(..., description="File gambar daun padi.")):
    if not (image.content_type and image.content_type.startswith("image/")):
        raise HTTPException(status_code=400, detail="Tipe file tidak valid. Harap unggah gambar.")

    image_bytes = await image.read()
    
    try:
        result = await prediction_service.predict(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi error saat prediksi: {str(e)}")
    
@app.post("/set-admin/{email}")
def set_admin_role(email: str):
    try:
        user = auth.get_user_by_email(email)
        auth.set_custom_user_claims(user.uid, {'admin': True})
        return {"message": f"User {email} telah dijadikan admin."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User tidak ditemukan: {str(e)}")
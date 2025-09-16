# server/app/services/prediction_service.py

import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os

# --- Konfigurasi Model ---
# Path ke model .h5 Anda di dalam direktori server/
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models', 'expert_model.h5')
IMAGE_SIZE = (224, 224) # Sesuaikan dengan ukuran input EfficientNetB0 Anda
CLASS_NAMES = [
    'bacterial_leaf_blight', 'bacterial_leaf_streak', 'bacterial_panicle_blight',
    'blast', 'brown_spot', 'dead_heart', 'downy_mildew', 'hispa', 'normal', 'tungro'
] # Sesuaikan dengan 10 kelas dari dataset Anda

# --- Pemuatan Model ---
# Variabel global untuk menyimpan model yang sudah dimuat
expert_model = None

def load_model():
    """Memuat model Keras dari file .h5 ke dalam memori."""
    global expert_model
    if os.path.exists(MODEL_PATH):
        print(f"Memuat model ahli dari: {MODEL_PATH}")
        expert_model = tf.keras.models.load_model(MODEL_PATH)
        print("Model ahli berhasil dimuat.")
    else:
        print(f"PERINGATAN: File model tidak ditemukan di {MODEL_PATH}. Menjalankan dalam mode dummy.")
        expert_model = None

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Mengubah byte gambar menjadi format yang siap untuk model."""
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize(IMAGE_SIZE)
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    # Menambahkan dimensi batch dan normalisasi jika diperlukan (misal: / 255.0)
    image_batch = np.expand_dims(image_array, axis=0)
    return image_batch / 255.0 # Normalisasi piksel ke rentang [0, 1]

async def predict(image_bytes: bytes) -> dict:
    """
    Melakukan prediksi menggunakan model ahli yang telah dimuat.
    Jika model tidak ada, akan mengembalikan hasil dummy.
    """
    if expert_model is None:
        # --- LOGIKA DUMMY ---
        # Ini hanya akan berjalan jika expert_model.h5 tidak ditemukan
        import random
        import asyncio
        await asyncio.sleep(1) # Simulasi delay
        dummy_class = random.choice(CLASS_NAMES)
        dummy_confidence = round(random.uniform(0.85, 0.99), 4)
        return {"class_name": dummy_class, "confidence": dummy_confidence}
        # --- AKHIR LOGIKA DUMMY ---

    # --- LOGIKA MODEL ASLI ---
    processed_image = preprocess_image(image_bytes)
    
    # Lakukan prediksi
    predictions = expert_model.predict(processed_image)
    
    # Proses hasilnya
    predicted_class_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class_index])
    class_name = CLASS_NAMES[predicted_class_index]
    
    return {"class_name": class_name, "confidence": confidence}
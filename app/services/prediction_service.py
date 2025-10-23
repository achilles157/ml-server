# server/app/services/prediction_service.py

import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os

# --- Konfigurasi Model ---
# PERUBAHAN: Ganti nama file ke .tflite
MODEL_FILENAME = "model_quantized_int8.tflite" # Nama file TFLite Anda
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models', MODEL_FILENAME)
IMAGE_SIZE = (256, 256) # Sesuaikan dengan ukuran input model Anda
CLASS_NAMES = [
    'bacterial_leaf_blight', 'bacterial_leaf_streak', 'bacterial_panicle_blight',
    'blast', 'brown_spot', 'dead_heart', 'downy_mildew', 'hispa', 'normal', 'tungro'
] # Pastikan urutan kelas ini sama persis dengan saat pelatihan

# --- Pemuatan Model (Interpreter TFLite dari TensorFlow) ---
interpreter = None
input_details = None
output_details = None

def load_model():
    """Memuat model TFLite (.tflite) ke dalam memori menggunakan tf.lite."""
    global interpreter, input_details, output_details
    if os.path.exists(MODEL_PATH):
        print(f"Memuat model TFLite dari: {MODEL_PATH}")
        # PERUBAHAN: Gunakan tf.lite.Interpreter
        interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print("Model TFLite berhasil dimuat.")
        print(f"Tipe data input yang diharapkan: {input_details[0]['dtype']}")
    else:
        raise FileNotFoundError(f"ERROR: File model '{MODEL_FILENAME}' tidak ditemukan di {os.path.dirname(MODEL_PATH)}. Server tidak dapat memulai.")

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Mengubah byte gambar menjadi format yang siap untuk model TFLite."""
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize(IMAGE_SIZE)
    # PERUBAHAN: Ubah ke array numpy float32, sesuai tipe input TFLite
    image_array = np.array(image, dtype=np.float32)
    # Tambahkan dimensi batch
    image_batch = np.expand_dims(image_array, axis=0)
    # Normalisasi / 255.0 TIDAK diperlukan karena model Keras asli Anda include_preprocessing=True
    # Model TFLite yang dikonversi dari sana juga mengharapkan input [0, 255] float32
    return image_batch

async def predict(image_bytes: bytes) -> dict:
    """
    Melakukan prediksi menggunakan model TFLite yang telah dimuat.
    """
    global interpreter, input_details, output_details

    # PERUBAHAN: Tambahkan pengecekan untuk input_details dan output_details
    if interpreter is None or input_details is None or output_details is None:
         raise RuntimeError("Interpreter TFLite atau detail input/output belum dimuat. Server tidak dapat melakukan prediksi.")

    processed_image = preprocess_image(image_bytes)

    # Dapatkan tipe data dan indeks input (sekarang aman karena sudah dicek)
    input_dtype = input_details[0]['dtype']
    input_index = input_details[0]['index']

    # Pastikan tipe data input sesuai
    if processed_image.dtype != input_dtype:
         processed_image = processed_image.astype(input_dtype)

    # Set tensor input
    interpreter.set_tensor(input_index, processed_image)

    # Jalankan inferensi
    interpreter.invoke()

    # Dapatkan hasil (sekarang aman karena output_details sudah dicek)
    output_index = output_details[0]['index']
    predictions = interpreter.get_tensor(output_index)

    # Proses hasilnya
    predicted_class_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class_index])
    class_name = CLASS_NAMES[predicted_class_index]

    return {"class_name": class_name, "confidence": confidence}
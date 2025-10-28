import numpy as np
import tensorflow as tf
from PIL import Image
import io
import os

MODEL_FILENAME = "model_quantized_int8.tflite" 
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'ml_models', MODEL_FILENAME)
IMAGE_SIZE = (256, 256) 
CLASS_NAMES = [
    'bacterial_leaf_blight', 'bacterial_leaf_streak', 'bacterial_panicle_blight',
    'blast', 'brown_spot', 'dead_heart', 'downy_mildew', 'hispa', 'normal', 'tungro'
] 

interpreter = None
input_details = None
output_details = None

def load_model():
    """Memuat model TFLite (.tflite) ke dalam memori menggunakan tf.lite."""
    global interpreter, input_details, output_details
    if os.path.exists(MODEL_PATH):
        print(f"Memuat model TFLite dari: {MODEL_PATH}")
        interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print("Model TFLite berhasil dimuat.")
        print(f"Tipe data input yang diharapkan: {input_details[0]['dtype']}")
    else:
        raise FileNotFoundError(f"ERROR: File model '{MODEL_FILENAME}' tidak ditemukan di {os.path.dirname(MODEL_PATH)}. Server tidak dapat memulai.")

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize(IMAGE_SIZE)
    image_array = np.array(image, dtype=np.float32)
    image_batch = np.expand_dims(image_array, axis=0)
    return image_batch

async def predict(image_bytes: bytes) -> dict:
    global interpreter, input_details, output_details

    if interpreter is None or input_details is None or output_details is None:
         raise RuntimeError("Interpreter TFLite atau detail input/output belum dimuat. Server tidak dapat melakukan prediksi.")

    processed_image = preprocess_image(image_bytes)
    input_dtype = input_details[0]['dtype']
    input_index = input_details[0]['index']

    if processed_image.dtype != input_dtype:
         processed_image = processed_image.astype(input_dtype)

    interpreter.set_tensor(input_index, processed_image)
    interpreter.invoke()

    output_index = output_details[0]['index']
    predictions = interpreter.get_tensor(output_index)
    predicted_class_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class_index])
    class_name = CLASS_NAMES[predicted_class_index]

    return {"class_name": class_name, "confidence": confidence}
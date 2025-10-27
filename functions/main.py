# main.py
from fastapi import FastAPI, File, UploadFile
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Memuat model TensorFlow Lite
interpreter = tf.lite.Interpreter(model_path="ml-models/model_quantized_int8.tflite")
interpreter.allocate_tensors()

# Mendapatkan input dan output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.get("/")
async def root():
    return {"message": "PaddyPadi ML Backend is running!"}

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    # Baca gambar
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Preprocessing gambar sesuai kebutuhan model Anda
    input_shape = input_details[0]['shape'] # (1, height, width, 3)
    input_height, input_width = input_shape[1], input_shape[2]
    image = image.resize((input_width, input_height))
    input_data = np.array(image, dtype=np.uint8) # Ubah ke uint8
    input_data = np.expand_dims(input_data, axis=0) # Tambah batch dimension

    # Set tensor input
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Jalankan inferensi
    interpreter.invoke()

    # Dapatkan hasil
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Post-processing output (misal, mendapatkan kelas/probabilitas)
    # Sesuaikan ini dengan output model Anda
    predicted_class = np.argmax(output_data[0]) 
    
    return {"prediction": int(predicted_class), "raw_output": output_data.tolist()}